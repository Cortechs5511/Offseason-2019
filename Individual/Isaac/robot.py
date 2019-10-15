'''Notes'''
'''		wpilib.DifferentialDrive'''

import wpilib

class MyRobot(wpilib.TimedRobot):

	def robotInit(self):

		self.motorL1 = wpilib.Talon(0)
		self.motorL2 = wpilib.Talon(1)
		self.motorR1 = wpilib.Talon(2)
		self.motorR2 = wpilib.Talon(3)
		self.robot_driveL = wpilib.SpeedControllerGroup(self.motorL1, self.motorL2)
		self.robot_driveR = wpilib.SpeedControllerGroup(self.motorR1, self.motorR2)
		self.stick1 = wpilib.Joystick(0)
		self.stick2 = wpilib.Joystick(1)

	def teleopPeriodic(self):
		speedL = self.stick1.getY()
		speedR = self.stick2.getY()
		if abs(self.stick1.getY()) < 0.02:
			speedL = 0
		if abs(self.stick2.getY()) < 0.02:
			speedR = 0
		self.robot_driveL.set(-self.stick1.getY())
		self.robot_driveR.set(self.stick2.getY())

if __name__ == "__main__":
	wpilib.run(MyRobot)
