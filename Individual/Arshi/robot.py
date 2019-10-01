import wpilib

class MyRobot(wpilib.TimedRobot):

	def robotInit(self):
		pass

	def teleopPeriodic(self):
		pass

if __name__ == "__main__":
	wpilib.run(MyRobot)