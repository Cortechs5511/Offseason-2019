import math

import wpilib
from wpilib.command import Command
from wpilib.command import InstantCommand

class Zero(InstantCommand):

    def __init__(self):
        super().__init__('Zero')
        robot = self.getRobot()
        self.cargoMech = robot.cargoMech
        self.hatchMech = robot.hatchMech
        self.requires(robot.cargoMech)
        self.requires(robot.hatchMech)

    def initialize(self):
        self.cargoMech.zero()
        self.hatchMech.zero()

    def interrupted(self):
        pass

    def end(self):
        pass
