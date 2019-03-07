import math

import wpilib
from wpilib.command import Command
from wpilib.command import InstantCommand

class Zero(InstantCommand):

    def __init__(self):
        super().__init__('Zero')
        robot = self.getRobot()
        #self.cargoMech = robot.cargoMech
        #self.hatchMech = robot.hatchMech
        #self.requires(robot.cargoMech)
        #self.requires(robot.hatchMech)
        #self.cargoMech = self.getRobot().cargoMech
        #self.cargoMech = self.getRobot().hatchMech
        #self.requires(self.getRobot().cargoMech)
        #self.requires(self.getRobot().hatchMech)

    def initialize(self):
        #self.cargoMech.zero()
        #self.hatchMech.zero()
        pass

    def interrupted(self):
        pass

    def end(self):
        pass
