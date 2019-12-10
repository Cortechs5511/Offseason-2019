'''Notes'''
'''		wpilib.DifferentialDrive'''

import wpilib
from wpilib.drive import DifferentialDrive
from wpilib.smartdashboard import SmartDashboard

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
		#self.drive = DifferentialDrive(self.robot_driveL, self.robot_driveR)

	def teleopPeriodic(self):
		speedL = -self.stick1.getY() * .75 #negative for controller
		#speedR = self.stick2.getY()
		speedR = self.stick1.getRawAxis(4) * .30 #(wpilib.Joystick.Axis.Throttle) #negative for controller
		if abs(speedL) < 0.1:
			speedL = 0
		if abs(speedR) < 0.1:
			speedR = 0
		lp = speedL + speedR
		rp = speedL - speedR
		self.setDrivePower(lp * .793, rp * .9)
		#self.drive.arcadeDrive(-speedL, speedR + .375 * speedL, squareInputs=True)

	def autonomousInit(self):
		self.autonTimer = wpilib.Timer()
		self.autonTimer.start()

	def setDrivePower(self, leftpower, rightpower):
		self.robot_driveL.set(-leftpower)
		self.robot_driveR.set(rightpower)

	def autonomousPeriodic(self):
		self.setDrivePower(0, 0)
		#self.drive.arcadeDrive(0,0)
		return
		time = self.autonTimer.get()
		if time <= 1.62:
			self.setDrivePower(.793, .9)
			SmartDashboard.putNumber("autonTime", time)
		else:
			self.setDrivePower(0, 0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
