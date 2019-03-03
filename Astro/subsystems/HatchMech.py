import wpilib
from wpilib import SmartDashboard
import map
import oi

class HatchMech():
    def __init__(self, Robot):
        self.robot = Robot
        self.operator = oi.getJoystick(2)
        #Normal1ly the ejectPiston would be on solenoid 1, but was changed to see if slide worked.
        self.ejectPiston = wpilib.Solenoid(map.hatchKick)
        self.ejectPistonSlide = wpilib.Solenoid(map.hatchSlide)
        self.ejectPiston.setName("Hatch" , "Ejector")
        self.ejectPistonSlide.setName("Hatch" , "Slider")

        self.eject("in")

    def hatchPeriodic(self):
        if self.operator.getRawButton(3) == True:
            self.eject("out")
        elif self.operator.getRawButton(7) == True:
            self.ejectToggle()
        elif self.operator.getRawButton(8) == True:
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
