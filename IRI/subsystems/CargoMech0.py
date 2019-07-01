from wpilib import SmartDashboard
from ctre import WPI_TalonSRX as Talon
from wpilib import SmartDashboard
from wpilib import PIDController
from wpilib import RobotBase
import wpilib
import map
import oi
from sim import simComms
import math

#gravity for cargo ship is -.1, angle is -28
#gravity for rocket is .15, angle is 5
#gravity for resting position was .15 , angle is -50
#gravity for intake is .15, angle is 50
class CargoMech():
    kSlotIdx = 0
    kPIDLoopIdx = 0
    kTimeoutMs = 10

    def initialize(self):
        timeout = 15
        SmartDashboard.putNumber("Wrist Power Set", 0)
        SmartDashboard.putNumber("Gravity Power", 0)
        self.sb = []
        self.targetPosUp = -300 #!!!!!
        self.targetPosDown = -1500 #!!!!!
        self.maxVolts = 10
        self.simpleGain = 0.57
        self.wristUpVolts = 5
        self.wristDownVolts = 2
        self.simpleGainGravity = 0.07
        self.xbox = oi.getJoystick(2)
        self.joystick0 = oi.getJoystick(0)
        #below is the talon on the intake
        self.motor = Talon(map.intake)

        self.input = 0
        self.input2 = 0
        self.lastCargoCommand = "unknown"

        self.motor.configContinuousCurrentLimit(20,timeout) #15 Amps per motor
        self.motor.configPeakCurrentLimit(30,timeout) #20 Amps during Peak Duration
        self.motor.configPeakCurrentDuration(100,timeout) #Peak Current for max 100 ms
        self.motor.enableCurrentLimit(True)

        #Talon motor object created
        self.wrist = Talon(map.wrist)
        if not wpilib.RobotBase.isSimulation():
            self.wrist.configFactoryDefault()
        self.wrist.configVoltageCompSaturation(self.maxVolts)
        self.wrist.setInverted(True)
        self.wrist.setNeutralMode(2)
        self.motor.setNeutralMode(2)
        self.motor.configVoltageCompSaturation(self.maxVolts)

        self.wrist.configClearPositionOnLimitF(True)

        #MOTION MAGIC CONFIG
        self.loops = 0
        self.timesInMotionMagic = 0

        #self.wrist.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)

        self.F = 0
        #should be 0.4
        SmartDashboard.putNumber("F Gain", self.F)

        [self.kP, self.kI, self.kD, self.kF] = [0, 0, 0, 0]
        cargoController = PIDController(self.kP, self.kI, self.kD, self.kF, self, self)
        self.cargoController = cargoController
        self.cargoController.disable()

        self.pidValuesForMode = {
            "resting": [-50, self.kP, self.kI, self.kD, 0.15 / -50],
            "cargoship": [-28, self.kP, self.kI, self.kD, 0.0],
            "intake": [50, self.kP, self.kI, self.kD, 0.0],
            "rocket": [5, self.kP, self.kI, self.kD, 0.19/5],
        }

    def intake(self, mode):
        #Intake/Outtake/Stop, based on the mode it changes the speed of the motor
        if mode == "intake": self.motor.set(0.9)
        elif mode == "outtake": self.motor.set(-0.9)
        elif mode == "stop": self.motor.set(0)

    def pidWrite(self, output):
        maxPower = 0.3
        if output < -maxPower:
            output = -maxPower
        elif output > maxPower:
            output = maxPower
        self.wrist.set(output)
        self.input = output

    def pidGet(self):
        return self.getAngle()

    def setPIDSourceType(self):
        pass

    def getPIDSourceType(self):
        return 0

    def moveWrist(self, mode):
        if mode != self.lastCargoCommand:
            self.lastCargoCommand = mode
            if mode in self.pidValuesForMode:
                array = self.pidValuesForMode[mode]
                self.cargoController.setP(array[1])
                self.cargoController.setI(array[2])
                self.cargoController.setD(array[3])
                self.cargoController.setF(math.sin(self.getAngle()/180*math.pi)*self.F)
                self.cargoController.setSetpoint(array[0])
                self.cargoController.enable()
            else:
                self.cargoController.disable()
        elif(mode not in self.pidValuesForMode):
            self.wrist.set(math.sin(self.getAngle()/180*math.pi)*self.F)
            self.input2 = math.sin(self.getAngle()/180*math.pi)*self.F


    def periodic(self):
        #0.4 as a deadband
        if self.xbox.getRawAxis(map.intakeCargo)>0.4: self.intake("intake")
        elif self.xbox.getRawAxis(map.outtakeCargo)>0.4: self.intake("outtake")
        else: self.intake("stop")

        if self.xbox.getPOV() == 0:
            self.moveWrist("resting")
            self.lastCargoCommand = "resting"
        elif self.xbox.getPOV() == 90:
            self.moveWrist("cargoship")
            self.lastCargoCommand = "cargoship"
        elif self.xbox.getPOV() == 180:
            self.moveWrist("intake")
            self.lastCargoCommand = "intake"
        elif self.xbox.getPOV() == 270:
            self.moveWrist("rocket")
            self.lastCargoCommand = "rocket"
        else:
            self.moveWrist(self.lastCargoCommand)

    #disables intake
    def disable(self):
        self.intake("stop")

    #gets the angle, used in other support functions
    def getAngle(self):
        pos = self.getPosition()
        angle = abs(pos * 115/self.targetPosDown)
        return (angle-20)

    def getPosition(self):
        return self.wrist.getQuadraturePosition()

    def getNumber(self, key, defVal):
        val = SmartDashboard.getNumber(key, None)
        if val == None:
            val = defVal
            SmartDashboard.putNumber(key, val)
        return val

    def dashboardInit(self): pass

    def dashboardPeriodic(self):
        #self.wristUp = self.getNumber("WristUpSpeed" , 0.5)
        #self.wristDown = self.getNumber("WristDownSpeed" , 0.2)
        #self.wristUpVolts = self.getNumber("WristUpVoltage" , 5)
        #self.wristDownVolts = self.getNumber("WristDownVoltage" , 2)
        #self.simpleGain = self.getNumber("Wrist Simple Gain", self.simpleGain)
        #self.simpleGainGravity = self.getNumber("Wrist Simple Gain Gravity", self.simpleGainGravity)
        SmartDashboard.putNumber("Wrist Position", self.wrist.getQuadraturePosition())
        SmartDashboard.putData("PID Controller", self.cargoController)
        SmartDashboard.putNumber("Wrist Angle" , self.getAngle())
        SmartDashboard.putNumber("Wrist Power", self.input)
        SmartDashboard.putNumber("Wrist Power2", self.input2)
        SmartDashboard.putString("Last Cargo Command", self.lastCargoCommand)
        SmartDashboard.putBoolean("Wrist PinState Quad A", self.wrist.getPinStateQuadA())
        SmartDashboard.putBoolean("Wrist PinState Quad B", self.wrist.getPinStateQuadB())
        self.F = SmartDashboard.getNumber("F Gain", 0)
