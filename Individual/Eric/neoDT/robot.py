import wpilib
from wpilib import SmartDashboard
import rev

class MyRobot(wpilib.TimedRobot):
    #code for practice DT neo testing
    def robotInit(self):
        self.frontLeft: CANSparkMax = rev.CANSparkMax(0, rev.MotorType.kBrushless)
        self.rearLeft: CANSparkMax = rev.CANSparkMax(1, rev.MotorType.kBrushless)
        self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight: CANSparkMax = rev.CANSparkMax(2, rev.MotorType.kBrushless)
        self.rearRight: CANSparkMax = rev.CANSparkMax(3, rev.MotorType.kBrushless)
        self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        for motor in [self.frontLeft, self.rearLeft, self.frontRight, self.rearRight]:
            motor.clearFaults()
            motor.setOpenLoopRampRate(0.5)
            #motor.setSmartCurrentLimit(64, 64, 4100) # with 40A breakers equals >= 3sec. peak endurance at 64A
            #motor.setSecondaryCurrentLimit(100)
            #motor.setIdleMode(coast)

        SmartDashboard.putNumber("Left Power", 0)
        SmartDashboard.putNumber("Right Power", 0)
        SmartDashboard.putString("Control Mode", "Joystick")

        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)

    def teleopInit(self):
        for motor in [self.frontLeft, self.frontRight]:
            motor.getEncoder().setPosition(0)
        self.controlMode = SmartDashboard.getString("Control Mode", "Joystick")

    def teleopPeriodic(self):
        if self.controlMode == "Joystick":
            leftInput = self.leftStick.getY()
            rightInput = self.rightStick.getY()

            SmartDashboard.putNumber("Left Power", leftInput)
            SmartDashboard.putNumber("Right Power", rightInput)

            if abs(leftInput) >= 0.1:
                self.left.set(leftInput * 0.9)
            else:
                self.left.set(0)
            if abs(rightInput) >= 0.1:
                self.right.set(rightInput * 0.9)
            else:
                self.right.set(0)
        elif self.controlMode == "SmartDashboard":
            self.left.set(SmartDashboard.getNumber("Left Power", 0))
            self.right.set(SmartDashboard.getNumber("Right Power", 0))
        else:
            self.left.stopMotor()
            self.right.stopMotor()
            SmartDashboard.putNumber("Left Power", 0)
            SmartDashboard.putNumber("Right Power", 0)

    def updateEncoders(self):
        SmartDashboard.putNumber("Left Encoder", self.frontLeft.getEncoder().getPosition())
        SmartDashboard.putNumber("Right Encoder", self.frontRight.getEncoder().getPosition())

    def periodic(self):
        self.updateEncoders()


if __name__ == '__main__':
    wpilib.run(MyRobot)
