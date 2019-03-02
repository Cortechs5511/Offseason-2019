'''import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib.command import CommandGroup
from commands.climber import driveToEdge
from commands.climber import liftRobot
from commands.drive import setFixedDT

class AutoClimb(CommandGroup):
    def __init__(self):
        super().__init__('AutoClimb')
        self.addSequential(liftRobot.LiftRobot("both"))
        self.addSequential(driveToEdge.DriveToEdge("front"))
        self.addSequential(liftRobot.LiftRobot("front"))
        self.addSequential(driveToEdge.DriveToEdge("back"))
        self.addSequential(liftRobot.LiftRobot("back"))
        # time units is in milliseconds
        self.addSequential(setFixedDT.SetFixedDT(0.5, 0.5, 200))'''
