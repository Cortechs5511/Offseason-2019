# does the drivetrain stuff
import wpilib
from wpilib.smartdashboard import SmartDashboard
from wpilib.command.subsystem import Subsystem
from commands.joystickdrive import joystickDrive
from wpilib.command import Command
import math
import oi

class Drive(Subsystem):

    def __init__(self):
        super().__init__("Drive")
        Command.pageDrive = lambda x=0: self
        self.frontRight = wpilib.Talon(0)
        self.rearRight = wpilib.Talon(1)
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)
        self.frontLeft = wpilib.Talon(2)
        self.rearLeft = wpilib.Talon(3)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.leftEncoder = wpilib.Encoder(8, 9)
        self.leftEncoder.setDistancePerPulse(1/3 * math.pi / 256) # 4 inch wheels?
        self.leftEncoder.setSamplesToAverage(10)
        SmartDashboard.putNumber("distance", 0)
        SmartDashboard.putString("DriveStyle", "Tank")

    def setSpeed(self, leftSpeed, rightSpeed, turn):
        speedMult = 0.6

        if abs(leftSpeed) <= 0.1:
            leftSpeed = 0
        if abs(rightSpeed) <= 0.1:
            rightSpeed = 0

        if oi.halfSpeedButton() == True:
            speedMult = 0.4

        if oi.flipButton() == True:
            speedMult = -speedMult

        if True:#self.driveType == "Arcade": # smartdashboard implementation has not been tested
            power = leftSpeed
            if abs(turn) < 0.1:
                turn = 0
            turn = -0.7 * turn

            if power > 0:
                if turn > 0:
                    [left, right] = [max(power, turn), power - turn]
                else:
                    [left, right] = [power + turn, max(power, -turn)]
            else:
                if turn < 0:
                    [left, right] = [-max(-power, -turn), power - turn]
                else:
                    [left, right] = [power + turn, -max(-power, turn)]

            self.left.set(left * speedMult)
            self.right.set(right * speedMult)

        else:
            self.left.set(-leftSpeed * speedMult)
            self.right.set(-rightSpeed * speedMult)


    def getEncoders(self):
        left = self.leftEncoder.getDistance()
        #right = self.rightEncoder.getDistance()
        SmartDashboard.putNumber("distance", left)
        return left

    def initDefaultCommand(self):
        self.setDefaultCommand(joystickDrive())

    def periodic(self):
        self.getEncoders()
        self.driveType = SmartDashboard.getString("DriveStyle", "Tank")
