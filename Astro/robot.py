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

from commands.drive.drivePath import DrivePath
from commands.drive.align import Align

from subsystems import HatchMech
from subsystems import CargoMech
from subsystems import Climber
from subsystems import Drive
from subsystems import Limelight
from robotpy_ext.misc import looptimer
from CRLibrary.path import odometry as od


import rate

class MyRobot(CommandBasedRobot):

    dashboard = True
    follower = "Ramsetes"

    frequency = 20
    period = 1/frequency

    def __init__(self):
        super().__init__(self.period)

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

       # if(self.dashboard): self.updateDashboardInit()
        self.updateDashboardInit()

        self.hatchMech.subsystemInit()
        self.cargoMech.subsystemInit()
        self.climber.subsystemInit()

        self.DrivePath = DrivePath(name="AlignBack", follower="Ramsetes")

    def teleopInit(self):
        self.loop_timer = looptimer.LoopTimer(self.logger)

    def teleopPeriodic(self):
        super().teleopPeriodic()
        self.loop_timer.measure()

    def robotPeriodic(self):
        #self.drive.odMain.display()
        self.drive.odTemp.display()

        #self.limelight.readLimelightData()
        if(self.dashboard): self.updateDashboardPeriodic()

    def autonomousInit(self):
        self.drive.zero()
        self.timer.reset()
        self.timer.start()
        self.curr = 0

        #[x,y] = self.limelight.getPathXY()
        #[x,y] = [-10, 0]
        self.DrivePath.start()
        #self.Align.start(x,y)

        '''
        self.autoMode = "TestPath" #self.autoMode = "DriveStraight"
        if self.autoMode == "DriveStraight": self.DriveStraight.start()
        elif self.autoMode == "TestPath": self.TestPath.init()
        '''

    def updateDashboardInit(self):
        #SmartDashboard.putData("Drive", self.drive)
        #SmartDashboard.putData("Hatch", self.hatchMech)
        #SmartDashboard.putData("Cargo", self.cargoMech)
        #SmartDashboard.putData("Climber", self.climber)

        self.drive.dashboardInit()
        #self.hatchMech.dashboardInit()
        #self.cargoMech.dashboardInit()
        #self.climber.dashboardInit()
        #self.limelight.dashboardInit()

        sequences.dashboardInit()
        autonomous.dashboardInit()

        SmartDashboard.putData("Zero", Zero())

    def updateDashboardPeriodic(self):
        self.rate.execute()
        #self.drive.dashboardPeriodic()
        #self.hatchMech.dashboardPeriodic()
        #self.cargoMech.dashboardPeriodic()
        #self.climber.dashboardPeriodic()
        #self.limelight.dashboardPeriodic()

        sequences.dashboardPeriodic()
        autonomous.dashboardPeriodic()

    def disabledInit(self):
        self.drive.disable()
        self.hatchMech.disable()
        self.cargoMech.disable()
        self.climber.disable()

    def disabledPeriodic(self):
        self.disabledInit()

    #I think the below should go in oi.py somehow, but I'm lazy tonight - Abhijit

    def driverLeftButton(self, id):
        """ Return a button off of the left driver joystick that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.joystick0, id)

    def driverRightButton(self, id):
        """ Return a button off of the right driver joystick that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.joystick1, id)

    def operatorButton(self, id):
        """ Return a button off of the operator gamepad that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.xbox, id)

    def operatorAxis(self,id):
        """ Return a Joystick off of the operator gamepad that we want to map a command to. """
        #id is axis channel for taking value of axis
        return self.xbox.getRawAxis(id)
        #wpilib.joystick.setAxisChannel(self.xbox, id)
    def readOperatorButton(self,id):
        """ Return button value """
        return self.xbox.getRawButton(id)

    def readDriverRightButton(self,id):
        """ Return button value from right joystick """
        return self.joystick1.getRawButton(id)

    def readDriverLeftButton(self,id):
        """ Return button value from left joystick """
        return self.joystick0.getRawButton(id)




if __name__ == "__main__":
    wpilib.run(MyRobot)
