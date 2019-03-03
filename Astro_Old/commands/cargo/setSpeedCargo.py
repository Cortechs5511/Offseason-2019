from wpilib.command import Command

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
        deadband = .1
        #if self.robot.getOperatorAxis(0) > deadband:
        #    self.cargoMech.wristUp()
        #elif self.robot.getOperatorAxis(1) < -deadband:
        #    self.cargoMech.wristDown()

        #else:
        #    self.cargoMech.wristStop()

        #if self.robot.getOperatorAxis(0) > deadband:
        #    self.cargoMech.intake()
        #
        #elif self.robot.getOperatorAxis(1) < -deadband:
        #    self.cargoMech.outtake()

        #else:
        #    self.cargoMech.stopIntake()
        """if self.power == -1:
            self.cargoMech.outtake()
        elif self.power == 1:
            self.cargoMech.intake()"""

    def interrupted(self):
        self.cargoMech.stopIntake()

    def end(self):
        self.cargoMech.stopIntake()

    def isFinished(self):
        #return self.power == 0
        return False
