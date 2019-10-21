# command based robot
import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot
from subsystems import Drive
from commands.autonomous import Autonomous

class myRobot(CommandBasedRobot):

    def robotInit(self):
        Command.getRobot = lambda x=0: self
        self.drivetrain = Drive.Drive()
        self.Autonomous = Autonomous()

    def autonomousInit(self):
        self.Autonomous.start()

if __name__ == "__main__":
    wpilib.run(myRobot)
