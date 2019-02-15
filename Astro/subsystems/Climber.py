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
from commands.climber.frontClimb import FrontClimb
from commands.climber.backClimb import BackClimb

import map

class Climber(Subsystem):

    # TODO DETERMINE CONVERSION!!!!
    TICKS_TO_INCHES = 1.0 #inches/tick
    MAX_EXTEND = 12.0 #inches

    #MAX_PITCH = 5 #degrees

    climbSpeed = 0.25

    def __init__(self, robot):
        super().__init__('Climber')

        self.robot = robot
        self.debug = True

        timeout = 0

        self.backLift = Talon(map.backLift)
        self.frontLift = Talon(map.frontLift)
        self.wheelLeft = Victor(map.wheelLeft)
        self.wheelRight = Victor(map.wheelRight)
        self.switchTopFront = wpilib.DigitalInput(4)
        self.switchBottomFront = wpilib.DigitalInput(5)
        self.switchTopBack = wpilib.DigitalInput(6)
        #self.switchBottomBack = wpilib.DigitalInput(3)

        self.wheelRight.follow(self.wheelLeft)
        self.wheels = self.wheelLeft

        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)

        for motor in [self.backLift, self.frontLift, self.wheelLeft, self.wheelRight]:
            motor.clearStickyFaults(timeout)
            motor.setSafetyEnabled(False)
            motor.setInverted(False)

        for motor in [self.backLift, self.frontLift]:
            motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
            motor.enableCurrentLimit(True)

            motor.configVoltageCompSaturation(9,timeout) #Sets saturation value
            motor.enableVoltageCompensation(True) #Compensates for lower voltages

        self.MAX_PITCH = self.returnTolerance()

    def subsystemInit(self):
        r = self.robot

        climberWheelsForward : wpilib.buttons.JoystickButton = r.driverLeftButton(7)
        climberWheelsForward.whileHeld(SetSpeedWheel(1))

        climberWheelsBackward : wpilib.buttons.JoystickButton = r.driverLeftButton(8)
        climberWheelsBackward.whileHeld(SetSpeedWheel(-1))

        liftButton : wpilib.buttons.JoystickButton = r.driverLeftButton(9)
        liftButton.whileHeld(LiftRobot())

        liftButton : wpilib.buttons.JoystickButton = r.driverLeftButton(10)
        liftButton.whileHeld(LowerRobot())

        climberFrontUp : wpilib.buttons.JoystickButton = r.driverLeftButton(13)
        climberFrontUp.whileHeld(FrontClimb(True))

        climberFrontDown : wpilib.buttons.JoystickButton = r.driverLeftButton(14)
        climberFrontDown.whileHeld(FrontClimb(False))

        climberBackUp : wpilib.buttons.JoystickButton = r.driverLeftButton(12)
        climberBackUp.whileHeld(BackClimb(True))

        climberBackDown : wpilib.buttons.JoystickButton = r.driverLeftButton(15)
        climberBackDown.whileHeld(BackClimb(False))

    def getPitch(self):
        return self.robot.drive.pitch #negate here if pitch is backwards of expected

    def getRoll(self):
        return self.robot.drive.roll

    def getHeightFront(self):
        """ this will return the height in inches from encoder """
        #ticks = self.frontLift.getQuadraturePosition()
        #return ticks * self.TICKS_TO_INCHES
        return 0 #temp

    def getHeightBack(self):
        """ this will return the height in inches from encoder """
        #ticks = self.backLift.getQuadraturePosition()
        #return ticks * self.TICKS_TO_INCHES
        return 0 #temp

    def isFullyExtendedFront(self):
        """ tells us if the front is fully extended """
        #return self.getHeightFront() >= self.MAX_EXTEND
        return self.switchTopFront.get()

    def isFullyExtendedBack(self):
        """ tells us if the back is fully extended, so it can stop """
        #return self.getHeightBack() >= self.MAX_EXTEND
        return self.switchTopBack.get()

    def isFullyUnextendedFront(self):
        return self.switchBottomFront.get()

    def isFullyUnextendedBack(self):
        #return self.switchBottomBack.get()
        return False

    def isFullyExtendedBoth(self):
        """ tells us if both front and back are fully extended, so it can stop """
        return self.isFullyExtendedFront() and self.isFullyExtendedBack()

    #functions for lift
    def liftFront(self, lift, tol=True, oppadjust=False):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down(extend) """

        if isFullyExtendedFront() and lift/abs(lift) == 1 : self.stopFront()
        elif isFullyUnextendedFront() and lift/abs(lift) == -1 : self.stopFront()
        elif oppadjust and lift/abs(lift)*self.getRoll()>self.MAX_PITCH: self.liftBack(0.5)
        elif tol and lift/abs(lift)*self.getRoll()>self.MAX_PITCH: self.stopFront()
        else: self.frontLift.set(1.1*lift)

    def liftBack(self, lift, tol=True):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down """

        if isFullyExtendedBack() and lift/abs(lift) == 1 : self.stopBack()
        elif isFullyUnextendedBack() and lift/abs(lift) == -1 : self.stopBack()
        elif tol and lift/abs(lift)*self.getRoll()<-self.MAX_PITCH: self.stopBack()
        else: self.backLift.set(lift)

    def lift(self, lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down(extend) """

        self.liftFront(lift)
        self.liftBack(lift)

    #wheel speed
    def wheelForward(self): self.wheels.set(self.returnClimbSpeed())
    def wheelBack(self): self.wheels.set(-1 * self.returnClimbSpeed())

    def stopFront(self): self.frontLift.set(0)
    def stopBack(self): self.backLift.set(0)

    def stop(self):
        self.stopFront()
        self.stopBack()

    def stopDrive(self): self.wheels.set(0)

    def disable(self):
        self.stopFront()
        self.stopBack()
        self.stopDrive()

    def dashboardInit(self):
        SmartDashboard.putNumber("ClimberSpeed", 1)
        SmartDashboard.putNumber("Tolerance", 2)
        SmartDashboard.putData("Lift Robot", LiftRobot())
        SmartDashboard.putData("Lower Robot", LowerRobot())

    def dashboardPeriodic(self):
        if self.debug == True:
            SmartDashboard.putNumber("Pitch", self.getPitch())
            SmartDashboard.putNumber("FrontTicks", self.getHeightFront())
            SmartDashboard.putNumber("BackTicks", self.getHeightBack())

    def returnClimbSpeed(self):
        self.climbSpeed = SmartDashboard.getNumber("ClimberSpeed", 0.9)
        return self.climbSpeed

    def returnTolerance(self):
        self.tolerance = SmartDashboard.getNumber("Tolerance", 2)
        return self.tolerance
