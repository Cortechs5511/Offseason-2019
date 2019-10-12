import wpilib
from wpilib.command import CommandGroup
from wpilib.command.waitcommand import WaitCommand
from commands.drivestraight import DriveStraight
from subsystems import Drive

class Autonomous(CommandGroup): # Nothing works yet.

    def __init__(self):
        super().__init__("Autonomous")
        self.addSequential(WaitCommand(timeout = 0.2))
        #self.addSequential(Drive.Drive.leftEncoder.getDistance())
        for i in range(0, 20): # 20 iterations, 400 ms accel 0.1 -> 0.8
            speed = (0.8)/(1+7*2**-(i/2)) # logistic function 0.8/1+7*2^-x/2, c = 0.8, a = 7, init. = 0.8, base 2
            self.addSequential(DriveStraight(power = speed, timeout = 0.02))
        self.addSequential(DriveStraight(power = 0.8, timeout = 3))
        for i in range(0, 130): # 130 iterations, 6.5 second decel 0.8 -> 0.1
            speed = (1.6)/(1+1.5**(i/20)) # logistic function 0.8/1+1.5^x/20, c = 1.6, a = 1, init. = 0.8, base 1.5
            self.addSequential(DriveStraight(power = speed, timeout = 0.02))
