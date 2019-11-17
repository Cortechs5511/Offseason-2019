import wpilib
from wpilib.command import Command
from commandbased import CommandBasedRobot
import subsystems.drive as drive
#from subsystems.drive import Drive
import robotmap

class MyRobot(CommandBasedRobot):

    def robotInit(self):
        Command.getRobot = lambda x=0: self
        self.drive = drive.Drive()
        wpilib.SmartDashboard.putData("DriveSub")

if __name__ == "__main__":
    wpilib.run(MyRobot)
