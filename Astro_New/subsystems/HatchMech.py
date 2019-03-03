import wpilib
from wpilib import SmartDashboard
import map

class HatchMech():
    def hatchInit(self):
        self.operator = map.getJoystick(2)
        self.ejectPiston = wpilib.Solenoid(map.hatchKick)
        self.ejectPistonSlide = wpilib.Solenoid(map.hatchSlide)
        self.ejectPiston.setName("Hatch" , "Ejector")
        self.ejectPistonSlide.setName("Hatch" , "Slider")
        self.eject("in")

    def hatchPeriodic(self):
        if self.operator.getRawButton(map.KickSimpleHatch) == True:
            self.eject("out")
        elif self.operator.getRawButton(map.ToggleSimpleHatch) == True:
            self.ejectToggle()
        elif self.operator.getRawButton(map.ToggleNewHatch) == True:
            self.slideToggle()

    def eject(self, mode):
        """ Use this method to throw hatch onto docking surface. """
        if mode == "in":
            self.ejectPiston.set(True)
        elif mode == "out":
            self.ejectPiston.set(False)

    def slide(self, mode):
        """ Slides hatch mechanism out over bumpers. """
        if mode == "in":
            self.ejectPistonSlide.set(True)
        elif mode == "out":
            self.ejectPistonSlide.set(False)

    def isEjectorOut(self):
        return self.ejectPiston.get()

    def ejectToggle(self):
        ejectorOut = self.isEjectorOut()
        if ejectorOut:
            self.eject("in")
        else:
            self.eject("out")

    def isSlideIn(self):
        return self.ejectPistonSlide.get()

    def disable(self):
        self.eject("in")
        self.slide("in")

    def slideToggle(self):
        slideOut = self.isSlideIn()
        if slideOut:
            self.slide("in")
        else:
            self.slide("out")

    def dashboardPeriodic():
        pass
