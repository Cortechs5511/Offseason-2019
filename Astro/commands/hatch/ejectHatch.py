from wpilib.command import Command


class EjectHatch(Command):
    def __init__(self):
        super().__init__('EjectHatch')
        robot = self.getRobot()
        self.hatchMech = robot.hatchMech
        self.requires(self.hatchMech)

    def initialize(self):
        pass

    def execute(self):
         self.hatchMech.ejectHatch()


    def isFinished(self):
        return self.timeSinceInitialized()>0.25

    def interrupted(self):
        pass

    def end(self):
         self.hatchMech.retractEjector()
