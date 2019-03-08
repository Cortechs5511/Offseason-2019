import wpilib
from wpilib import SmartDashboard
import map

class HatchMech():
    def initialize(self):
        self.xbox = map.getJoystick(2)
        self.piston = wpilib.Solenoid(map.hatchKick)
        self.eject("in")

    def periodic(self):
        if self.operator.getRawButton(map.kickHatch) == True: self.kick("out")
        elif self.operator.getRawButton(map.toggleHatch) == True: self.kickToggle()

    def kick(self, mode):
        if mode == "in": self.piston.set(True)
        elif mode == "out": self.piston.set(False)

    def isEjectorOut(self):
        return self.piston.get()

    def toggle(self):
        if self.piston.get(): self.eject("in")
        else: self.eject("out")

    def disable(self):
        self.eject("in")
        self.slide("in")

    def dashboardInit():
        pass

    def dashboardPeriodic():
        pass
