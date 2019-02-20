import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib.command import CommandGroup
from commands.climber import driveToEdge



class AutoClimb(CommandGroup):
    def __init__(self):
        self.LiftRobot = liftRobot.LiftRobot
        self.DriveToEdge = driveToEdge.DriveToEdge
        self.addSequential(LiftRobot("both"))
        self.addSequential(self.DriveToEdge("front"))
        self.addSequential(self.LiftRobot("front"))
        self.addSequential(self.DriveToEdge("back"))
        self.addSequential(self.LiftRobot("back"))
        # time units is in milliseconds
        self.addSequential(self.commands.drive.setFixedDT.SetFixedDT(0.5, 0.5, 200))
