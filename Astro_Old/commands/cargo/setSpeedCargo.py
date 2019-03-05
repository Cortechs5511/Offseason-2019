from wpilib.command import Command
import map

class SetSpeedCargo(Command):
    def __init__(self, timeout=300):
        super().__init__("SetSpeedCargo")
        self.robot = self.getRobot()
        self.cargoMech = self.robot.cargoMech
        self.requires(self.cargoMech)
        self.xbox = self.robot.xbox


    def initialize(self):
        pass

    def execute(self):
        deadband = 0.05
        if self.xbox.getRawAxis(map.setSpeedWrist) > deadband:
            self.cargoMech.wrist("up")
        elif self.xbox.getRawAxis(map.setSpeedWrist) < -deadband:
            self.cargoMech.wrist("down")
        else: self.cargoMech.wrist("stop")

        if self.xbox.getRawAxis(map.intakeCargo) > deadband:
            self.cargoMech.motorIntake.set(0.5)
        elif self.xbox.getRawAxis(map.outtakeCargo) > deadband:
            self.cargoMech.intake("outtake")
        else: self.cargoMech.intake("stop")

    def interrupted(self):
        self.cargoMech.disable()

    def end(self):
        self.cargoMech.disable()

    def isFinished(self):
        return False
