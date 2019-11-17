from wpilib.command import TimedCommand
from subsystems import Drive


class DriveFull(TimedCommand):
    def __init__(self, power, timeout):
        super().__init__("Set Speed %d" % power, timeout)
        self.power = power
        self.requires(self.getRobot().drivetrain)

    def initialize(self):
        Drive.Drive.setSpeed(self.pageDrive(), self.power, self.power)

    def isFinished(self):
        if oi.halfSpeedButton() == True or oi.flipButton() == True:
            return True
        else:
            return False

    def end(self):
        Drive.Drive.setSpeed(self.pageDrive(), 0, 0)
