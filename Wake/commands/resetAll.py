import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand

from subsystems import HatchMech
from subsystems import CargoMech
from subsystems import Climber

from commandbased import CommandBasedRobot

class ResetAll(CommandBasedRobot):

    def __init__(self):
        super().__init__('ResetAll')
        self.requires(self.getRobot().hatch)
        self.requires(self.getRobot().climber)
        self.DT = self.getRobot().drive

    def initialize(self):
        pass
    def execute(self):
        #reset hatches
        self.HatchMech.retractEjector()
        self.HatchMech.slidein()
        self.Climber.lowerRobot()

    def isFinished(self):
        pass

    def interrupted(self):
        self.disable()

    def disable(self):
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)
