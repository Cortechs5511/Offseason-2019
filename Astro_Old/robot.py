import math
import wpilib
import oi

from wpilib import SmartDashboard
import wpilib.buttons
from wpilib.command import Command
from wpilib.command import CommandGroup
from wpilib.command import WaitCommand
from commandbased import CommandBasedRobot

from commands.zero import Zero
from commands import sequences
from commands import autonomous

from commands.autonomous import DriveStraight

from commands.drive.drivePath import DrivePath
from commands.drive.rotateAuton import autonRotation

from wpilib.sendablechooser import SendableChooser

import map
from subsystems import HatchMech
from subsystems import CargoMech
from subsystems import Climber
from subsystems import Drive
from subsystems import Limelight
from commands import resetAll
from subsystems import disableAll


from CRLibrary.path import odometry as od
#from commands.climber.autoClimb import AutoClimb
from commands.climber.liftRobot import LiftRobot
from commands.climber.driveToEdge import DriveToEdge

from commands.autoSingleHatch import LeftCargo as LeftCargo
from commands.autoSingleHatch import RightCargo as RightCargo
from commands.autoSingleHatch import CenterCargo as CenterCargo
from commands.autoSingleHatch import LeftCargoLevel2 as LeftCargoLevel2
from commands.autoSingleHatch import RightCargoLevel2 as RightCargoLevel2
from commands.autoSingleHatch import CenterCargoLevel2Left as CenterCargoLevel2Left
from commands.autoSingleHatch import CenterCargoLevel2Right as CenterCargoLevel2Right
from commands .autoSingleHatch import DriveStraight as DriveStraight


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

        # Load system preferences prior to constructing
        # subsystems
        map.loadPreferences()

        # Construct subsystems prior to constructing commands
        self.limelight = Limelight.Limelight(self)
        self.hatchMech = HatchMech.HatchMech(self)
        self.cargoMech = CargoMech.CargoMech(self)
        self.climber = Climber.Climber(self)
        self.drive = Drive.Drive(self)
        self.compressor = wpilib.Compressor(0)

        self.timer = wpilib.Timer()
        self.timer.start()
        self.watch = wpilib.Watchdog(150, None)

        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''

        [self.joystick0, self.joystick1, self.xbox, self.xbox2] = oi.commands()

        #self.rate = rate.DebugRate()
        #SmartDashboard.putData(rate.DebugRate())

        #self.rate.initialize()

        self.updateDashboardInit()
        self.DriveStraight = DriveStraight()
        self.LeftCargo = LeftCargo()
        self.RightCargo = RightCargo()
        self.CenterCargo = CenterCargo()
        self.LeftCargoLevel2 =LeftCargoLevel2()
        self.RightCargoLevel2 = RightCargoLevel2()
        self.CenterCargoLevel2Left = CenterCargoLevel2Left()
        self.CenterCargoLevel2Right = CenterCargoLevel2Right()
        self.DrivePath = DrivePath(name="DriveStraight", follower="Ramsetes")
        #self.autonChooser = SendableChooser()
        #self.autonChooser.setDefaultOption("Do Nothing", WaitCommand(3))
        #self.autonChooser.addOption("FrontHatch", AutoFrontHatch())
        #self.autonChooser.addOption("DriveAuton", AutonCheck(9.75))
        #self.autonChooser.addOption("DrivePath", DrivePath())
        #self.autonChooser.addOption("AutonRotation", autonRotation())
        #SmartDashboard.putData("AutonChooser", self.autonChooser)

        #self.hatchMech.subsystemInit()
        #self.cargoMech.subsystemInit()
        self.climber.subsystemInit()
        self.climber.dashboardInit()
        #self.hatchMech.hatchInit(self)

        climberAuto : wpilib.buttons.JoystickButton = self.driverLeftButton(11)
        cg = CommandGroup("AutoClimb")
        cg.addSequential(LiftRobot("both"))
        cg.addSequential(DriveToEdge("front"))
        cg.addSequential(LiftRobot("front"))
        cg.addSequential(DriveToEdge("back"))
        cg.addSequential(LiftRobot("back"))
        climberAuto.whileHeld(cg)


    # def teleopInit(self):
    #     self.loop_timer = looptimer.LoopTimer(self.logger)

    # def teleopPeriodic(self):
    #     super().teleopPeriodic()
    #     self.loop_timer.measure()

    def robotPeriodic(self):
        #self.drive.odMain.display()
        #self.drive.odTemp.display()
        #self.hatchMech.hatchPeriodic()
        self.limelight.readLimelightData()
        if(self.dashboard): self.updateDashboardPeriodic()

    def autonomousInit(self):
        self.drive.zero()
        self.timer.reset()
        self.timer.start()
        self.curr = 0
        #self.autoSelector(self.position, side)
        self.autoSelector("level1","L")
        #self.autonChooser.getSelected().start()


    def updateDashboardInit(self):
        SmartDashboard.putData("Drive", self.drive)
        #SmartDashboard.putData("Hatch", self.hatchMech)
        #SmartDashboard.putData("Cargo", self.cargoMech)
        SmartDashboard.putData("Climber", self.climber)
        self.drive.dashboardInit()
        #self.hatchMech.dashboardInit()
        #self.cargoMech.dashboardInit()
        self.climber.dashboardInit()
        #self.limelight.dashboardInit()

        #sequences.dashboardInit()
        #autonomous.dashboardInit()

        #SmartDashboard.putData("Zero", Zero())

    def updateDashboardPeriodic(self):
        #SmartDashboard.putNumber("PressureSwitchValue", self.compressor.getPressureSwitchValue())
        #SmartDashboard.putNumber("Timer", self.timer.get())
        #self.rate.execute()
        self.drive.dashboardPeriodic()
        #self.hatchMech.dashboardPeriodic()
        #self.cargoMech.dashboardPeriodic()
        self.climber.dashboardPeriodic()
        #self.limelight.dashboardPeriodic()

        #sequences.dashboardPeriodic()
        #autonomous.dashboardPeriodic()

    def telopInit(self):
        #auton: Command = self.autonChooser.getSelected()
        #auton.cancel()
        pass

    def disabledInit(self):
        self.drive.disable()
        self.hatchMech.disable()
        self.cargoMech.disable()
        self.climber.disable()

    def disabledPeriodic(self):
        self.disabledInit()


    def driverLeftButton(self, id):
        """ Return a button off of the left driver joystick that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.joystick0, id)

    def driverRightButton(self, id):
        """ Return a button off of the right driver joystick that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.joystick1, id)

    def operatorButton(self, id):
        """ Return a button off of the operator gamepad that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.xbox, id)

    def operator2Button(self, id):
        """ Return a button off of the operator gamepad that we want to map a command to. """
        return wpilib.buttons.JoystickButton(self.xbox2, id)

    def operatorAxis(self,id):
        """ Return a Joystick off of the operator gamepad that we want to map a command to. """
        #id is axis channel for taking value of axis
        return self.xbox.getRawAxis(id)
        #wpilib.joystick.setAxisChannel(self.xbox, id)

    def operator2Axis(self,id):
        """ Return a Joystick off of the operator gamepad that we want to map a command to. """
        #id is axis channel for taking value of axis
        return self.xbox2.getRawAxis(id)
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

    def autoSelector(self, preference, position):
        """"returns auto command group to run based on starting position and preference for level 1 or 2"""
        pos = position
        pref = preference
        if pos == "L":
            if pref == "level1":
                self.LeftCargo.start()
            elif pref == "level2side":
                self.LeftCargoLevel2.start()
            elif pref == "level2center":
                self.CenterCargoLevel2Left.start()
            elif pref == "drivestraight":
                self.DriveStraight.start()
            else: pass
        elif pos == "R":
            if pref == "level1":
                self.RightCargo.start()
            elif pref == "level2side":
                self.RightCargoLevel2.start()
            elif pref== "level2center":
                self.CenterCargoLevel2Right.start()
            elif pref =="drivestraight":
                self.DriveStraight.start()
            else:
                pass
        elif pos == "C":
            self.CenterCargo.start()
        else:
            pass

if __name__ == "__main__":
    wpilib.run(MyRobot)
