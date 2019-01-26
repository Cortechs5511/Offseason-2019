import wpilib
from wpilib import SmartDashboard
from wpilib.command.subsystem import Subsystem
from wpilib.command import Command
from wpilib import SmartDashboard as sd
import ctre
from ..commands.Wrist import Wrist


class Intake(Command):
    def __init__(self,label,power):
        super().__init__(label)
        robot = self.getRobot()
        self.cargoMech = robot.cargoMech
        self.requires(self.cargoMech)
        self.power = power

    def initialize(self):
        pass

    def execute(self):
        if self.power == -1:
            self.cargoMech.outtake()
        elif self.power == 1:
            self.cargoMech.intake()
        
    def interrupted(self):
        self.cargoMech.stopIntake()

    def end(self):
        self.cargoMech.stopIntake()
    
    def isFinished(self):
        return self.power == 0

class CargoMech(Subsystem):
    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Cargo')
        self.robot = Robot
        #fix
        self.motorIntake = ctre.WPI_TalonSRX(0)
        self.motorWrist = ctre.WPI_TalonSRX(1)
        # Set to true for extra info to smart dashboard
        self.debug = True

    def disable(self):
        self.stopIntake()

    def updateDashboard(self):
        """ Put diagnostics out to smart dashboard. """
        pass

    def intake(self):
        ''' Intake the balls (turn wheels inward) '''
        self.motorIntake.set(0.5)
    def outtake(self):
        ''' Outake the balls (turn wheels outwards) '''
        self.motorIntake.set(-0.5)
    def stopIntake(self):
        ''' Quit intake/outake '''
        self.motorIntake.set(0)
    def wristUp(self):
        '''Move wrist up, make angle bigger'''
        self.motorWrist.set(0.5)
    def wristDown(self):
        '''Move wrist down, make angle smaller: Make sure to stop it at a certain point'''
        self.motorWrist.set(-0.5)
    def wristStop(self):
        '''Stops wrist'''
        self.motorWrist.set(0)

    def subsystemInit(self):
        """ Adds subsystem specific commands. """
        if self.debug == True:
            sd.putData("Intake", Intake('intake',1))
            sd.putData("Outtake",Intake('outtake',-1))
            sd.putData("Stop Inake",Intake('stop',0))
            sd.putData("Wrist up",Wrist('wrist up',1))
            sd.putData("Wrist down",Wrist('wrist down',-1))
            sd.putData("Stop wrist",Wrist('stop wrist',0))
        r = self.robot
        wristUp : wpilib.buttons.JoystickButton = r.operatorButton(4)
        wristUp.whenPressed(Wrist('wrist up',1))
        wristDown : wpilib.buttons.JoystickButton = r.operatorButton(1)
        wristDown.whenPressed(Wrist('wrist down',-1))
        outtakeButton : wpilib.buttons.JoystickButton = r.operatorButton(5)
        outtakeButton.whenPressed(Intake('outtake',-1))
        intakeButton : wpilib.buttons.JoystickButton = r.operatorButton(6)
        intakeButton.whenPressed(Intake('intake',1))