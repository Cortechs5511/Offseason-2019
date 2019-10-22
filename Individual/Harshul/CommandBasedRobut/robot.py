import wpilib
from commandbased import CommandBasedRobot
import subsystems.drive
#from subsystems.drive import Drive
import robotmap

class MyRobot(CommandBasedRobot):

    def robotInit(self):
        Command.getRobot = lambda x=0: self
        self.drive = drive.Drive()
