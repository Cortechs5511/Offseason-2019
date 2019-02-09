import wpilib
from wpilib import SmartDashboard
from wpilib import TimedRobot
from wpilib.joystick import Joystick

import navx

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

class MyRobot(TimedRobot):

    def robotInit(self):

        self.navx = navx.ahrs.AHRS(0)

        self.timer = wpilib.Timer()
        self.timer.start()

        self.joystick0 = wpilib.Joystick(0)
        self.joystick1 = wpilib.Joystick(1)

        TalonLeft = Talon(10)
        TalonRight = Talon(20)

        VictorLeft1 = Victor(11)
        VictorLeft2 = Victor(12)
        VictorLeft1.follow(TalonLeft)
        VictorLeft2.follow(TalonLeft)

        VictorRight1 = Victor(21)
        VictorRight2 = Victor(22)
        VictorRight1.follow(TalonRight)
        VictorRight2.follow(TalonRight)

        self.left = TalonLeft
        self.right = TalonRight

        self.function = self.navx.getYaw
        self.measurement = 0
        self.estimate = 0
        self.prediction = 0
        self.g = 0.5
        self.h = 0.3
        self.time_step = 0
        self.gain = 0

    def robotPeriodic(self):

        self.measurement = self.function()
        self.time_step += 1
        self.prediction = self.estimate + self.gain
        self.gain += (self.h * (self.measurement - self.prediction) / self.time_step)
        self.estimate = self.prediction + (self.g * (self.measurement - self.prediction))

        self.updateDashboardPeriodic()

        self.left.set(self.joystick0.getY())
        self.right.set(self.joystick1.getY())

    def autonomousInit(self):
        pass

    def updateDashboardPeriodic(self):
        SmartDashboard.putNumber("NavX Raw", self.navx.getYaw())
        SmartDashboard.putNumber("NavX Clean", self.estimate)

if __name__ == "__main__":
    wpilib.run(MyRobot)
