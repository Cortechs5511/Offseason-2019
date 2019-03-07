import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
import wpilib.encoder

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

from commands.climber.liftRobot import LiftRobot
from commands.climber.lowerRobot import LowerRobot
from commands.climber.setSpeedWheel import SetSpeedWheel
from commands.climber.setSpeedClimber import SetSpeedClimber
#from commands.climber.autoClimb import AutoClimb
from subsystems.disableAll import DisableAll
from commands.climber.driveToEdge import DriveToEdge

import math
import oi
import map

class Climber(Subsystem):

    def __init__(self, robot):
        super().__init__('Climber')

        self.robot = robot
        self.debug = True
        timeout = 0
        self.xbox = oi.getJoystick(2)

        if map.robotId == map.astroV1:
            self.backLift = Talon(map.backLift)
            self.frontLift = Talon(map.frontLift)
        else:
            #MOTORS ARE SWITCHED ON V2
            self.backLift = Talon(map.frontLift)
            self.frontLift = Talon(map.backLift)

        if map.robotId == map.astroV1:
            self.frontLift.setInverted(True)
            self.backLift.setInverted(True)
        else:
            self.frontLift.setInverted(False)
            self.backLift.setInverted(True)

        if map.robotId == map.astroV1:
            self.wheelLeft = Victor(map.wheelLeft)
            self.wheelRight = Victor(map.wheelRight)
        elif map.robotId == map.astroV2:
            self.wheelLeft = Talon(map.wheelLeft)
            self.wheelRight = Talon(map.wheelRight)

        if map.robotId == map.astroV1:
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(True)
        elif map.robotId == map.astroV2:
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(False)

        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)

        for motor in [self.backLift, self.frontLift, self.wheelLeft, self.wheelRight]:
            motor.clearStickyFaults(timeout)
            motor.setSafetyEnabled(False)

        for motor in [self.backLift, self.frontLift]:
            motor.configContinuousCurrentLimit(30,timeout) #Amps per motor
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(10,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

        self.MAX_ANGLE = 3 #degrees
        self.MAX_ROLL = 2 #degrees
        self.climbSpeed = 0.9 #out of 1
        self.wheelSpeed = 0.9 #out of 1

    def subsystemInit(self):
        r = self.robot

        '''climberWheelsForward : wpilib.buttons.JoystickButton = r.operator2Button(map.driveForwardClimber)
        climberWheelsForward.whileHeld(SetSpeedWheel(1))

        climberWheelsBackward : wpilib.buttons.JoystickButton = r.operator2Button(map.driveBackwardClimber)
        climberWheelsBackward.whileHeld(SetSpeedWheel(-1))

        liftButton : wpilib.buttons.JoystickButton = r.operator2Button(map.lowerClimber)
        liftButton.whileHeld(LiftRobot("both"))

        liftButton : wpilib.buttons.JoystickButton = r.operator2Button(map.liftClimber)
        liftButton.whileHeld(LowerRobot("both"))

        disableAll : wpilib.buttons.JoystickButton =r.operator2Button(map.disableAll)
        disableAll.whenPressed(DisableAll())

        climberFrontUp : wpilib.buttons.JoystickButton = r.operato2Button(13)
        climberFrontUp.whileHeld(LiftRobot("front"))

        climberFrontDown : wpilib.buttons.JoystickButton = r.driverLeftButton(14)
        climberFrontDown.whileHeld(LowerRobot("front"))

        climberBackUp : wpilib.buttons.JoystickButton = r.driverLeftButton(12)
        climberBackUp.whileHeld(LiftRobot("back"))

        climberBackDown : wpilib.buttons.JoystickButton = r.driverLeftButton(15)
        climberBackDown.whileHeld(LowerRobot("back"))'''

        #autoClimbButton : wpilib.buttons.JoystickButton = r.operatorButton(7)
        #autoClimbButton.whenPressed(AutoClimb())

        #killautoClimbButton : wpilib.buttons.JoystickButton = r.operatorButton(8)
        #killautoClimbButton.whenPressed(self.disable())

    def lift(self, mode):
        if mode == "front":
            if self.isLeaning(True):
                self.backLift.set(self.returnCorrectionSpeed())
            else:
                self.stopBack()
            self.frontLift.set(self.climbSpeed)
        elif mode == "back":
            self.frontLift.set(0)
            self.backLift.set(self.climbSpeed)
        elif mode == "both":
            if self.isLeaning(True):
                self.backLift.set(self.returnCorrectionSpeed())
                self.frontLift.set(self.climbSpeed)
            elif self.isLeaning(False):
                self.backLift.set(self.climbSpeed)
                self.frontLift.set(self.returnCorrectionSpeed())
            else:
                self.backLift.set(self.climbSpeed)
                self.frontLift.set(self.climbSpeed)


    def lower(self, mode):
        if mode == "front":
            if self.isLeaning(True):
                self.backLift.set(self.returnCorrectionSpeed())
            else:
                self.stopBack()
            self.frontLift.set(self.climbSpeed)
        elif mode == "back":
            self.frontLift.set(0)
            self.backLift.set(-1 * self.climbSpeed)
        elif mode == "both":
            if self.isLeaning(False):
                self.backLift.set(-1 * self.returnCorrectionSpeed())
                self.frontLift.set(-1 * self.climbSpeed)
            elif self.isLeaning(True):
                self.backLift.set(-1 * self.climbSpeed)
                self.frontLift.set(-1 * self.returnCorrectionSpeed())
            else:
                self.backLift.set(-1 * self.climbSpeed)
                self.frontLift.set(-1 * self.climbSpeed)

    def wheel(self, direction):
        if direction == "forward":
            self.wheelLeft.set(self.wheelSpeed)
            self.wheelRight.set(self.wheelSpeed)
        elif direction == "backward":
            self.wheelLeft.set(-1 * self.wheelSpeed)
            self.wheelRight.set(-1 * self.wheelSpeed)

        if self.isLeaning(False):
            self.backLift.set(-1 * self.returnCorrectionSpeed())
            self.stopFront()
        elif self.isLeaning(True):
            self.backLift.set(self.returnCorrectionSpeed())
            self.stopFront()

    def initDefaultCommand(self):
        self.setDefaultCommand(SetSpeedClimber())

    def isLeaning(self, direction):
        '''true checking tip forward'''
        if direction == True and self.getLean()+1 < -self.MAX_ANGLE :
            return True
        elif direction == False and self.getLean()-1 > self.MAX_ANGLE :
            return True
        else:
            return False

    def getLean(self):
        if map.robotId == map.astroV1:
            return self.robot.drive.getRoll()
        else:
            return self.robot.drive.getPitch()

    #wheel speed
    def wheelForward(self):
        self.wheelLeft.set(self.returnWheelSpeed())
        self.wheelRight.set(self.returnWheelSpeed())

    def wheelBack(self):
        self.wheelLeft.set(-1 * self.returnWheelSpeed())
        self.wheelRight.set(-1 * self.returnWheelSpeed())

    def stopFront(self): self.frontLift.set(0)

    def stopBack(self): self.backLift.set(0)

    def stop(self):
        self.stopFront()
        self.stopBack()

    def stopDrive(self):
        self.wheelLeft.set(0)
        self.wheelRight.set(0)

    def disable(self):
        self.stopFront()
        self.stopBack()
        self.stopDrive()

    def dashboardInit(self):
        SmartDashboard.putNumber("ClimberSpeed", 0.9)
        SmartDashboard.putNumber("WheelSpeed", 0.7)
        SmartDashboard.putNumber("Tolerance", 2)
        SmartDashboard.putData("Lift Robot", LiftRobot("both"))
        SmartDashboard.putData("Drive To Edge, Front", DriveToEdge("front"))
        SmartDashboard.putData("Drive To Edge, Back", DriveToEdge("back"))
        SmartDashboard.putData("Lift Robot, Front", LiftRobot("front"))
        SmartDashboard.putData("Lift Robot, Back", LiftRobot("back"))
        SmartDashboard.putData("Lower Robot", LowerRobot("both"))

    def dashboardPeriodic(self):
        self.MAX_ANGLE = self.returnTolerance()
        self.returnWheelSpeed()
        self.returnClimbSpeed()
        SmartDashboard.putNumber("Lean", self.getLean())

        if self.debug == True:
            SmartDashboard.putBoolean("Fully Extended Front",self.isFullyExtendedFront())
            SmartDashboard.putBoolean("Fully Extended Back",self.isFullyExtendedBack())
            SmartDashboard.putBoolean("Fully Retracted Front",self.isFullyRetractedFront())
            SmartDashboard.putBoolean("Fully Retracted Back",self.isFullyRetractedBack())
            #SmartDashboard.putData("Lean", self.getLean())

    def returnCorrectionSpeed(self):
        #proportional speed based on angle
        targetAngle = -1
        lean = self.getLean()
        error = lean - targetAngle
        multiplier = 1 - (0.1 * math.fabs(error))
        return (multiplier * self.returnClimbSpeed())
