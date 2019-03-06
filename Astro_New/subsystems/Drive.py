import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import navx

import wpilib
from wpilib import SmartDashboard

from CRLibrary.physics import DCMotorTransmission as DCMotor
from CRLibrary.physics import DifferentialDrive as dDrive
from CRLibrary.path import odometry as od
from CRLibrary.path import Path
from CRLibrary.util import units
from sim import simComms

import map

class Drive():

    mode = ""

    distPID = 0
    anglePID = 0

    prevDist = [0,0]

    maxSpeed = 1

    model = None

    yaw = 0
    pitch = 0
    roll = 0

    leftVal = 0
    rightVal = 0

    leftConv = 6/12 * math.pi / 256
    rightConv = -6/12 * math.pi / 256

    def driveInit(self, Robot):
        self.maxspeed = 0.9
        self.robot = Robot
        self.debug = True
        self.preferences = wpilib.Preferences.getInstance()
        timeout = 0

        TalonLeft = Talon(map.driveLeft1)
        TalonRight = Talon(map.driveRight1)

        leftInverted = True
        rightInverted = False

        if map.robotId == map.astroV1:
            leftInverted = False
            rightInverted = True
            
        TalonLeft.setInverted(leftInverted)
        TalonRight.setInverted(rightInverted)

        if not wpilib.RobotBase.isSimulation():
            VictorLeft1 = Victor(map.driveLeft2)
            VictorLeft2 = Victor(map.driveLeft3)
            VictorLeft1.setName("Drive", "Victor Left 1")
            VictorLeft2.setName("Drive", "Victor Left 2")
            VictorLeft1.follow(TalonLeft)
            VictorLeft2.follow(TalonLeft)

            VictorRight1 = Victor(map.driveRight2)
            VictorRight2 = Victor(map.driveRight3)
            VictorRight1.setName("Drive", "Victor Right 1")
            VictorRight2.setName("Drive", "Victor Right 2")
            VictorRight1.follow(TalonRight)
            VictorRight2.follow(TalonRight)

            for motor in [VictorLeft1,VictorLeft2]:
                motor.clearStickyFaults(timeout)
                #motor.setSafetyEnabled(True)
                motor.setInverted(leftInverted)

            for motor in [VictorRight1,VictorRight2]:
                motor.clearStickyFaults(timeout)
                #motor.setSafetyEnabled(True)
                motor.setInverted(rightInverted)


        for motor in [TalonLeft,TalonRight]:
            motor.setSafetyEnabled(False)
            motor.clearStickyFaults(timeout) #Clears sticky faults

            motor.configContinuousCurrentLimit(15,timeout) #15 Amps per motor
            motor.configPeakCurrentLimit(20,timeout) #20 Amps during Peak Duration
            motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(12,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

            motor.configOpenLoopRamp(0.2,timeout) #number of seconds from 0 to 1

        self.left = TalonLeft
        self.right = TalonRight

        self.accel = wpilib.BuiltInAccelerometer()
        #self.navx = navx.AHRS.create_spi()
        self.navx = None

        self.leftEncoder = wpilib.Encoder(map.leftEncoder[0], map.leftEncoder[1])
        self.leftEncoder.setName("Drive", "Left Encoder")
        self.leftEncoder.setDistancePerPulse(self.leftConv)
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(map.rightEncoder[0], map.rightEncoder[1])
        self.rightEncoder.setName("Drive", "Right Encoder")
        self.rightEncoder.setDistancePerPulse(self.rightConv)
        self.rightEncoder.setSamplesToAverage(10)

        self.TolDist = 0.2 #feet
        [kP,kI,kD,kF] = [0.07, 0.00, 0.20, 0.00]
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.40, 0.00, 1.50, 0.00]
        distController = wpilib.PIDController(kP, kI, kD, kF, source=self.__getDistance__, output=self.__setDistance__)
        distController.setInputRange(0, 50) #feet
        distController.setOutputRange(-0.9, 0.9)
        distController.setAbsoluteTolerance(self.TolDist)
        distController.setContinuous(False)
        self.distController = distController
        self.distController.disable()

        self.TolAngle = 3 #degrees
        [kP,kI,kD,kF] = [0.024, 0.00, 0.20, 0.00]
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.020,0.00,0.00,0.00]
        angleController = wpilib.PIDController(kP, kI, kD, kF, source=self.__getAngle__, output=self.__setAngle__)
        angleController.setInputRange(-180,  180) #degrees
        angleController.setOutputRange(-0.9, 0.9)
        angleController.setAbsoluteTolerance(self.TolAngle)
        angleController.setContinuous(True)
        self.angleController = angleController
        self.angleController.disable()

        self.odMain = od.Odometer(self.robot.period)
        self.odTemp = od.Odometer(self.robot.period)

        Ltrans = DCMotor.DCMotorTransmission(5.21, 4.14, 1.08)
        Rtrans = DCMotor.DCMotorTransmission(5.21, 4.14, 1.2)
        self.model = dDrive.DifferentialDrive(29, 1.83, 0, units.inchesToMeters(3.0), units.inchesToMeters(14), Ltrans, Rtrans)
        self.maxVel = self.maxSpeed*self.model.getMaxAbsVelocity(0, 0, 12)
        self.Path = Path.Path(self, self.model, self.odTemp, self.getDistance)

    def drivePeriodic(self):
        self.updateSensors()
        self.setDirect()
        self.joystick0 = map.getJoystick(0)
        self.joystick1 = map.getJoystick(1)

        left = self.joystick0.getRawAxis(map.drive)
        right = self.joystick1.getRawAxis(map.drive)
        # half-speed
        if self.joystick1.getRawButton(map.halfSpeed) or self.joystick0.getRawButton(map.halfSpeed):
            left = left / 2
            right = right / 2

        if (abs(left)<0.025) and (abs(right)<0.025):
            self.tankDrive (0 ,0)
        else:
            #flipped
            if self.joystick1.getRawButton(map.flip) or self.joystick0.getRawButton(map.flip) :
                self.__tankDrive__(-right * self.maxspeed ,-left * self.maxspeed)
            else:
                self.__tankDrive__(left * self.maxspeed ,right * self.maxspeed)


    def __getDistance__(self): return self.getAvgDistance()
    def __setDistance__(self,output): self.distPID = output

    def __getAngle__(self): return self.getAngle()
    def __setAngle__(self,output): self.anglePID = output

    def setMode(self, mode, name=None, distance=0, angle=0):
        self.distPID = 0
        self.anglePID = 0
        if(mode=="Distance"):
            self.distController.setSetpoint(distance)
            self.angleController.disable()
            self.distController.enable()
        elif(mode=="Angle"):
            self.angleController.setSetpoint(angle)
            self.distController.disable()
            self.angleController.enable()
        elif(mode=="Combined"):
            self.distController.setSetpoint(distance)
            self.angleController.setSetpoint(angle)
            self.distController.enable()
            self.angleController.enable()
        elif(mode=="DriveStraight"):
            self.angleController.setSetpoint(angle)
            self.distController.disable()
            self.angleController.enable()
        elif(mode=="Path"):
            self.distController.disable()
            self.angleController.disable()
            self.Path.initPath(name)
        elif(mode=="DiffDrive"):
            self.distController.disable()
            self.angleController.disable()
        elif(mode=="Direct"):
            self.distController.disable()
            self.angleController.disable()
        self.mode = mode


    def setDistance(self, distance): self.setMode("Distance",distance=distance)
    def setAngle(self, angle): self.setMode("Angle",angle=angle)
    def setCombined(self, distance, angle): self.setMode("Combined",distance=distance,angle=angle)

    def setPath(self, name, follower):
        self.Path.setFollower(follower)
        self.setMode("Path", name=name)

    def setDiffDrive(self): self.setMode("DiffDrive")
    def setDirect(self): self.setMode("Direct")

    def sign(self,num):
        if(num>0): return 1
        if(num==0): return 0
        return -1

    def diffAssist(self, left, right):
        wheelVelocity = dDrive.WheelState(left*self.maxVel/self.model.wheelRadius(), right*self.maxVel/self.model.wheelRadius())
        wheelAcceleration = dDrive.WheelState(0, 0) #Add better math here later
        voltage = self.model.solveInverseDynamics_WS(wheelVelocity, wheelAcceleration).getVoltage()
        return [voltage[0]/12, voltage[1]/12]

    def tankDrive(self,left=0,right=0):
        self.updateSensors()

        if(self.mode=="Distance"): [left,right] = [self.distPID,self.distPID]
        elif(self.mode=="Angle"): [left,right] = [self.anglePID,-self.anglePID]
        elif(self.mode=="Combined"): [left,right] = [self.distPID+self.anglePID,self.distPID-self.anglePID]
        elif(self.mode=="Path"): [left, right] = self.Path.followPath()
        elif(self.mode=="DriveStraight"): [left, right] = [left+self.anglePID, right-self.anglePID]
        elif(self.mode=="DiffDrive"): [left, right] = self.diffAssist(left, right)
        elif(self.mode=="Direct"): [left, right] = [left, right] #Add advanced math here
        else: [left, right] = [0,0]

        left = min(abs(left),self.maxSpeed)*self.sign(left)
        right = min(abs(right),self.maxSpeed)*self.sign(right)
        self.__tankDrive__(left,right)

    def __tankDrive__(self,left,right):
        self.left.set(right)
        self.right.set(left)
        self.updateOdometry()

    def updateOdometry(self):
        vel = self.getVelocity()
        self.odMain.update(vel[0], vel[1], self.getAngle())
        self.odTemp.update(vel[0], vel[1], self.getAngle())
        self.prevDist = self.getDistance()

    def getOutputCurrent(self):
        return (self.right.getOutputCurrent()+self.left.getOutputCurrent())*3

    def updateSensors(self):
        if self.navx == None:
            self.yaw = 0
        else:
            self.yaw = self.navx.getYaw() * -1
        self.leftVal = self.leftEncoder.get()
        self.rightVal = self.rightEncoder.get()

    def getAngle(self):
        return (self.yaw)


    def getRaw(self): return [self.leftVal, self.rightVal]
    def getDistance(self): return [self.leftVal*self.leftConv, self.rightVal*self.rightConv]
    def getAvgDistance(self): return (self.getDistance()[0]+self.getDistance()[1])/2
    def getVelocity(self):
        dist = self.getDistance()
        velocity = [self.robot.frequency*(dist[0]-self.prevDist[0]),self.robot.frequency*(dist[1]-self.prevDist[1])]
        self.prevDist = dist
        return velocity

    def getAvgVelocity(self): return (self.getVelocity()[0]+self.getVelocity()[1])/2
    def getAvgAbsVelocity(self): return (abs(self.getVelocity()[0])+abs(self.getVelocity()[1]))/2

    def zeroEncoders(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        simComms.resetEncoders()

    def zeroNavx(self):
        if self.navx == None:
            pass
        else:
            self.navx.zeroYaw()

    def zero(self):
        self.zeroEncoders()
        self.zeroNavx()

    def initDefaultCommand(self):
        self.setDefaultCommand(SetSpeedDT(timeout = 300))

    def disable(self):
        self.__tankDrive__(0,0)

    def updateDashboardInit(self):
        pass

    def updateDashboardPeriodic(self):
        SmartDashboard.putNumber("Left Counts", self.leftEncoder.get())
        SmartDashboard.putNumber("Left Distance", self.leftEncoder.getDistance())
        SmartDashboard.putNumber("Right Counts", self.rightEncoder.get())
        SmartDashboard.putNumber("Right Distance", self.rightEncoder.getDistance())
        SmartDashboard.putNumber("DT_DistanceAvg", self.getAvgDistance())
        SmartDashboard.putNumber("DT_DistanceLeft", self.getDistance()[0])
        SmartDashboard.putNumber("DT_DistanceRight", self.getDistance()[1])
        SmartDashboard.putNumber("DT_Angle", self.getAngle())
        SmartDashboard.putNumber("DT_PowerLeft", self.left.get())
        SmartDashboard.putNumber("DT_PowerRight", self.right.get())
        SmartDashboard.putNumber("DT_VelocityLeft", self.getVelocity()[0])
        SmartDashboard.putNumber("DT_VelocityRight", self.getVelocity()[1])
        SmartDashboard.putNumber("DT_CounLeft", self.getRaw()[0])
        SmartDashboard.putNumber("DT_CountRight", self.getRaw()[1])

    def bumpCheck(self, bumpInt = 0.4):
        self.accelX = self.accel.getX()
        self.accelY = self.accel.getY()
        if abs(self.accelX) >= bumpInt or abs(self.accelY) >= bumpInt: return True
        return False
