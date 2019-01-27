import math
import wpilib
import oi

from wpilib import SmartDashboard
import wpilib.buttons

from wpilib.command import Command
from commandbased import CommandBasedRobot

from commands.zero import Zero

from commands import sequences

from commands import autonomous
from commands.autonomous import TestPath
from commands.autonomous import DriveStraight

from subsystems import HatchMech
from subsystems import CargoMech
from subsystems import Climber
from subsystems import Drive
from subsystems import Limelight

from CRLibrary.path import odometry as od


import rate

class MyRobot(CommandBasedRobot):

    dashboard = True
    follower = "Ramsetes"

    def robotInit(self):

        '''
        This is a good place to set up your subsystems and anything else that
        you will need to access later.
        '''

        Command.getRobot = lambda x=0: self

        self.limelight = Limelight.Limelight(self)
        self.hatchMech = HatchMech.HatchMech(self)
        self.cargoMech = CargoMech.CargoMech(self)
        self.climber = Climber.Climber(self)
        self.drive = Drive.Drive(self)

        self.timer = wpilib.Timer()
        self.timer.start()

        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''

        [self.joystick0, self.joystick1, self.xbox] = oi.commands()

        self.rate = rate.DebugRate()
        self.rate.initialize()

        if(self.dashboard): self.updateDashboardInit()

        self.TestPath = TestPath(self.follower)
        self.DriveStraight = DriveStraight()

    def robotPeriodic(self):
        self.limelight.readLimelightData()
        if(self.dashboard): self.updateDashboardPeriodic()

    def autonomousInit(self):
        self.drive.zero()
        self.timer.reset()
        self.timer.start()
        self.curr = 0

        self.autoMode = "TestPath" #self.autoMode = "DriveStraight"
        if self.autoMode == "DriveStraight": self.DriveStraight.start()
        elif self.autoMode == "TestPath": self.TestPath.start()

    def updateDashboardInit(self):
        SmartDashboard.putData("Drive", self.drive)
        SmartDashboard.putData("Hatch", self.hatchMech)
        SmartDashboard.putData("Cargo", self.cargoMech)
        SmartDashboard.putData("Climber", self.climber)

        self.drive.dashboardInit()
        self.hatchMech.dashboardInit()
        self.cargoMech.dashboardInit()
        self.climber.dashboardInit()

        SmartDashboard.putData("Zero", Zero())

        sequences.dashboardInit()
        autonomous.dashboardInit()

        self.limelight.dashboardInit()

    def updateDashboardPeriodic(self):
        self.rate.execute()

        self.drive.dashboardPeriodic()
        self.hatchMech.dashboardPeriodic()
        self.cargoMech.dashboardPeriodic()
        self.climber.dashboardPeriodic()

        sequences.dashboardPeriodic()
        autonomous.dashboardPeriodic()

        self.limelight.dashboardPeriodic()

    def disabledInit(self):
        self.drive.disable()
        self.hatchMech.disable()
        self.cargoMech.disable()
        self.climber.disable()

    def disabledPeriodic(self):
        self.disabledInit()

    #I think the below should go in oi.py somehow, but I'm lazy tonight - Abhijit
    '''
    def driverLeftButton(self, id):
        """ Return a button off of the left driver joystick that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.joystick0, id)

    def driverRightButton(self, id):
        """ Return a button off of the right driver joystick that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.joystick1, id)

    def operatorButton(self, id):
        """ Return a button off of the operator gamepad that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.xbox, id)
    '''

if __name__ == "__main__":
    wpilib.run(MyRobot)
