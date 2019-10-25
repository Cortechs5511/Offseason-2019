import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot
from subsystems import Drive
from commands.autonomous import Autonomous


class MyRobot(CommandBasedRobot):
    def robotInit(self):
        Command.getRobot = lambda x=0: self
        self.drivetrain = Drive.Drive()
        self.autonomous = Autonomous()

    def autonomousInit(self):
        self.autonomous.start()

if __name__ == "__main__":
    wpilib.run(MyRobot)
