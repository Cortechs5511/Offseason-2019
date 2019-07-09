from wpilib import SmartDashboard
import wpilib.buttons

from wpilib.command import Command
from wpilib.command import CommandGroup
from commandbased import CommandBasedRobot

from wpilib.sendablechooser import SendableChooser
import map
from wpilib import CameraServer

from subsystems import HatchMech
from subsystems import CargoMech
#from subsystems import CargoMech0
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
from commands.autonomous import DriveStraight as DriveStraight
from commands.autonomous import DriveStraightSide as DriveStraightSide
from commands.autonomous import CenterCargoPart2 as CenterCargoPart2
from commands.autonomous import AutoAlign as AutoAlign
from commands.autonomous import StraightAlign as StraightAlign
from commands.autonomous import LimeLightAutoAlign

from commands.drive.driveStraightDistance import DriveStraightDistance
from commands.drive.driveStraightCombined import DriveStraightCombined

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
        wpilib.CameraServer.launch()
        self.lastAuto = False
        self.lastAlign = False
        self.lastStraightAlign = False
        self.teleop = False
        Command.getRobot = lambda x=0: self

        # Load system preferences prior to constructing
        # subsystems
        map.loadPreferences()

        # Construct subsystems prior to constructing commands
        self.limelight = Limelight.Limelight(self) #not a subsystem

        self.hatch = HatchMech.HatchMech(self)
        self.hatch.initialize()

        #self.cargo = CargoMech0.CargoMech()
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
        self.DriveStraightSide = DriveStraightSide()
        self.LeftCargo = LeftCargo()
        self.RightCargo = RightCargo()
        self.CenterCargo = CenterCargo()
        self.SetSpeedDT = SetSpeedDT()
        self.CenterCargoPart2 = CenterCargoPart2()

        # Set up auton chooser
        self.autonChooser = SendableChooser()
        self.autonChooser.setDefaultOption("Drive Straight", "DriveStraight")
        #self.autonChooser.addOption("Test LimeLight", "TestLimeLight")
        self.autonChooser.addOption("Left Cargo", "LeftCargo")
        self.autonChooser.addOption("Right Cargo", "RightCargo")
        self.autonChooser.addOption("Do Nothing", "DoNothing")
        self.autonChooser.addOption("Level 1 Center","Level1Center")
        self.autonChooser.addOption("Drive Straight Side", "DriveStraightSide")

        SmartDashboard.putData("Auto mode", self.autonChooser)
        self.drive.initializeCommands(self)

    def robotPeriodic(self):
        self.limelight.readLimelightData()
        SmartDashboard.putBoolean("teleop",self.teleop)

        if(self.dashboard): self.updateDashboardPeriodic()

        '''currAlign = self.joystick0.getRawButton(map.autoAlign)
        if currAlign and currAlign != self.lastAlign:
            AutoAlign(self.limelight.getPath()[0],self.limelight.getPath()[1],self.limelight.getPath()[2],self.limelight.getPath()[3]).start()

        if not currAlign and currAlign != self.lastAlign:
            AutoAlign(self.limelight.getPath()[0],self.limelight.getPath()[1],self.limelight.getPath()[2],self.limelight.getPath()[3]).cancel()
            self.SetSpeedDT.start()

        self.lastAlign = currAlign'''

        '''currStraightAlign = self.joystick0.getRawButton(map.straightAlign)
        if currStraightAlign and currStraightAlign != self.lastStraightAlign:
            StraightAlign(self.limelight.getTx()).start()
        self.lastStraightAlign = currAlign
        if not currStraightAlign and currStraightAlign != self.lastStraightAlign:
            StraightAlign(self.limelight.getTx()).cancel()
            self.SetSpeedDT.start()'''

    def autonomousInit(self):
        super().autonomousInit()
        self.drive.zero()
        self.timer.reset()
        self.timer.start()

        self.autoSelector(self.autonChooser.getSelected())

    def autonomousPeriodic(self):
        super().autonomousPeriodic()

        #starts second part of auto for center if button is pressed
        currAuto = self.xbox.getRawButton(map.autoStart)
        if currAuto and currAuto != self.lastAuto: self.CenterCargoPart2.start()
        self.lastAuto = currAuto

        #driver takes control of drivetrain
        deadband = 0.1
        if(abs(self.joystick0.getRawAxis(map.drive))>abs(deadband)): self.SetSpeedDT.start()
        if(abs(self.joystick1.getRawAxis(map.drive))>abs(deadband)): self.SetSpeedDT.start()

        self.cargo.periodic()

    def teleopInit(self):
        super().teleopInit()
        self.disabledInit()
        self.teleop = True

    def teleopPeriodic(self):
        self.climber.periodic()
        self.cargo.periodic()
        self.hatch.periodic()
        super().teleopPeriodic()

    def updateDashboardInit(self):
        self.drive.dashboardInit()
        #self.hatch.dashboardInit()
        #self.cargo.dashboardInit()
        self.climber.dashboardInit()
        #self.limelight.dashboardInit()
        #sequences.dashboardInit()
        #autonomous.dashboardInit()

    def updateDashboardPeriodic(self):
        #SmartDashboard.putNumber("Timer", self.timer.get())
        self.drive.dashboardPeriodic()
        #self.hatch.dashboardPeriodic()
        #self.cargo.dashboardPeriodic()
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

    def autoSelector(self, auto):
        a = auto

        if a == "DriveStraight":
            self.DriveStraight.start()
        elif a == "DoNothing":
            self.disabledInit()
        elif a == "Level1Center":
            self.CenterCargo.start()
        elif a == "DriverControl":
            self.driverControl()
        elif a == "DriveStraightSide":
            self.DriveStraightSide.start()
        elif a== "RightCargo":
            self.RightCargo.start()
        elif a== "LeftCargo":
            self.LeftCargo.start()
        elif a == "TestLimeLight":
            LimeLightAutoAlign(self).start()
        else:
            self.disabledInit()

    def driverControl(self):
        self.SetSpeedDT.start()


if __name__ == "__main__":
    wpilib.run(MyRobot)
