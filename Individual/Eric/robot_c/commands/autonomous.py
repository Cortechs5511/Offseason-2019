import wpilib
from wpilib.command import CommandGroup
from commands.drivefull import DriveFull
from subsystems import Drive
import oi

class Autonomous(CommandGroup): # Nothing works yet.

    def __init__(self):
        super().__init__("Autonomous")
        self.addSequential(DriveFull(power = 0, timeout = 0.35))
        for i in range(0, 40):
            speed = (1)/(1+7*2**-(i/4))
            self.addSequential(DriveFull(power = speed, timeout = 0.02))
        self.addSequential(DriveFull(power = 1, timeout = 1))
        for i in range(0, 130):
            speed = (2)/(1+1.5**(i/20))
            self.addSequential(DriveFull(power = speed, timeout = 0.02))
