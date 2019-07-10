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

from commands.drive.driveStraightCombined import DriveStraightCombined
from commands.drive.setFixedDT import SetFixedDT
from commands.drive.setSpeedDT import SetSpeedDT
from commands.drive.turnAngle import TurnAngle

from commands.autonomous import DriveStraight as DriveStraight
from sim import simComms
import map

class Drive(Subsystem):
    distPID = 0
    anglePID = 0

    prevDist = [0,0]

    maxSpeed = 0.85

    yaw = 0
    pitch = 0
    roll = 0

    leftVal = 0
    rightVal = 0

    leftConv = 6/12 * math.pi / 256
    rightConv = -6/12 * math.pi / 256


    def __init__(self, robot):
        super().__init__('Drive')

        SmartDashboard.putNumber("DriveStraight_P", 0.075)
        SmartDashboard.putNumber("DriveStraight_I", 0.0)
        SmartDashboard.putNumber("DriveStraight_D", 0.42)
        # OLD GAINS 0.075, 0, 0.42

        SmartDashboard.putNumber("DriveAngle_P", 0.009)
        SmartDashboard.putNumber("DriveAngle_I", 0.0)
        SmartDashboard.putNumber("DriveAngle_D", 0.025)

        SmartDashboard.putNumber("DriveStraightAngle_P", 0.025)
        SmartDashboard.putNumber("DriveStraightAngle_I", 0.0)
        SmartDashboard.putNumber("DriveStraightAngle_D", 0.01)

        self.driveStyle = "Tank"
        SmartDashboard.putString("DriveStyle", self.driveStyle)
        #SmartDashboard.putData("Mode", self.mode)

        self.robot = robot
        self.lime = self.robot.limelight
        self.nominalPID = 0.15
        self.nominalPIDAngle = 0.22 # 0.11 - v2

        self.preferences = Preferences.getInstance()
        timeout = 0

        TalonLeft = Talon(map.driveLeft1)
        TalonRight = Talon(map.driveRight1)

        leftInverted = True
        rightInverted = False

        TalonLeft.setInverted(leftInverted)
        TalonRight.setInverted(rightInverted)

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

            motor.configContinuousCurrentLimit(40,timeout) #15 Amps per motor
            motor.configPeakCurrentLimit(70,timeout) #20 Amps during Peak Duration
            motor.configPeakCurrentDuration(300,timeout) #Peak Current for max 100 ms
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

        self.zero()

        #PID for Drive
        self.TolDist = 0.1 #feet
        [kP,kI,kD,kF] = [0.027, 0.00, 0.20, 0.00]
        if wpilib.RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.25, 0.00, 1.00, 0.00]
        distController = PIDController(kP, kI, kD, kF, source=self.__getDistance__, output=self.__setDistance__)
        distController.setInputRange(0, 50) #feet
        distController.setOutputRange(-0.6, 0.6)
        distController.setAbsoluteTolerance(self.TolDist)
        distController.setContinuous(False)
        self.distController = distController
        self.distController.disable()

        '''PID for Angle'''
        self.TolAngle = 2 #degrees
        [kP,kI,kD,kF] = [0.025, 0.00, 0.01, 0.00]
        if RobotBase.isSimulation(): [kP,kI,kD,kF] = [0.005, 0.0, 0.01, 0.00]
        angleController = PIDController(kP, kI, kD, kF, source=self.__getAngle__, output=self.__setAngle__)
        angleController.setInputRange(-180,  180) #degrees
        angleController.setOutputRange(-0.5, 0.5)
        angleController.setAbsoluteTolerance(self.TolAngle)
        angleController.setContinuous(True)
        self.angleController = angleController
        self.angleController.disable()

        self.k = 1
        self.sensitivity = 1

        SmartDashboard.putNumber("K Value", self.k)
        SmartDashboard.putNumber("sensitivity", self.sensitivity)

    def setGains(self, p, i, d, f):
        self.distController.setPID(p,i,d,f)

    def setGainsAngle(self, p, i, d, f):
        self.angleController.setPID(p,i,d,f)

    def periodic(self):
        self.updateSensors()

    def __getDistance__(self):
        return self.getAvgDistance()

    def __setDistance__(self,output): self.distPID = output

    def __getAngle__(self):
        return self.getAngle()

    def __setAngle__(self,output): self.anglePID = output

    def setMode(self, mode, name=None, distance=0, angle=0):
        self.distPID = 0
        self.anglePID = 0

        if(mode=="Angle"):
            self.angleController.setSetpoint(angle)
            self.distController.disable()
            self.angleController.enable()
        elif(mode=="Combined"):
            self.distController.setSetpoint(distance)
            self.angleController.setSetpoint(angle)
            self.distController.enable()
            self.angleController.enable()
        elif(mode=="Direct"):
            self.distController.disable()
            self.angleController.disable()
        self.mode = mode

    def setAngle(self, angle): self.setMode("Angle",angle=angle)
    def setCombined(self, distance, angle): self.setMode("Combined",distance=distance,angle=angle)
    def setDirect(self): self.setMode("Direct")

    def sign(self,num):
        if(num>0): return 1
        if(num==0): return 0
        return -1

    def tankDrive(self,left=0,right=0):
        if(self.mode=="Angle"):
            nom = self.nominalPIDAngle
            if self.anglePID < 0:
                nom = -nom
            left= self.getMaximum(self.anglePID, nom)
            right = self.getMaximum(-self.anglePID, -nom)
        elif(self.mode=="Combined"):
            nom = self.nominalPID
            if self.distPID < 0:
                nom = -nom

            print(self.distPID)
            left= self.getMaximum(self.distPID+self.anglePID,nom)
            right = self.getMaximum(self.distPID-self.anglePID,nom)

        elif(self.mode=="Direct"): [left, right] = [left, right]
        else: [left, right] = [0,0]

        left = min(abs(left),self.maxSpeed)*self.sign(left)
        right = min(abs(right),self.maxSpeed)*self.sign(right)
        self.__tankDrive__(left,right)

    def __tankDrive__(self,left,right):
        deadband = 0.1

        if(abs(left)>abs(deadband)): self.left.set(left)
        else: self.left.set(0)

        if(abs(right)>abs(deadband)): self.right.set(right)
        else: self.right.set(0)

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
        angle = self.yaw
        if RobotBase.isSimulation(): return -angle
        if self.robot.teleop:
            if angle == 0:
                angle = 0
            elif angle < 0:
                angle = angle + 180
            else:
                angle = angle - 180
        return angle

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
        SmartDashboard.putData("Turn Angle", TurnAngle())
        SmartDashboard.putData("Drive Combined" , DriveStraight())

    def getMaximum(self, number, comparison):
        if math.fabs(number) > math.fabs(comparison): return number
        else: return comparison

    def isCargoPassed(self):
        if self.getAvgDistance() > 16.1: return True
        else: return False

    def dashboardPeriodic(self):
        #commented out some values. DON'T DELETE THESE VALUES
        #SmartDashboard.putNumber("Left Counts", self.leftEncoder.get())
        #SmartDashboard.putNumber("Left Distance", self.leftEncoder.getDistance())
        #SmartDashboard.putNumber("Right Counts", self.rightEncoder.get())
        #SmartDashboard.putNumber("Right Distance", self.rightEncoder.getDistance())
        #SmartDashboard.putNumber("DT_DistanceAvg", self.getAvgDistance())
        #SmartDashboard.putNumber("DT_DistanceLeft", self.getDistance()[0])
        #SmartDashboard.putNumber("DT_DistanceRight", self.getDistance()[1])
        #SmartDashboard.putNumber("DT_Angle", self.getAngle())
        #SmartDashboard.putNumber("DT_PowerLeft", self.left.get())
        #SmartDashboard.putNumber("DT_PowerRight", self.right.get())
        #SmartDashboard.putNumber("DT_VelocityLeft", self.getVelocity()[0])
        #SmartDashboard.putNumber("DT_VelocityRight", self.getVelocity()[1])
        #SmartDashboard.putNumber("DT_CounLeft", self.getRaw()[0])
        #SmartDashboard.putNumber("DT_CountRight", self.getRaw()[1])
        #SmartDashboard.putNumber("angle correction", self.anglePID)
        #SmartDashboard.putNumber("DriveAmps",self.getOutputCurrent())

        #self.mode = SmartDashboard.getData("Mode", "Tank")
        self.k = SmartDashboard.getNumber("K Value", 1)
        self.sensitivity = SmartDashboard.getNumber("sensitivity", 1)
        self.driveStyle = SmartDashboard.getString("DriveStyle", "Tank")
