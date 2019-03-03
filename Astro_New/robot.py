import wpilib
from wpilib import SmartDashboard
import wpilib.buttons
import map
from subsystems import HatchMech
from subsystems import CargoMech
from subsystems import Climber
from subsystems import Drive
from subsystems import Limelight
from subsystems import Sensors
from CRLibrary.path import odometry as od
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

class MyRobot(wpilib.IterativeRobot):

    dashboard = True
    follower = "Ramsetes"

    frequency = 20
    period = 1/frequency

    def __init__(self):
        super().__init__()

    def robotInit(self):
        #temporary
        TalonLeft = Talon(map.driveLeft1)
        TalonRight = Talon(map.driveRight1)

        map.loadPreferences()

        self.compressor = wpilib.Compressor(0)

        self.timer = wpilib.Timer()
        self.timer.start()
        self.watch = wpilib.Watchdog(150, None)

        self.cargoMech = CargoMech.CargoMech()
        self.sensors = Sensors.Sensors()
        self.hatchMech = HatchMech.HatchMech()
        self.climber = Climber.Climber()
        self.cargoMech.cargoInit()
        self.sensors.sensorsInit()
        self.hatchMech.hatchInit()
        self.climber.climberInit()

    def robotPeriodic(self):
        if self.dashboard:
            self.timer.reset()
            self.timer.start()
            self.timerNum = self.timer.get()
        self.cargoMech.cargoPeriodic()
        self.sensors.sensorsPeriodic()
        self.hatchMech.hatchPeriodic()
        self.climber.climberPeriodic()

    def autonomousInit(self):
        #self.drive.zero()
        self.timer.reset()
        self.timer.start()
        self.curr = 0

    def updateDashboardInit(self):
        self.climber.dashboardInit()

    def updateDashboardPeriodic(self):
        SmartDashboard.putNumber("Periodic Duration", self.timerNum)
        self.climber.dashboardPeriodic()

    def telopInit(self):
        pass

    def disabledInit(self):
        #self.drive.disable()
        self.hatchMech.disable()
        self.cargoMech.disable()
        self.climber.disable()

    def disabledPeriodic(self):
        self.disabledInit()

if __name__ == "__main__":
    wpilib.run(MyRobot)
