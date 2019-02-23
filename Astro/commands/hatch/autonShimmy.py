import wpilib
from wpilib.command import Command
from wpilib.command import TimedCommand
from wpilib.command import CommandGroup

class AutonShimmy(CommandGroup):
    def __init__(self, Mode):

        self.mode = Mode
        self.drive = self.getRobot().drive
        self.Shimmy = self.shimmy.Shimmy
        self.requires(self.Shimmy)
        self.end = False
        
    def execute(self):

        self.addSequential(self.Shimmy("Left"))
        self.addSequential(self.Shimmy("Right"))
        self.end = True

    def isFinished(self):
        if self.end == True:
            return True
        else: return False
    
    def end(self):
        self.drive.left.set(0)
        self.drive.right.set(0)

    def interrupted(self:
        self.end()


    
