from wpilib.command import CommandGroup
from commands.drive.drivedistance import DriveDistance


class Autonomous(CommandGroup):
    def __init__(self):
        super().__init__("Autonomous")
        self.addSequential(DriveDistance(distance = 79.7, power = 0.7))
