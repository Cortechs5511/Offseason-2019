import wpilib
from wpilib import SmartDashboard
from wpilib.command import Command
from commandbased import CommandBasedRobot

class DebugRate(Command):
    def initialize(self):
        self.curr = 0
        self.print = 10 #change for frequency

    def execute(self):
        self.curr += 1
        if(self.curr%self.print!=0): return
        time = self.timeSinceInitialized()
        SmartDashboard.putNumber("Iterations:", self.curr/(time+1e-5))
        SmartDashboard.putNumber("Time", time)
        SmartDashboard.putNumber("Rate", self.curr/(time+1e-5))

class MyRobot(CommandBasedRobot):
    def robotInit(self):
        pass
    def robotPeriodic(self):
        pass
    def autonomousInit(self):
        self.rate = DebugRate()
        self.rate.start()

if __name__ == "__main__":
    wpilib.run(MyRobot)
