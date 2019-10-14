import wpilib

class MyRobot(wpilib.TimedRobot):

	def robotInit(self):
		'''Isaac is a good programmer'''
		pass

	def teleopPeriodic(self):
		pass

if __name__ == "__main__":
	wpilib.run(MyRobot)
