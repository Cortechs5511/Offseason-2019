import wpilib
import wpilib.drive
import ctre

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.frontLeft = ctre.WPI_TalonSRX(0) #can't get talons to work
        self.rearLeft = ctre.WPI_TalonSRX(1)
        #self.left = wpilib.SpeedControllerGroup(self.frontLeft, self.rearLeft)

        self.frontRight = ctre.WPI_TalonSRX(2)
        self.rearRight = ctre.WPI_TalonSRX(3)
        #self.right = wpilib.SpeedControllerGroup(self.frontRight, self.rearRight)

        #self.drive = wpilib.DifferentialDrive(self.left, self.right)
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.timer = wpilib.Timer()

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous. Please don't select this one, because it instantly kills the robot."""
        print("This is a placeholder. It is recommended to stop this.")
        self.frontRight.set(-0.01)
        self.rearRight.set(0.01)
        self.frontLeft.set(0.01)
        self.rearLeft.set(-0.01)


    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        #ideally this would be in another file but i can't figure out how to do that yet
        if abs(self.rightStick.getY()) < 0.05:
            self.frontRight.set(0)
            self.rearRight.set(0)
            pass
        if abs(self.leftStick.getY()) < 0.05:
            self.frontLeft.set(0)
            self.rearLeft.set(0)
            pass
        if self.rightStick.getY() >= 0.05:
            self.frontRight.set(self.rightStick.getY()*0.9) #5% deadband for forwards and reverse
            self.rearRight.set(self.rightStick.getY()*0.9) #0.9x linear scaling
        elif self.rightStick.getY() <= -0.05:
            self.frontRight.set(self.rightStick.getY()*0.9)
            self.rearRight.set(self.rightStick.getY()*0.9)
        if self.leftStick.getY() >= 0.05:
            self.frontLeft.set(self.leftStick.getY()*0.9) #5% deadband for forwards and reverse
            self.rearLeft.set(self.leftStick.getY()*0.9) #0.9x linear scaling
        elif self.leftStick.getY() <= -0.05:
            self.frontLeft.set(self.leftStick.getY()*0.9)
            self.rearLeft.set(self.leftStick.getY()*0.9)


if __name__ == "__main__":
    wpilib.run(MyRobot)

#to-do work out motor control groups to optimize teleopPeriodic
#to-do physics file
