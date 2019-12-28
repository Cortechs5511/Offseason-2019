# controls from joysticks
from wpilib.command import Command
from subsystems import Drive
import oi

class joystickDrive(Command):

    def __init__(self):
        super().__init__("Joystick Drive")
        self.requires(self.getRobot().drivetrain)

    def execute(self):
        Drive.Drive.setSpeed(self.pageDrive(), oi.getLeftStick(), oi.getRightStick(), oi.getTurn())
