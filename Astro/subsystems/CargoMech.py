import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
from wpilib import SmartDashboard as sd

class IntakeCargo(Command):
    def __init__(self):
        super().__init__('IntakeCargo')
        robot = self.getRobot()
        self.cargoMech = robot.cargoMech
        self.requires(self.cargoMech)
         
    def initialize(self):
        pass

    def execute(self):
        self.cargoMech.intake()
        
    def interrupted(self):
        self.cargoMech.stopIntake()

    def end(self):
        self.cargoMech.stopIntake()
    
    def isFinished(self):
        return False

class CargoMech(Subsystem):
    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Cargo')
        # Set to true for extra info to smart dashboard
        self.debug = True


    def disable(self):
        self.stopIntake()

    def updateDashboard(self):
        """ Put diagnostics out to smart dashboard. """
        sd.putData("Intake", IntakeCargo())
        sd.putData("Cargo Mech", self)

    def subsystemInit(self):
        """ Adds subsystem specific commands. """
        pass
    def intake(self):
        ''' Intake the balls (turn wheels inward) '''
        pass
    def outake(self):
        ''' Outake the balls (turn wheels outwards) '''
        pass
    def stopIntake(self):
        ''' Quit intake/outake '''
        
        pass
    
