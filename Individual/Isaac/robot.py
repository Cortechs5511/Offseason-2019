'''Notes'''
'''		wpilib.DifferentialDrive'''

import wpilib
from wpilib.smartdashboard import SmartDashboard

"""subsystem1 = None

def init():
    global subsystem1

    subsystem1 = SubsystemType()"""

"""from commandbased import CommandBasedRobot

from commands import AutonomousCommandGroup

class MyRobot(CommandBasedRobot):

    def robotInit(self):
        '''Initialize things like subsystems'''

        self.autonomous = AutonomousCommandGroup()


    def autonomousInit(self):
        self.autonomous.start()"""

"""import subsystems
from wpilib.command import InstantCommand

class ExampleCommand(InstantCommand):

    def __init__(self):
        self.requires(subsystems.subsystem1)

    def initialize(self):
        subsystems.subsystem1.do_something()"""

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
		speedL = -self.stick1.getY() #negative for controller
		#speedR = self.stick2.getY()
		speedR = -self.stick1.getThrottle() #(wpilib.Joystick.Axis.Throttle) #negative for controller
		if abs(speedL) < 0.1:
			speedL = 0
		if abs(speedR) < 0.1:
			speedR = 0
		self.setDrivePower(speedL * .793, speedR * .9)

	def autonomousInit(self):
		self.autonTimer = wpilib.Timer()
		self.autonTimer.start()

	def setDrivePower(self, leftpower, rightpower):
		self.robot_driveL.set(-leftpower)
		self.robot_driveR.set(rightpower)

	def autonomousPeriodic(self):
		time = self.autonTimer.get()
		if time <= 1.62:
			self.setDrivePower(.793, .9)
			SmartDashboard.putNumber("autonTime", time)
		else:
			self.setDrivePower(0, 0)


if __name__ == "__main__":
    wpilib.run(MyRobot)
