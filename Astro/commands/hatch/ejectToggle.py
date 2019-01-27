from wpilib.command import Command



class EjectToggle(Command):
    def __init__(self):
        super().__init__('EjectToggle')
        robot = self.getRobot()
        self.hatchMech = robot.hatchMech
        self.requires(self.hatchMech)

    def initialize(self):
        pass

    def execute(self):
        ejectorOut = self.hatchMech.isEjectorOut()
        if ejectorOut:
            self.hatchMech.retractEjector()
        else:
            self.hatchMech.ejectHatch()





    def isFinished(self):
        return True

    def interrupted(self):
        pass

    def end(self):
       pass
