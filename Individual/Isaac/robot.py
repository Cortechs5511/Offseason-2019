import wpilib

'''Notes'''
	'''wpilib.DifferentialDrive'''

class MyRobot(wpilib.TimedRobot):

	def robotInit(self):

		self.motorL1 = wpilib.Jaguar(0)
		self.motorL2 = wpilib.Jaguar(1)
		self.motorR1 = wpilib.Jaguar(2)
		self.motorR2 = wpilib.Jaguar(3)
		self.robot_driveL = wpilib.drive.SpeedControllerGroup(self.motorL1, self.motorL2)
		self.robot_driveR = wpilib.drive.SpeedControllerGroup(self.motorR1, self.motorR2)
		self.stick1 = wpilib.Joystick(1)
		self.stick2 = wpilib.Joystick(2)

	def teleopPeriodic(self):
		speedL = self.stick.getY()
		speedR = self.stick2.getY()
		if abs(self.stick.getY()) < 0.02:
			speedL = 0
		if abs(self.stick2.getY()) < 0.02:
			speedR = 0
		self.robot_driveL.set(self.stick1.getY())
		self.robot_driveR.set(self.stick2.getY())

if __name__ == "__main__":
	wpilib.run(MyRobot)
