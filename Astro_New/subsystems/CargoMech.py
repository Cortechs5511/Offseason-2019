import wpilib
from wpilib import SmartDashboard



import ctre


import map
class CargoMech():
    def cargoInit(self):
        #Create all physical parts used by subsystem
        self.debug = True
        self.robot = Robot
        #fix
        self.motorIntake = ctre.WPI_TalonSRX(map.intake)
        self.motorWrist = ctre.WPI_TalonSRX(map.wrist)
        self.motorIntake.setName("Cargo","Motor Intake")
        self.motorWrist.setName("Cargo", "Motor Wrist")
        self.xbox = self.robot.operatorAxis(id)
    def intake(self):
        ''' Intake the balls (turn wheels inward) '''
        self.motorIntake.set(0.5)
    def outtake(self):
        ''' Outake the balls (turn wheels outwards) '''
        self.motorIntake.set(-0.5)
    def stopIntake(self):
        ''' Quit intake/outake '''
        self.motorIntake.set(0)
    def wristUp(self):
        '''Move wrist up, make angle bigger'''
        self.motorWrist.set(0.5)
    def wristDown(self):
        '''Move wrist down, make angle smaller: Make sure to stop it at a certain point'''
        self.motorWrist.set(-0.5)
    def wristStop(self):
        '''Stops wrist'''
        self.motorWrist.set(0)

    def cargoPeriodic(self):

        deadband = 0.1
        if self.xbox.getRawAxis(1) > deadband:
            self.wristUp()
        elif self.xbox.getRawAxis(1) < -deadband:
            self.wristDown()

        else: self.wristStop()
        
        if self.xbox.getRawAxis(2) > deadband:
            self.intake()
        
        elif self.xbox.getRawAxis(3) > deadband:
            self.outtake()

        else: self.stopIntake() 

    def subsystemInit(self):
        r = self.robot

        #wristUp : wpilib.buttons.JoystickButton = r.operatorAxis(1)
        #wristUp.whileActive(WristMove('wrist up',1))
        #wristDown : wpilib.buttons.JoystickButton = r.operatorAxis(1)
        #wristDown.whileActive(WristMove('wrist down',-1))
        #outtakeButton : wpilib.buttons.JoystickButton = r.operatorButton(5)
        #outtakeButton.whileActive(WristIntake('outtake',-1))
        #intakeButton : wpilib.buttons.JoystickButton = r.operatorButton(6)
        #intakeButton.whileActive(WristIntake('intake',1))
    
    ''' def dashboardInit(self):
        """ Adds subsystem specific commands. """

            if self.debug == True:
            SmartDashboard.putData("Intake", WristIntake('intake',1))
            SmartDashboard.putData("Outtake",WristIntake('outtake',-1))
            SmartDashboard.putData("Stop Inake",WristIntake('stop',0))
            SmartDashboard.putData("Wrist up",WristMove('wrist up',1))
            SmartDashboard.putData("Wrist down",WristMove('wrist down',-1))
            SmartDashboard.putData("Stop wrist",WristMove('stop wrist',0)) '''

    def disable(self):
        self.stopIntake()
        self.wristStop()
    def dashboardPeriodic(self):
        pass 

   