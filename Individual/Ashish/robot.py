# timed robot
import wpilib
import math
from networktables import NetworkTables
from wpilib import SmartDashboard


class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.frontRight = wpilib.Talon(0)
        self.rearRight = wpilib.Talon(1)
        self.frontRight.setInverted(True)
        self.rearRight.setInverted(True)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        self.frontLeft = wpilib.Talon(2)
        self.rearLeft = wpilib.Talon(3)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.timer = wpilib.Timer()

        self.leftEncoder = wpilib.Encoder(8, 9)
        self.leftEncoder.setDistancePerPulse(1/2 * math.pi / 256)
        self.leftEncoder.setSamplesToAverage(10)

        self.table = NetworkTables.getTable('limelight')

    def teleopPeriodic(self):
        leftInput = float(self.leftStick.getY()) * 0.9
        rightInput = float(self.rightStick.getY()) * 0.9
        if abs(leftInput) >= 0.05:
            self.left.set(leftInput)
        else:
            self.left.set(0)
        if abs(rightInput) >= 0.05:
            self.right.set(rightInput)
        else:
            self.right.set(0)
        self.getLimeData()

    def getLimeData(self):
        tx = self.table.getNumber('tx', 900)
        ta = self.table.getNumber('ta', 900)
        distance_1 = (6.5) / (math.sqrt(ta/100) * math.tan(math.radians(29.8)))
        limeMult = (-5.44 * .0001 * distance_1) + 0.864
        distance_2 = distance_1 * limeMult
        SmartDashboard.putNumber("Limelight Distance", distance_2)
        SmartDashboard.putNumber("Limelight Angle", tx)
        return [distance_2, tx]

    def moveRobot(self):
        [distance, angle] = self.getLimeData()
        #phase 1 - angle tuning
        if abs(angle) > math.radians(1):
            if angle > 0:
                self.right.set(-0.2)
                self.left.set(0.2)
            elif angle < 0:
                self.right.set(0.2)
                self.left.set(-0.2)
            else:
                print('error 01')
        #phase 2 - distance tuning
        elif abs(angle) <= math.radians(1):
            if distance > 0:
                self.right.set(0.3)
                self.left.set(0.3)

if __name__ == "__main__":
    wpilib.run(MyRobot)
