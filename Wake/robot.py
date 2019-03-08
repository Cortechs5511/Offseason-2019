from wpilib import SmartDashboard
import wpilib.buttons

from wpilib.command import Command
from wpilib.command import CommandGroup
from commandbased import CommandBasedRobot

from wpilib.sendablechooser import SendableChooser
import map

from subsystems import HatchMech
from subsystems import CargoMech
from subsystems import Climber
from subsystems import Drive
from subsystems import Limelight

from commands import sequences
from commands import autonomous

from commands.drive.setSpeedDT import SetSpeedDT
from commands.drive.turnAngle import TurnAngle

from commands.autonomous import LeftCargo as LeftCargo
from commands.autonomous import RightCargo as RightCargo
from commands.autonomous import CenterCargo as CenterCargo
from commands.autonomous import LeftCargoLevel2 as LeftCargoLevel2
from commands.autonomous import RightCargoLevel2 as RightCargoLevel2
from commands.autonomous import CenterCargoLevel2Left as CenterCargoLevel2Left
from commands.autonomous import CenterCargoLevel2Right as CenterCargoLevel2Right
from commands.autonomous import DriveStraight as DriveStraight

import oi

class MyRobot(CommandBasedRobot):

    dashboard = True

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
        self.limelight = Limelight.Limelight(self) #not a subsystem

        self.hatch = HatchMech.HatchMech(self)
        self.hatch.initialize()

        self.cargo = CargoMech.CargoMech() #not a subsystem
        self.cargo.initialize()

        self.climber = Climber.Climber() #not a subsystem
        self.climber.initialize(self)

        self.drive = Drive.Drive(self)
        self.compressor = wpilib.Compressor(0)

        self.timer = wpilib.Timer()
        self.timer.start()

        self.watch = wpilib.Watchdog(150, None)

        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''

        [self.joystick0, self.joystick1, self.xbox] = oi.commands()

        self.updateDashboardInit()
        self.DriveStraight = DriveStraight()
        self.LeftCargo = LeftCargo()
        self.RightCargo = RightCargo()
        self.CenterCargo = CenterCargo()
        self.LeftCargoLevel2 =LeftCargoLevel2()
        self.RightCargoLevel2 = RightCargoLevel2()
        self.CenterCargoLevel2Left = CenterCargoLevel2Left()
        self.CenterCargoLevel2Right = CenterCargoLevel2Right()
        self.TurnAngle = TurnAngle()

        #self.autonChooser = SendableChooser()
        #self.autonChooser.setDefaultOption("Do Nothing", WaitCommand(3))
        #self.autonChooser.addOption("FrontHatch", AutoFrontHatch())
        #self.autonChooser.addOption("DriveAuton", AutonCheck(9.75))
        #self.autonChooser.addOption("DrivePath", DrivePath())
        #self.autonChooser.addOption("AutonRotation", autonRotation())
        SmartDashboard.putData("DriveStraightAngle", TurnAngle(90))

    def robotPeriodic(self):
        self.limelight.readLimelightData()
        if(self.dashboard): self.updateDashboardPeriodic()

    def autonomousInit(self):
        super().autonomousInit()
        self.drive.zero()
        self.timer.reset()
        self.timer.start()

        self.autoSelector("level1","L")
        #self.autonChooser.getSelected().start()

    def autonomousPeriodic(self):
        super().autonomousPeriodic()

        deadband = 0.25
        if(abs(self.joystick0.getRawAxis(map.drive))>abs(deadband)): setSpeedDT()
        if(abs(self.joystick1.getRawAxis(map.drive))>abs(deadband)): setSpeedDT()

    def teleopInit(self):
        super().teleopInit()
        self.disabledInit()

    def teleopPeriodic(self):
        self.climber.periodic()
        self.cargo.periodic()
        self.hatch.periodic()
        super().teleopPeriodic()

    def updateDashboardInit(self):
        self.drive.dashboardInit()
        self.hatch.dashboardInit()
        self.cargo.dashboardInit()
        self.climber.dashboardInit()
        #self.limelight.dashboardInit()

        #sequences.dashboardInit()
        #autonomous.dashboardInit()

    def updateDashboardPeriodic(self):
        #SmartDashboard.putNumber("Timer", self.timer.get())

        self.drive.dashboardPeriodic()
        self.hatch.dashboardPeriodic()
        self.cargo.dashboardPeriodic()
        self.climber.dashboardPeriodic()
        #self.limelight.dashboardPeriodic()

        #sequences.dashboardPeriodic()
        #autonomous.dashboardPeriodic()

    def disabledInit(self):
        self.scheduler.removeAll()
        self.drive.disable()
        self.hatch.disable()
        self.cargo.disable()
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
