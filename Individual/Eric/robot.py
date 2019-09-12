import wpilib

class MyRobot(wpilib.TimedRobot):

    def robotInit(self):
        #init motor controllers
        #init joysticks
        pass

    def teleopPeriodic(self):
        #measure joystick values
        #refine data
        #set motor values
        pass

if __name__ == '__main__':
    wpilib.run(MyRobot)
