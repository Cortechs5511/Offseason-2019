import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
from wpilib import SmartDashboard as sd

class EjectHatch(Command):
    def __init__(self):
        super().__init__('HatchEject')
        robot = self.getRobot()
        self.hatchMech = robot.hatchMech
        self.requires(self.hatchMech)
         
    def initialize(self):
        pass

    def execute(self):
         self.hatchMech.ejectHatch()
         

    def isFinished(self):
        return self.timeSinceInitialized()>3

    def interrupted(self):
        pass

    def end(self):
         self.hatchMech.retractEjector()




class EjectToggle(Command):
    def __init__(self):
        super().__init__('toggleHatch')
        robot = self.getRobot()
        self.hatchMech = robot.hatchMech
        self.requires(self.hatchMech)

    def initialize(self):
        pass

    def execute(self):
        isEjectorOut = True
        # if EjectHatch(true)
            

         

    def isFinished(self):
        return True

    def interrupted(self):
        pass

    def end(self):
         self.hatchMech.retractEjector()
#    """ JACOB Make this command toggle between eject in/out. """
    


class HatchMech(Subsystem):
    """ Controls the handling of hatches.

    Expects pistons that we use to eject hatch onto docking surface.
    Also has slider mechanism that can move back and forth.
    """

    def __init__(self, robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Hatch')
        # Set to true for extra info to smart dashboard
        self.debug = True
        self.robot = robot
        self.ejectPiston = wpilib.Solenoid(0)
        self.ejectPistonSlide = wpilib.Solenoid(1)
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
    
    def disable(self):
        """ Disables subsystem and puts everything back to starting position. """
        self.retractEjector()
        self.slideIn()

    def updateDashboard(self):
        """ Put diagnostics out to smart dashboard. """
        SmartDashboard.putBoolean("Ejector Out", self.isEjectorOut())
        SmartDashboard.putBoolean("Slide Out",self.isSlideIn ())
       # SmartDashboard.putBoolean("Ejector Toggle" , EjectToggle())

    def subsystemInit(self):
        """ Adds subsystem specific commands. """
        if self.debug:
            SmartDashboard.putData("Eject Hatch", EjectHatch())
            SmartDashboard.putData("Hatch Mech", self)
        self.retractEjector()
        r = self.robot
        b : wpilib.buttons.JoystickButton = r.operatorButton(3)
        b.whenPressed(EjectHatch())
