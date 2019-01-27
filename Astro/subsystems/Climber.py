import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

import ctre

class Climber(Subsystem):

    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Climber')
        self.robot = Robot
        self.debug = True

    def disable(self):
        pass

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        pass
