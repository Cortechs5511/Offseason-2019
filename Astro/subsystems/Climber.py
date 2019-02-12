import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
import wpilib.encoder
import ctre
import map
from commands.climber.liftRobot import LiftRobot
from commands.climber.lowerRobot import LowerRobot
from commands.climber.setSpeedWheel import SetSpeedWheel
# TODO DETERMINE CONVERSION!!!!
TICKS_TO_INCHES = 1.0
MAX_EXTEND = 12.0

class Climber(Subsystem):
    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Climber')
        self.robot = Robot
        self.debug = True

        self.backLift = ctre.WPI_TalonSRX(map.backLift)
        self.frontLift = ctre.WPI_TalonSRX(map.frontLift)
        self.wheelLeft = ctre.WPI_VictorSPX(map.wheelLeft)
        self.wheelRight = ctre.WPI_VictorSPX(map.wheelRight)

        self.climberLock = wpilib.DoubleSolenoid(map.climberLock1 , map.climberLock2)

        self.backLift.setNeutralMode(2)
        self.frontLift.setNeutralMode(2)
        self.wheelLeft.setNeutralMode(2)
        self.wheelRight.setNeutralMode(2)

        self.backLift.setName("Climber" , "BackLift")
        self.frontLift.setName("Climber" , "FrontLift")
        self.wheelLeft.setName("Climber" , "Wheels")
        self.climberLock.setName("Climber" , "Lock")

        SmartDashboard.putNumber("Climber Speed", 0.25)

    def dashboardInit(self):
        SmartDashboard.putData("Lift Robot", LiftRobot())

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

    def getPitch(self):
        return self.robot.drive.pitch

    def getHeightFront(self):
        """
        this will return the height in inches from encoder
        Pass height to SD
        """

        ticks = self.frontLift.getQuadraturePosition()
        return ticks * TICKS_TO_INCHES

    def getHeightBack(self):
        """
        this will return the height in inches from encoder
        Pass height to SD
        """

        ticks = self.backLift.getQuadraturePosition()
        return ticks * TICKS_TO_INCHES

    def isFullyExtendedFront(self):
        """
        tells us if the front is fully extended
        """

        return self.getHeightFront() >= MAX_EXTEND

    def isFullyExtendedBack(self):
        """tells us if the back is fully extended, so it can stop"""
        return self.getHeightBack() >= MAX_EXTEND

    def isFullyExtendedBoth(self):
        """tells us if both front and back are fully extended, so it can stop"""
        return self.isFullyExtendedFront() and self.isFullyExtendedBack()

    #functions for lift
    def liftFront(self,lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down(extend)
        """
        if lift > 0 and self.getHeightFront()>=MAX_EXTEND:
            self.frontLift.set(0)
        elif lift < 0 and self.getHeightFront() < 0:
            self.frontLift.set(0)
        else:
            self.frontLift.set(lift)

    def liftBack(self,lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down
        """
        if  lift > 0 and self.getHeightBack()>=MAX_EXTEND:
            self.backLift.set(0)

        elif lift < 0 and self.getHeightBack()<0:
            self.backLift.set(0)
        else:
            self.backLift.set(lift)

    #wheel speed
    def wheelForward(self):
        self.wheelLeft.set(0.75)
        self.wheelRight.set(0.75)

    def wheelBack(self):
        self.wheelLeft.set(-0.75)
        self.wheelRight.set(-0.75)

    #stopping and disable
    def stopFront(self):
        self.frontLift.set(0)

    def stopBack(self):
        self.backLift.set(0)

    def stopDrive(self):
        self.wheelLeft.set(0)
        self.wheelRight.set(0)

    def disable(self):
        self.stopFront()
        self.stopBack()
        self.stopDrive()

    def dashboardPeriodic(self):
        if self.debug == True:
            SmartDashboard.putNumber("Ticks on front", self.getHeightFront())
            SmartDashboard.putNumber("Ticks on back", self.getHeightBack())

    def returnClimbSpeed(self):
        self.climbSpeed = SmartDashboard.getNumber("Climber Speed", 0.25)
        return self.climbSpeed
