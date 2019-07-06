import wpilib
import wpilib.drive
import ctre

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        self.left1 = ctre.WPI_VictorSPX(11)
        self.left2 = ctre.WPI_VictorSPX(12)
        self.leftMain = ctre.WPI_TalonSRX(10)
        self.right1 = ctre.WPI_VictorSPX(21)
        self.right2 = ctre.WPI_VictorSPX(22)
        self.rightMain = ctre.WPI_TalonSRX(20)
        self.left1.follow(self.leftMain)
        self.left2.follow(self.leftMain)
        self.right1.follow(self.rightMain)
        self.right2.follow(self.rightMain)
        self.drive = wpilib.drive.DifferentialDrive(self.leftMain, self.rightMain)
        self.stick = wpilib.Joystick(0)
        self.stick2 = wpilib.Joystick(1)
        self.timer = wpilib.Timer()
        self.leftMain.setNeutralMode(2)
        self.rightMain.setNeutralMode(2)

    def teleopPeriodic(self):
        self.drive.tankDrive(self.stick.getY(), self.stick2.getY())

if __name__ == "__main__":
    wpilib.run(MyRobot)
