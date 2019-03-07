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
        self.xbox = oi.getJoystick(2)

        if map.robotId == map.astroV1:
            '''IDS AND DIRECTIONS FOR V1'''
            self.backLift = Talon(map.backLift)
            self.frontLift = Talon(map.frontLift)
            self.frontLift.setInverted(True)
            self.backLift.setInverted(True)

            self.wheelLeft = Victor(map.wheelLeft)
            self.wheelRight = Victor(map.wheelRight)
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(True)
        else:
            '''IDS AND DIRECTIONS FOR V2'''
            self.backLift = Talon(map.frontLift)
            self.frontLift = Talon(map.backLift)
            self.frontLift.setInverted(False)
            self.backLift.setInverted(True)

            self.wheelLeft = Talon(map.wheelLeft)
            self.wheelRight = Talon(map.wheelRight)
            self.wheelRight.setInverted(True)
            self.wheelLeft.setInverted(False)

        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)

        for motor in [self.backLift, self.frontLift, self.wheelLeft, self.wheelRight]:
            motor.clearStickyFaults(0)
            motor.setSafetyEnabled(False)

        for motor in [self.backLift, self.frontLift]:
            motor.configContinuousCurrentLimit(30,0) #Amps per motor
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(10,0) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

        self.backSwitch = wpilib.DigitalInput(map.backBottomSensor)
        self.frontSwitch = wpilib.DigitalInput(map.frontBottomSensor)

        self.MAX_ANGLE = 3 #degrees
        self.climbSpeed = 0.9 #90%
        self.wheelSpeed = 0.9 #90%

        self.backHold = -0.1 #holds back stationary if extended
        self.frontHold = -0.1 #holds front stationary if extended

        self.kP = 0.1 #proportional gain for angle to power

        '''
        NEGATIVE POWER TO ELEVATOR LIFTS ROBOT, LOWERS LEGS
        POSITIVE POWER TO ELEVATOR LOWERS ROBOT, LIFTS LEGS

        NEGATIVE POWER TO WHEELS MOVES ROBOT BACKWARDS
        POSITIVE POWER TO WHEELS MOVES ROBOT FORWARD
        '''

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

    def getLean(self):
        if map.robotId == map.astroV1: return self.robot.drive.getRoll()
        else: return self.robot.drive.getPitch()

    def isLeaning(self, direction):
        '''TRUE TESTS TIPPING FORWARD, FORWARD TIP HAS NEGATIVE ANGLE'''
        if direction==True and self.getLean()<-self.MAX_ANGLE: return True
        elif direction==False and self.getLean()>self.MAX_ANGLE: return True
        else: return False

    def backRetracted(self): return not self.frontSwitch.get()
    def frontRetracted(self): return not self.backSwitch.get()

    def returnCorrectionSpeed(self):
        multiplier = 1 - (self.kP * math.fabs(self.getLean()))
        return (multiplier * self.climbSpeed)

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
        '''FORWARD MOVES ROBOT FORWARD, BACKWARD MOVES ROBOT BACKWARD'''
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

    def wheelForward(self):
        self.wheelLeft.set(self.wheelSpeed)
        self.wheelRight.set(self.wheelSpeed)

    def wheelBack(self):
        self.wheelLeft.set(-1 * self.wheelSpeed)
        self.wheelRight.set(-1 * self.wheelSpeed)

    def stopFront(self):
        if(self.frontRetracted()): self.frontLift.set(0)
        else: self.frontLift.set(self.frontHold)

    def stopBack(self):
        if(self.backRetracted()): self.backLift.set(0)
        else: self.backLift.set(self.backHold)

    def stopDrive(self):
        self.wheelLeft.set(0)
        self.wheelRight.set(0)

    def disable(self):
        self.stopFront()
        self.stopBack()
        self.stopDrive()

    def initDefaultCommand(self):
        self.setDefaultCommand(SetSpeedClimber())

    def dashboardInit(self):
        SmartDashboard.putData("Lift Robot", LiftRobot("both"))
        SmartDashboard.putData("Drive To Edge, Front", DriveToEdge("front"))
        SmartDashboard.putData("Drive To Edge, Back", DriveToEdge("back"))
        SmartDashboard.putData("Lift Robot, Front", LiftRobot("front"))
        SmartDashboard.putData("Lift Robot, Back", LiftRobot("back"))
        SmartDashboard.putData("Lower Robot", LowerRobot("both"))

    def dashboardPeriodic(self):
        SmartDashboard.putNumber("Lean", self.getLean())
