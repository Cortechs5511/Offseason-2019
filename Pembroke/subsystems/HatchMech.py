from wpilib import SmartDashboard
from wpilib import Solenoid

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

import map
import oi

class HatchMech(Subsystem):
    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Hatch')
        self.debug = True
        self.robot = Robot

    def initialize(self):
        self.xbox = oi.getJoystick(2)
        self.piston = Solenoid(map.hatchKick)
        self.kick("in")

    def periodic(self):
        #self.last = False
        #curr = self.xbox.getRawButton(map.toggleHatch)
        if self.xbox.getRawButton(map.kickHatch) == True: self.kick("out")
        elif self.xbox.getRawButton(map.toggleHatch) == True: self.kick("in")
        '''if curr and curr != self.last:
            self.kick("toggle")
            self.last = curr'''

    def kick(self, mode):
        if mode == "out": self.piston.set(True)
        elif mode == "in": self.piston.set(False)
        else: self.piston.set(not self.piston.get())

    def isEjectorOut(self): return self.piston.get()

    def toggle(self):
        if self.piston.get(): self.kick("out")
        else: self.kick("in")

    def disable(self): self.kick("in")

    def dashboardInit(self): pass

    def dashboardPeriodic(self): pass

class EjectHatch(Command):
    def __init__(self):
        super().__init__('EjectHatch')
        robot = self.getRobot()
        self.hatch = robot.hatch
        self.requires(self.hatch)

    def initialize(self): pass

    def execute(self): self.hatch.kick("out")

    def isFinished(self): return self.timeSinceInitialized()>0.25

    def interrupted(self): pass

    def end(self): self.hatch.kick("in")
