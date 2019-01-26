import math
import wpilib
import wpilib.buttons
from wpilib import TimedRobot
from ctre import WPI_TalonSRX as Talon
from ctre import WPI_VictorSPX as Victor
from wpilib import drive

class MyRobot(TimedRobot):

    def robotInit(self):

        self.joystick0 = wpilib.Joystick(0)
        self.joystick1 = wpilib.Joystick(1)
        self.leftTalon = Talon(10)
        self.left2 = Victor(11)
        self.left3 = Victor(12)
        self.rightTalon = Talon(20)
        self.right2 = Victor(21)
        self.right3 = Victor(22)
        self.left2.follow(self.leftTalon)
        self.left3.follow(self.leftTalon)
        self.right2.follow(self.rightTalon)
        self.right3.follow(self.rightTalon)
        self.drive = wpilib.drive.DifferentialDrive(self.leftTalon, self.rightTalon)

        #set stuff to be inverted
        for motor in [self.leftTalon, self.left2, self.left3]:
            #motor.setInverted(True)
            pass

        for motor in [self.rightTalon, self.right2, self.right3]:
            motor.setInverted(True)
            #pass

    def robotPeriodic(self):
        self.drive.tankDrive(self.joystick0.getY(), self.joystick1.getY())

    def autonomousInit(self):
        pass

if __name__ == "__main__":
    wpilib.run(MyRobot)
