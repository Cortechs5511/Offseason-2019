import wpilib
import ctre

class MyRobot(CommandBasedRobot):

    def robotInit(self):
        self.moveLeft1 = ctre.WPI_VictorSPX(3)
        self.moveLeft2 = ctre.WPI_VictorSPX(2)
        self.moveRight1 = ctre.WPI_VictorSPX(1)
        self.moveRight2 = ctre.WPI_VictorSPX(0)
        self.joystick1 = wpilib.Joystick(1)
        self.joystick2 = wpilib.Joystick(2)


    def teleopPeriodic(self):
        if self.joystick1.getY() >= .2:
            self.moveLeft1.set(0.3)
            self.moveLeft2.set(0.3)
        elif self.joystick1.getY() <= -0.2:
            self.moveLeft1.set(-0.3)
            self.moveLeft2.set(-0.3)
        if self.joystick2.getY() >= .2:
            self.moveRight1.set(0.3)
            self.moveRight2.set(0.3)
        elif self.joystick2.getY() <= -0.2:
            self.moveRight1.set(-0.3)
            self.moveRight2.set(-0.3)


if __name__ == '__main__':
    wpilib.run(MyRobot)
