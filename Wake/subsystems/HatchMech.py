from wpilib import SmartDashboard
from wpilib import Solenoid

import map
import oi

class HatchMech():

    def initialize(self):
        self.xbox = oi.getJoystick(2)
        self.piston = Solenoid(map.hatchKick)
        self.kick("in")

    def periodic(self):
        if self.xbox.getRawButton(map.kickHatch) == True: self.kick("out")
        elif self.xbox.getRawButton(map.toggleHatch) == True: self.kick("toggle")

    def kick(self, mode):
        if mode == "in": self.piston.set(True)
        elif mode == "out": self.piston.set(False)
        else:
          self.piston.set(not self.piston.get())

    def isEjectorOut(self):
        return self.piston.get()

    def toggle(self):
        if self.piston.get(): self.kick("in")
        else: self.kick("out")

    def disable(self):
        self.kick("in")

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        pass
