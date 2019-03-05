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

if robotId == astroV1:
    frontLift = 40
    backLift = 41
else:
    frontLift = 41
    backLift = 40

wheelLeft = 50
wheelRight = 51

#Solenoids

hatchKick = 0
hatchSlide = 1

climberLock1 = 2
climberLock2 = 3

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
