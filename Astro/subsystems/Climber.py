import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
import wpilib.encoder
import ctre

# TODO DETERMINE CONVERSION!!!!
TICKS_TO_INCHES = 1.0




class Climber(Subsystem):
    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Climber')
        self.robot = Robot
        self.debug = True
        self.backLift = ctre.WPI_TalonSRX(0)
        self.frontLift = ctre.WPI_TalonSRX(1)
        self.backWheel1 = ctre.WPI_VictorSPX(2)
        self.backWheel2 = ctre.WPI_VictorSPX(3)
        self.backWheel1.follow(self.backWheel2)
        self.encoder1 = wpilib.Encoder(0,1)
        self.encoder2 = wpilib.Encoder(2,3)
    def subsystemInit(self):
        if self.debug == True:
            SmartDashboard.putData("Ticks on front", self.geHeightFront())
            SmartDashboard.putData("Ticks on back", self.getHeightBack())
        r = self.robot
        climberWheelsForward : wpilib.buttons.JoystickButton = r.operatorButton(7)
        climberWheelsForward.whenPressed(self.wheelForward())
        climberWheelsBackward : wpilib.buttons.JoystickButton = r.operatorButton(8)
        climberWheelsBackward.whenPressed(self.wheelBack())
        frontDeploy : wpilib.joystick = r.opertatoraxis.getY(0)
        frontDeploy : wpilib.joystick

    #gets height
    def getHeightFront(self):
        """this will return the height in inches from encoder
            Pass height to SD
        """
        ticks = self.frontLift.getQuadraturePosition()
        return ticks * TICKS_TO_INCHES
    def getHeightBack(self):
        """this will return the height in inches from encoder
            Pass height to SD
        """
        ticks = self.backLift.getQuadraturePosition()
        return ticks * TICKS_TO_INCHES

    #functions for lift
    def liftFront(self,lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down
        """
        if self.getHeightFront()>=19:
            self.frontLift.set(0)
        else:
            self.frontLift.set(lift)
        if self.getHeightFront()<=0:
            self.frontLift.set(0)
        else:
            self.frontLift.set(lift)
    def liftBack(self,lift):
        """ Basic lift function for lifting robot.
        @param lift - Positive values make lift go down
        """
        if self.getHeightBack()>=19:
            self.backLift.set(0)
        else:
            self.backLift.set(lift)
        if self.getHeightBack()<=0:
            self.backLift.set(0)
        else:
            self.backLift.set(lift)
    #wheel speed
    def wheelForwad(self):
        self.backWheel2.set(0.75)
    def wheelBack(self):
        self.backWheel2.set(-0.75)

    #stopping and disable
    def stopFront(self):
        self.frontLift.set(0)
    def stopBack(self):
        self.backLift.set(0)
    def stopDrive(self):
        self.backWheel2.set(0)
    def disable(self):
        self.stopFront()
        self.stopBack()
        self.stopDrive()

    def dashboardInit(self):
        pass
    def dashboardPeriodic(self):
        pass
