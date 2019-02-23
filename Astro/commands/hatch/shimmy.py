import wpilib 
from wpilib import command 


class Shimmy(Command):
    def __init__(self, Mode):
        super().__init__('Shimmy')

        self.mode = Mode
        self.drive = self.getRobot().drive
        self.requires(self.drive)
        self.shimmyTimer = wpilib.Timer()
        self.shimmyTimer.start()

    def initialize(self): pass 

    def execute(self):
        if self.mode == "Left":
            self.drive.leftTwitch()

        elif self.mode == "Right":
            self.drive.rightTwitch()

    def isFinished(self):
        if self.shimmyTimer > 3000:
            return True
        else: return False

    def end(self):
        self.drive.left.set(0)
        self.drive.right.set(0)

    def interrupted(self):
        self.end()
        
