from wpilib.command import Command

class WristMove(Command):
    def __init__(self, label, power):
        super().__init__("WristMove: " + label)
        robot = self.getRobot()
        self.cargoMech = robot.cargoMech
        self.requires(self.cargoMech)
        self.power = power

    def initialize(self):
        pass

    def execute(self):
        if self.power == -1:
            self.cargoMech.wristDown()
        elif self.power == 1:
            self.cargoMech.wristUp()

    def interrupted(self):
        self.cargoMech.wristStop()

    def end(self):
        self.cargoMech.wristStop()

    def isFinished(self):
        return self.power == 0
