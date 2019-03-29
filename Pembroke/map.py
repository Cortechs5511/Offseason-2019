import wpilib
from wpilib import Preferences

# Known robots that might have slight variations in configuration
# that we want to deploy the code to
synapse: int = 0
astroV1: int = 1
astroV2: int = 2

# ID of robot we are deploying to
# NOTE: Value will be updated when preferences are loaded
robotId: int = astroV2

#Can ID
driveLeft1 = 10
driveLeft2 = 11
driveLeft3 = 12
driveRight1 = 20
driveRight2 = 21
driveRight3 = 22


intake = 30
wrist = 31

frontLift = 40
backLift = 41

wheelLeft = 50
wheelRight = 51

#Solenoids

hatchKick = 1
hatchSlide = 2

#PWM

frontLiftPwm = 0
backLiftPwm = 1

#DIO

leftEncoder = (0,1)
rightEncoder = (2,3)

frontBottomSensor = 6
frontTopSensor = 7
backBottomSensor = 8
backTopSensor = 9

#sets the system preferences


# Robot preferences file stored on roboRIO
# values can be set differently for each roboRIO
config: Preferences = None

def getConfigInt(key: str, defVal: int) -> int:
  """
  Looks up an integer value from the robot configuration file
  or creates the value if not present.

  : param key : Key to use to look up/set value.
  : param defVal : Default value to set/return if not found.
  : return : Value from configuration file or default if not found.
  """
  global config
  if config.containsKey(key):
    val: int = config.getInt(key, defVal)
  else:
    # Value not set in config, set to default value provided
    # so we will see it and be able to edit it in the system
    # preferences editor
    val: int = defVal
    config.putInt(key, val)
  return val

def getConfigFloat(key: str, defVal: float) -> float:
  """
  Looks a float value from the robot configuration file
  or creates the value if not present.

  : param key : Key to use to look up/set value.
  : param defVal : Default value to set/return if not found.
  : return : Value from configuration file or default if not found.
  """
  global config
  if config.containsKey(key):
    val: float = config.getFloat(key, defVal)
  else:
    # Value not set in config, set to default value provided
    # so we will see it and be able to edit it in the system
    # preferences editor
    val: float = defVal
    config.putFloat(key, val)
  return val

def loadPreferences():
  global config
  config = Preferences.getInstance()
  global robotId
  robotId = getConfigFloat("RobotId", astroV2)
  print("map.py robotId", robotId)
  if robotId == astroV1:
    global driveLeft1
    global driveLeft2
    global driveLeft3
    global driveRight1
    global driveRight2
    global driveRight3
    driveLeft1 = 20
    driveLeft2 = 21
    driveLeft3 = 22
    driveRight1 = 10
    driveRight2 = 11
    driveRight3 = 12

'''BUTTONS/AXES'''
#call these constants when reading button states in subsystems

#OPERATOR
#axes
intakeCargo = 2
outtakeCargo = 3

#buttons
kickHatch = 2 #controlls original only hatch mech
toggleHatch = 5 #controlls original only hatch mech
wristUp =7
wristDown = 8


driveForwardClimber = 2
driveBackwardClimber = 3
liftClimber = 4
lowerClimber = 1
disableAll = 0

#AXES
liftFrontClimber = 5
lowerFrontClimber = 5
liftBackClimber = 1
lowerBackClimber = 1
resetAutoClimb = 0
#DRIVE
#axes
drive = 1
#wristUp = 13
#wristDown = 14
wristUpVolts = 12
wristDownVolts = 15
wristUpMagic = 11
wristDownMagic = 16
#buttons
halfSpeed = 1
flip = 4
shimmy = 15
