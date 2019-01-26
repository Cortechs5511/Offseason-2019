from wpilib.command import Command


class SlideToggle(Command):
    # this is a simple toggle command for pnuematics and the slide mechanism.
    def __init__(self):
        super().__init__('ToggleSlide')
        robot = self.getRobot()
        self.hatchMech = robot.hatchMech
        self.requires(self.hatchMech)

    def initialize(self):
        pass

    def execute(self):
        slideOut = self.hatchMech.isSlideIn()
        if slideOut:
            self.hatchMech.slideIn()
        else:
            self.hatchMech.slideOut()
         

    def isFinished(self):
        return True

    def interrupted(self):
        pass

    def end(self):
       pass