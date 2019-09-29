from wpilib.command import TimedCommand
from subsystems import Drive

class SetSpeed(TimedCommand):

    def __init__(self, power, timeout):
        super().__init__("Set Speed %d" % power, timeout)

        self.power = power
        self.requires(self.getRobot().drivetrain)

    def initialize(self):
        Drive.Drive.setSpeed(self.pageDrive(), power, power)

    def end(self):
        self.getRobot().motor.setSpeed(0)
