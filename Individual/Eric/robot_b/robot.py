# deprecated command based robot
import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot
import oi
from subsystems import Drive
from commands.autonomous import Autonomous

class MyRobot(CommandBasedRobot):

    def robotInit(self):
        Command.getRobot = lambda x=0: self
        MyRobot.drivetrain = Drive.Drive()
        MyRobot.leftStick = oi.getLeftStick()
        MyRobot.rightStick = oi.getRightStick()
        self.Autonomous = Autonomous()

    def autonomousInit(self):
        self.Autonomous.start()

if __name__ == "__main__":
    wpilib.run(MyRobot)
