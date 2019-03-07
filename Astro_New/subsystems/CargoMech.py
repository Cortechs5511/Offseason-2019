import wpilib
from wpilib import SmartDashboard
import ctre
import map

class CargoMech():
    def cargoInit(self, robot):
        self.robot = robot
        self.xbox = map.getJoystick(2)
        self.debug = True
        self.motorIntake = ctre.WPI_TalonSRX(map.intake)
        if not wpilib.RobotBase.isSimulation():
            self.motorIntake.configFactoryDefault()
        self.motorWrist = ctre.WPI_TalonSRX(map.wrist)
        self.motorIntake.setName("Cargo","Motor Intake")
        self.motorWrist.setName("Cargo", "Motor Wrist")

    def intake(self, mode):
        ''' Intake/Outtake/StopIntake the balls (turn wheels inward)'''
        if mode == "intake":
            self.motorIntake.set(0.9)
        elif mode == "outtake":
            self.motorIntake.set(-0.9)
        elif mode == "stop":
            self.motorIntake.set(0)

    def wrist(self, mode):
        '''Moves or stops the wrist'''
        if mode == "up":
            self.motorWrist.set(0.5)
        elif mode == "down":
            self.motorWrist.set(-0.5)
        elif mode == "stop":
            self.motorWrist.set(0)

    def cargoPeriodic(self):
        deadband = 0.4
        if self.xbox.getRawAxis(map.setSpeedWrist) > deadband:
            self.wrist("up")
        elif self.xbox.getRawAxis(map.setSpeedWrist) < -deadband:
            self.wrist("down")
        else: self.wrist("stop")

        if self.xbox.getRawAxis(map.intakeCargo) > deadband:
            self.intake("intake")
        elif self.xbox.getRawAxis(map.outtakeCargo) > deadband:
            self.intake("outtake")
        else: self.intake("stop")

    def disable(self):
        self.intake("stop")
        self.wrist("stop")

    def dashboardPeriodic(self):
        pass
