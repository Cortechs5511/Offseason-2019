# controls from joysticks
from wpilib.command import Command
from subsystems import Drive
import oi

class joystickDrive(Command):

    def __init__(self):
        super().__init__("Joystick Drive")
        self.requires(self.getRobot().drivetrain)

    def execute(self):
        leftInput = self.getRobot().leftStick.getY()
        rightInput = self.getRobot().rightStick.getY()
        if abs(leftInput) >= 0.05:
            leftOutput = float(leftInput) * 0.9
        else:
            leftOutput = 0
        if abs(rightInput) >= 0.05:
            rightOutput = float(rightInput) * 0.9
        else:
            rightOutput = 0
        Drive.Drive.setSpeed(self.pageDrive(), leftOutput, rightOutput)
