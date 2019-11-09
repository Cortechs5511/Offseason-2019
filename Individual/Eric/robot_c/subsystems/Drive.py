# does the drivetrain stuff
import wpilib
import ctre
from wpilib.command.subsystem import Subsystem
from commands.joystickdrive import JoystickDrive
from wpilib.command import Command
import oi
import math
import map


class Drive(Subsystem):
    def __init__(self):
        super().__init__("Drive")
        Command.pageDrive = lambda x=0: self

        self.left1 = ctre.WPI_TalonSRX(map.left1)
        self.left2 = ctre.WPI_VictorSPX(map.left2)
        self.left3 = ctre.WPI_VictorSPX(map.left3)
        self.right1 = ctre.WPI_TalonSRX(map.right1)
        self.right2 = ctre.WPI_VictorSPX(map.right2)
        self.right3 = ctre.WPI_VictorSPX(map.right3)

        self.left2.follow(self.left1)
        self.left3.follow(self.left1)
        self.right2.follow(self.right1)
        self.right3.follow(self.right1)

        self.leftEncoder = wpilib.Encoder(0, 1)
        self.leftEncoder.setDistancePerPulse(1/3 * math.pi / 256) # 4 inch wheels?
        self.leftEncoder.setSamplesToAverage(10)

        self.rightEncoder = wpilib.Encoder(2, 3)
        self.rightEncoder.setDistancePerPulse(-1/3 * math.pi / 256)
        self.rightEncoder.setSamplesToAverage(10)

    def getLeftEncoder(self):
        left = self.leftEncoder.getDistance()
        return left

    def getRightEncoder(self):
        right = self.rightEncoder.getDistance()
        return right

    def setSpeed(self, leftSpeed, rightSpeed, turn, driveType):
        speedMult = 1.0

        if abs(leftSpeed) <= 0.05:
            leftOutput = 0
        if abs(rightSpeed) <= 0.05:
            rightOutput = 0

        if oi.halfSpeedButton() == True:
            speedMult = 0.5

        if oi.flipButton() == True:
            speedMult = -speedMult

        if driveType == 'Arcade':
            power = -leftPower
            turn = turn
            if abs(turn) < 0.1: turn = 0.00 * self.sign(turn)
            if power > 0:
                if turn > 0:
                    [left, right] = [max(power, turn), power-turn]
                else:
                    [left, right] = [power+turn, max(power, -turn)]
            else:
                if turn < 0:
                    [left, right] = [-max(-power, -turn), power-turn]
                else:
                    [left, right] = [power+turn, -max(-power, turn)]
            self.left1.set(left * speedMult)
            self.right1.set(right * speedMult)
        else:
            self.left1.set(-leftSpeed * speedMult)
            self.right1.set(-rightSpeed * speedMult)

    def initDefaultCommand(self):
        self.setDefaultCommand(JoystickDrive())

    def periodic(self):
        self.getLeftEncoder()
        self.getRightEncoder()
