import math

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import navx

import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

from commands.drive.diffDrive import DiffDrive
from commands.drive.drivePath import DrivePath
from commands.drive.driveStraightCombined import DriveStraightCombined
from commands.drive.driveStraightDistance import DriveStraightDistance
from commands.drive.driveStraightTime import DriveStraightTime
from commands.drive.driveVision import DriveVision
from commands.drive.setFixedDT import SetFixedDT
from commands.drive.setSpeedDT import SetSpeedDT
from commands.drive.turnAngle import TurnAngle
from commands.drive.measured import Measured
from commands.drive.relativeTurn import RelativeTurn


from CRLibrary.physics import DCMotorTransmission as DCMotor
from CRLibrary.physics import DifferentialDrive as dDrive
from CRLibrary.path import odometry as od
from CRLibrary.path import Path
from CRLibrary.util import units

from subsystems.Limelight import Limelight
from sim import simComms

import map

class Drive(Subsystem):

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

    def __init__(self, robot):
        super().__init__('Drive')

        self.robot = robot
        self.flipped = False
        self.debug = False

        timeout = 0

        self.accel = wpilib.BuiltInAccelerometer()

        TalonLeft = Talon(map.driveLeft1)
        TalonRight = Talon(map.driveRight1)

        TalonLeft.setInverted(False)
        TalonRight.setInverted(True)

        if not wpilib.RobotBase.isSimulation():
            VictorLeft1 = Victor(map.driveLeft2)
            VictorLeft2 = Victor(map.driveLeft3)
            VictorLeft1.follow(TalonLeft)
            VictorLeft2.follow(TalonLeft)

            VictorRight1 = Victor(map.driveRight2)
            VictorRight2 = Victor(map.driveRight3)
            VictorRight1.follow(TalonRight)
            VictorRight2.follow(TalonRight)

            for motor in [VictorLeft1,VictorLeft2]:
                motor.clearStickyFaults(timeout)
                motor.setSafetyEnabled(False)
                motor.setInverted(False)

            for motor in [VictorRight1,VictorRight2]:
                motor.clearStickyFaults(timeout)
                motor.setSafetyEnabled(False)
                motor.setInverted(True)


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

        self.navx = navx.AHRS.create_spi()

        self.leftEncoder = wpilib.Encoder(map.leftEncoder[0], map.leftEncoder[1])
        self.leftEncoder.setDistancePerPulse(self.leftConv)
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(map.rightEncoder[0], map.rightEncoder[1])
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

    def periodic(self):
        self.updateSensors()

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
        elif(self.mode=="DiffDrive"): [left, right] = self.diffAssist(left, right)
        elif(self.mode=="Direct"): [left, right] = [left, right] #Add advanced math here
        else: [left, right] = [0,0]

        left = min(abs(left),self.maxSpeed)*self.sign(left)
        right = min(abs(right),self.maxSpeed)*self.sign(right)
        self.__tankDrive__(left,right)

        b = self.robot.driverRightButton(2)
        b.whenPressed(FlipButton())

    def __tankDrive__(self,left,right):
        self.left.set(left)
        self.right.set(right)
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
            self.pitch = 0
            self.roll = 0
        else:
            self.yaw = self.navx.getYaw()
            self.pitch = self.navx.getPitch()
            self.roll = self.navx.getRoll()
        self.leftVal = self.leftEncoder.get()
        self.rightVal = self.rightEncoder.get()

    def getAngle(self): return self.yaw
    def getRoll(self):
        '''LeaningForward - negative,LeaningBackward - Positive'''
        return self.roll
    def getRaw(self): return [self.leftVal, self.rightVal]
    def getDistance(self): return [self.leftVal*self.leftConv, self.rightVal*self.rightConv]
    def getAvgDistance(self): return (self.getDistance()[0]+self.getDistance()[1])/2
    def getPitch(self): return self.pitch
    def getVelocity(self):
        dist = self.getDistance()
        velocity = [self.robot.frequency*(dist[0]-self.prevDist[0]),self.robot.frequency*(dist[1]-self.prevDist[1])]
        self.prevDist = dist
        return velocity

    def getAvgVelocity(self): return (self.getVelocity()[0]+self.getVelocity()[1])/2
    def getAvgAbsVelocity(self): return (abs(self.getVelocity()[0])+abs(self.getVelocity()[1]))/2

    def isFlipped(self): return self.flipped

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

    def dashboardInit(self):
        SmartDashboard.putData("Flipped drive", FlipButton())
        SmartDashboard.putData("Measure", Measured())


        if(self.debug==False): return
        SmartDashboard.putData("autonCheck Frw", AutonCheck(10))
        SmartDashboard.putData("autonCheck Bkwd", AutonCheck(-10))

        SmartDashboard.putData("DT_DiffDrive", DiffDrive())
        SmartDashboard.putData("DT_DrivePath", DrivePath())
        SmartDashboard.putData("DT_DriveStraightCombined", DriveStraightCombined())
        SmartDashboard.putData("DT_DriveStraightDistance", DriveStraightDistance())
        SmartDashboard.putData("DT_DriveStraightTime", DriveStraightTime())

        SmartDashboard.putData("DT_SetFixedDT", SetFixedDT())
        SmartDashboard.putData("DT_SetSpeedDT", SetSpeedDT())

        SmartDashboard.putData("DT_TurnAngle", TurnAngle(90))
        SmartDashboard.putData("DT_RelativeTurn", RelativeTurn(90))


    def dashboardPeriodic(self):
        SmartDashboard.putBoolean("Driving Reverse", self.flipped)
        SmartDashboard.putNumber("Roll", self.getRoll())
        if(self.debug==False): return
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

        SmartDashboard.putNumber("DriveAmps",self.getOutputCurrent())

    def bumpCheck(self, bumpInt = 0.4):
        self.accelX = self.accel.getX()
        self.accelY = self.accel.getY()

        if self.debug:
            SmartDashboard.putNumber("AccelX", self.accelX)
            SmartDashboard.putNumber("AccelY", self.accelY)

        if abs(self.accelX) >= bumpInt or abs(self.accelY) >= bumpInt: return True
        return False

class FlipButton(Command):
    def __init__(self):
        super().__init__('Flip')
        robot = self.getRobot()
        self.drive = robot.drive

    def initialize(self):
        if self.drive.flipped: self.drive.flipped = False
        else: self.drive.flipped = True

    def isFinished(self):
        return True
