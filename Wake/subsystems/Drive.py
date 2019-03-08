import math

from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

import navx

import wpilib
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
from wpilib import SmartDashboard

from wpilib import PIDController
from wpilib import Preferences
from wpilib import RobotBase
from wpilib import Encoder

from commands.drive.driveStraightTime import DriveStraightTime
from commands.drive.setFixedDT import SetFixedDT
from commands.drive.setSpeedDT import SetSpeedDT
from commands.drive.turnAngle import TurnAngle
from commands.drive.FlipButton import FlipButton

from sim import simComms

import map

class Drive(Subsystem):
    distPID = 0
    anglePID = 0

    prevDist = [0,0]

    maxSpeed = 1

    yaw = 0
    pitch = 0
    roll = 0

    leftVal = 0
    rightVal = 0

    leftConv = 6/12 * math.pi / 256
    if wpilib.RobotBase.isSimulation(): rightConv =  -6/12 * math.pi / 256
    else: rightConv = 6/12 * math.pi / 256


    def __init__(self, robot):
        super().__init__('Drive')
        SmartDashboard.putNumber("DriveStraight_P", 0.04)
        SmartDashboard.putNumber("DriveStraight_I", 0)


        self.robot = robot
        self.flipped = False
        self.debug = True
        self.preferences = Preferences.getInstance()
        timeout = 0

        TalonLeft = Talon(map.driveLeft1)
        TalonRight = Talon(map.driveRight1)

        if map.robotId == map.astroV1:
            leftInverted = True
            rightInverted = False
        else:
            leftInverted = True
            rightInverted = False

        TalonLeft.setInverted(leftInverted)
        TalonRight.setInverted(rightInverted)

        if not RobotBase.isSimulation():
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
                motor.setSafetyEnabled(False)
                #motor.setExpiration(2 * self.robot.period)
                motor.setInverted(leftInverted)

            for motor in [VictorRight1,VictorRight2]:
                motor.clearStickyFaults(timeout)
                motor.setSafetyEnabled(False)
                #motor.setExpiration(2 * self.robot.period)
                motor.setInverted(rightInverted)


        for motor in [TalonLeft,TalonRight]:
            motor.setSafetyEnabled(False)
            #motor.setExpiration(2 * self.robot.period)
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

        self.leftEncoder = Encoder(map.leftEncoder[0], map.leftEncoder[1])
        self.leftEncoder.setDistancePerPulse(self.leftConv)
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = Encoder(map.rightEncoder[0], map.rightEncoder[1])
        self.rightEncoder.setDistancePerPulse(self.rightConv)
        self.rightEncoder.setSamplesToAverage(10)

        self.TolDist = 0.2 #feet
        [kP,kI,kD,kF] = [0.02, 0.00, 0.20, 0.00]
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.25, 0.00, 1.00, 0.00]
        distController = PIDController(kP, kI, kD, kF, source=self.__getDistance__, output=self.__setDistance__)
        distController.setInputRange(0, 50) #feet
        distController.setOutputRange(-0.7, 0.7)
        distController.setAbsoluteTolerance(self.TolDist)
        distController.setContinuous(False)
        self.distController = distController
        self.distController.disable()

        self.TolAngle = 2 #degrees
        [kP,kI,kD,kF] = [0.004, 0.00, 0.01, 0.00]
        if RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.005, 0.0, 0.01, 0.00]
        angleController = PIDController(kP, kI, kD, kF, source=self.__getAngle__, output=self.__setAngle__)
        angleController.setInputRange(-180,  180) #degrees
        angleController.setOutputRange(-0.9, 0.9)
        angleController.setAbsoluteTolerance(self.TolAngle)
        angleController.setContinuous(True)
        self.angleController = angleController
        self.angleController.disable()

    def setGains(self, p, i, d, f):
        self.distController.setPID(p,i,d,f)

    def subsystemInit(self):
        driveStraightButton : wpilib.buttons.JoystickButton = r.driverLeftButton(1)
        driveStraightButton.whileHeld(DriveStraightTime(0.5))

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
        elif(mode=="DriveStraight"):
            self.angleController.setSetpoint(angle)
            self.distController.disable()
            self.angleController.enable()
        elif(mode=="Direct"):
            self.distController.disable()
            self.angleController.disable()
        self.mode = mode


    def setDistance(self, distance): self.setMode("Distance",distance=distance)
    def setAngle(self, angle): self.setMode("Angle",angle=angle)
    def setCombined(self, distance, angle): self.setMode("Combined",distance=distance,angle=angle)
    def setDirect(self): self.setMode("Direct")

    def sign(self,num):
        if(num>0): return 1
        if(num==0): return 0
        return -1

    def tankDrive(self,left=0,right=0):
        self.updateSensors()

        if(self.mode=="Distance"): [left,right] = [self.distPID,self.distPID]
        elif(self.mode=="Angle"): [left,right] = [self.anglePID,-self.anglePID]
        elif(self.mode=="Combined"): [left,right] = [self.distPID+self.anglePID,self.distPID-self.anglePID]
        elif(self.mode=="DriveStraight"): [left, right] = [left+self.anglePID, right-self.anglePID]
        elif(self.mode=="Direct"): [left, right] = [left, right] #Add advanced math here
        else: [left, right] = [0,0]

        left = min(abs(left),self.maxSpeed)*self.sign(left)
        right = min(abs(right),self.maxSpeed)*self.sign(right)
        self.__tankDrive__(left,right)

    def __tankDrive__(self,left,right):
        self.left.set(right)
        self.right.set(left)

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

    def getAngle(self):
        if RobotBase.isSimulation(): return self.yaw
        else:
            if map.robotId == map.astroV1:
                return self.yaw
            else:
                return (-1 * self.yaw)

    def getRoll(self): return self.roll
    def getPitch(self): return self.pitch

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

    def isFlipped(self): return self.flipped

    def zeroEncoders(self):
        self.leftEncoder.reset()
        self.rightEncoder.reset()
        simComms.resetEncoders()

    def zeroNavx(self):
        if self.navx == None: pass
        else: self.navx.zeroYaw()

    def zero(self):
        self.zeroEncoders()
        self.zeroNavx()

    def disable(self):
        self.__tankDrive__(0,0)

    def initDefaultCommand(self):
        self.setDefaultCommand(SetSpeedDT(timeout = 300))

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
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
