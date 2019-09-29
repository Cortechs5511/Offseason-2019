# controls from joysticks
from wpilib.command import Command
from subsystems import Drive
import oi

class joystickDrive(Command):

    def __init__(self):
        super().__init__("Joystick Drive")
        self.requires(self.getRobot().drivetrain)

    def execute(self):
        if abs(self.getRobot().leftStick.getY()) >= 0.05:
            leftInput = float(self.getRobot().leftStick.getY()) * 0.9
        else:
            leftInput = 0
        if abs(self.getRobot().rightStick.getY()) >= 0.05:
            rightInput = float(self.getRobot().rightStick.getY()) * 0.9
        else:
            rightInput = 0
        Drive.Drive.setSpeed(self.pageDrive(), leftInput, rightInput)
