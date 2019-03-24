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
        self.kicker = Solenoid(map.hatchKick)
        self.slider = Solenoid(map.hatchSlide)
        self.kick("in")
        self.slide("in")

    def periodic(self):
        #self.last = False
        #curr = self.xbox.getRawButton(map.toggleHatch)
        if self.xbox.getRawButton(map.kickHatch) == True: self.kick("out")
        elif self.xbox.getRawButton(map.toggleHatch) == True: self.kick("in")

        if self.xbox.getRawButton(map.extendHatch) == True: self.slide("out")
        elif self.xbox.getRawButton(map.retractHatch) == True: self.slide("in")
        '''if curr and curr != self.last:
            self.kick("toggle")
            self.last = curr'''

    def kick(self, mode):
        if mode == "out": self.kicker.set(True)
        elif mode == "in": self.kicker.set(False)
        else: self.kicker.set(not self.kicker.get())

    def slide(self, mode):
        if mode == "out": self.slider.set(True)
        elif mode == "in": self.slider.set(False)
        else: self.kicker.set(not self.slider.get())

    def isEjectorOut(self): return self.kicker.get()

    def toggle(self):
        if self.kicker.get(): self.kick("out")
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
