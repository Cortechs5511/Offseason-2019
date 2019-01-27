from wpilib.command import Command
from wpilib import SmartDashboard

class DebugRate(Command):
    def initialize(self):
        self.curr = 0
        self.print = 10 #change for frequency

    def execute(self):
        self.curr += 1
        if(self.curr%self.print!=0): return
        time = self.timeSinceInitialized()
        SmartDashboard.putNumber("Iterations:", self.curr)
        SmartDashboard.putNumber("Time", time)
        SmartDashboard.putNumber("Rate", self.curr/(time+1e-5))
