
import wpilib
from wpilib import SmartDashboard
import wpilib.buttons
import map
from subsystems import HatchMech
from subsystems import CargoMech
from subsystems import Climber
from subsystems import Drive
from subsystems import Limelight
from CRLibrary.path import odometry as od

class MyRobot(wpilib.IterativeRobot):

    dashboard = True
    follower = "Ramsetes"

    frequency = 20
    period = 1/frequency

    def __init__(self):
        super().__init__()

    def robotInit(self):

        '''
        This is a good place to set up your subsystems and anything else that
        you will need to access later.
        '''
        map.loadPreferences()
        self.compressor = wpilib.Compressor(0)

        self.timer = wpilib.Timer()
        self.timer.start()
        self.watch = wpilib.Watchdog(150, None)
        self.climber = Climber.Climber()

        self.climber.climberInit()


        '''
        Since OI instantiates commands and commands need access to subsystems,
        OI must be initialized after subsystems.
        '''

    def robotPeriodic(self):
        self.climber.climberPeriodic()


    def autonomousInit(self):
        self.drive.zero()
        self.timer.reset()
        self.timer.start()
        self.curr = 0

    def updateDashboardInit(self):
        pass

    def updateDashboardPeriodic(self):
        pass

    def telopInit(self):
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
