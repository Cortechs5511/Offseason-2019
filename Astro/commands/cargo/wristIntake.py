from wpilib.command import Command

class WristIntake(Command):
    def __init__(self, label, power):
        super().__init__("WristIntake: " + label)
        robot = self.getRobot()
        self.cargoMech = robot.cargoMech
        self.requires(self.cargoMech)
        self.power = power

    def initialize(self):
        pass

    def execute(self):
        if self.power == -1:
            self.cargoMech.outtake()
        elif self.power == 1:
            self.cargoMech.intake()

    def interrupted(self):
        self.cargoMech.stopIntake()

    def end(self):
        self.cargoMech.stopIntake()

    def isFinished(self):
        return self.power == 0
