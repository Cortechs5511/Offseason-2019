# command based robot
import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot
import oi
from subsystems import Drive
from commands.autonomous import Autonomous

class myRobot(CommandBasedRobot):

    def robotInit(self):
        Command.getRobot = lambda x=0: self
        self.drivetrain = Drive.Drive()
        self.leftStick = oi.getLeftStick()
        self.rightStick = oi.getRightStick()
        

    def autonomousInit(self):
        self.autonomousProgram = Autonomous()

if __name__ == "__main__":
    wpilib.run(myRobot)
