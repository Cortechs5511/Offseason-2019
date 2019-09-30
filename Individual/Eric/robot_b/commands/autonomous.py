import wpilib
from wpilib.command import CommandGroup
from wpilib.command.waitcommand import WaitCommand
from subsystems import Drive
from commands.setspeedagain import SetSpeed

class Autonomous(CommandGroup): # Nothing works yet.

    def __init__(self):
        super().__init__("Autonomous")
        self.addSequential(WaitCommand(timeout = 1))
        self.addSequential(SetSpeed(power = 0.85, timeout = 0.5))
