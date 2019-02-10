import wpilib
from wpilib import SmartDashboard

from wpilib.command.subsystem import Subsystem
from wpilib.command import Command

import ctre

from commands.cargo.wristIntake import WristIntake
from commands.cargo.wristMove import WristMove
import map

class CargoMech(Subsystem):

    def __init__(self, Robot):
        """ Create all physical parts used by subsystem. """
        super().__init__('Cargo')

        self.debug = True
        self.robot = Robot

        #fix
        self.motorIntake = ctre.WPI_TalonSRX(map.intake)
        self.motorWrist = ctre.WPI_TalonSRX(map.wrist)

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

    def dashboardInit(self):
        """ Adds subsystem specific commands. """
        if self.debug == True:
            SmartDashboard.putData("Intake", WristIntake('intake',1))
            SmartDashboard.putData("Outtake",WristIntake('outtake',-1))
            SmartDashboard.putData("Stop Inake",WristIntake('stop',0))
            SmartDashboard.putData("Wrist up",WristMove('wrist up',1))
            SmartDashboard.putData("Wrist down",WristMove('wrist down',-1))
            SmartDashboard.putData("Stop wrist",WristMove('stop wrist',0))

    def subsystemInit(self):
        r = self.robot
        wristUp : wpilib.buttons.JoystickButton = r.operatorButton(4)
        wristUp.whileActive(WristMove('wrist up',1))
        wristDown : wpilib.buttons.JoystickButton = r.operatorButton(1)
        wristDown.whileActive(WristMove('wrist down',-1))
        outtakeButton : wpilib.buttons.JoystickButton = r.operatorButton(5)
        outtakeButton.whileActive(WristIntake('outtake',-1))
        intakeButton : wpilib.buttons.JoystickButton = r.operatorButton(6)
        intakeButton.whileActive(WristIntake('intake',1))

    def disable(self):
        self.stopIntake()
    def dashboardPeriodic(self):
        pass
