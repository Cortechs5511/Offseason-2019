import wpilib
from wpilib import SmartDashboard
import rev

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.frontLeft: CANSparkMax = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.rearLeft: CANSparkMax = rev.CANSparkMax(11, rev.MotorType.kBrushless)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight: CANSparkMax = rev.CANSparkMax(22, rev.MotorType.kBrushless)
        self.rearRight: CANSparkMax = rev.CANSparkMax(10, rev.MotorType.kBrushless)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        for motor in [self.frontLeft, self.rearLeft, self.frontRight, self.rearRight]:
            motor.clearFaults()
            motor.setOpenLoopRampRate(0.5)
            motor.setSmartCurrentLimit(60, 60, 6400) # >= 15 sec. stall tested
            motor.setSecondaryCurrentLimit(100)
            motor.getEncoder().setPositionConversionFactor(42)
            motor.setIdleMode(brake)

        SmartDashboard.putNumber("Left Power", 0)
        SmartDashboard.putNumber("Right Power", 0)

        self.leftStick = wpilib.Joystick(0)

    def teleopInit(self):
        for encoder in [self.frontLeft, self.rearLeft, self.frontRight, self.rearRight]:
            encoder.getEncoder().setPosition(0)

    def teleopPeriodic(self):
        power = self.leftStick.getY()
        rightInput = self.leftStick.getX()
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


if __name__ == '__main__':
    wpilib.run(MyRobot)
