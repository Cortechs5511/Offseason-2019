import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

from commands.hatch.ejectToggle import EjectToggle
from commands.hatch.ejectHatch import EjectHatch
from commands.hatch.slideToggle import SlideToggle

class HatchMech(Subsystem):
    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Hatch')
        self.debug = True
        self.robot = Robot

        #Normally the ejectPiston would be on solenoid 1, but was changed to see if slide worked.
        self.ejectPiston = wpilib.Solenoid(1)
        self.ejectPistonSlide = wpilib.Solenoid(0)
        self.ejectPiston.setName("Hatch" , "Ejector")
        self.ejectPistonSlide.setName("Hatch" , "Slider")

    def isEjectorOut(self):
        """ Returns True when ejector is sticking out. """
        return self.ejectPiston.get()

    def ejectHatch(self):
        """ Use this method to throw hatch onto docking surface. """
        self.ejectPiston.set(True)

    def retractEjector(self):
        """ Pulls the ejector back in. """
        self.ejectPiston.set(False)

    def slideOut(self):
        """ Slides hatch mechanism out over bumpers. """
        self.ejectPistonSlide.set(True)

    def slideIn(self):
        """ Pulls hatch mechanism back in. """
        self.ejectPistonSlide.set(False)

        """ says if the slide is in or not """
    def isSlideIn(self):
        return self.ejectPistonSlide.get()

    def subsystemInit(self):
        """ Adds subsystem specific commands. """
        if self.debug:
            SmartDashboard.putData("Eject Hatch", EjectHatch())
            SmartDashboard.putData("Hatch Mech", self)
            SmartDashboard.putData("Ejector Toggle" , EjectToggle())
        self.retractEjector()
        r = self.robot
        b : wpilib.buttons.JoystickButton = r.operatorButton(3)
        b.whenPressed(EjectHatch())
        b : wpilib.buttons.JoystickButton = r.operatorButton(5)
        b.whenPressed(EjectToggle())
        b : wpilib.buttons.JoystickButton = r.operatorButton(6)
        b.whenPressed(SlideToggle())

    def disable(self):
        self.retractEjector()
        self.slideIn()

    def dashboardInit(self):
        pass

    def dashboardPeriodic(self):
        if self.debug:
            SmartDashboard.putBoolean("EjectorOut", self.isEjectorOut())
            SmartDashboard.putBoolean("SlideOut",self.isSlideIn ())
