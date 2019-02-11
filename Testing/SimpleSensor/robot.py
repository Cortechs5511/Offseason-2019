import wpilib
from wpilib import SmartDashboard
from wpilib import TimedRobot
from wpilib.joystick import Joystick

from navx.ahrs import AHRS as nav

import ctre
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor

class MyRobot(TimedRobot):

    def robotInit(self):

        self.navx = nav.create_spi()

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

        self.function = self.get_ticks
        self.measurement = 0
        self.estimate = 0
        self.prediction = 0
        self.g = 0.5
        self.h = 0.3
        self.time_step = 0
        self.gain = 0

        self.left_encoder = wpilib.Encoder(0,1)
        self.right_encoder = wpilib.Encoder(2,3)

    def robotPeriodic(self):

        self.measurement = self.function()
        self.time_step += 1
        self.prediction = self.estimate + self.gain
        self.gain += (self.h * (self.measurement - self.prediction) / self.time_step)
        self.estimate = self.prediction + (self.g * (self.measurement - self.prediction))

        self.updateDashboardPeriodic()

        left_power = self.joystick0.getY()
        right_power = self.joystick1.getY()

        self.left.set(left_power)
        self.right.set(right_power * -1)

    def get_ticks(self):
        left_ticks = (self.left_encoder.getDistance())/255
        right_ticks = (self.right_encoder.getDistance())/-127
        ticks = (left_ticks +right_ticks)/2 
        self.distance = ticks * 4 *3.14
        return self.distance

    def autonomousInit(self):
        pass

    def updateDashboardPeriodic(self):
        #SmartDashboard.putNumber("NavX Raw", self.navx.getYaw())
        #SmartDashboard.putNumber("NavX Clean", self.estimate)
        SmartDashboard.putNumber("Average Encoder Raw", self.get_ticks())
        SmartDashboard.putNumber("Encoder Clean", self.estimate)

if __name__ == "__main__":
    wpilib.run(MyRobot)
