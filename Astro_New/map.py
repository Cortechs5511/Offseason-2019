import wpilib
from wpilib import Preferences
import wpilib
from wpilib.joystick import Joystick
from wpilib.buttons.joystickbutton import JoystickButton
from wpilib.buttons import Button

# Known robots that might have slight variations in configuration
# that we want to deploy the code to
synapse: int = 0
astroV1: int = 1
astroV2: int = 2

# ID of robot we are deploying to
# NOTE: Value will be updated when preferences are loaded
robotId: int = astroV2

#Can ID
if robotId == astroV2:
    driveLeft1 = 20
    driveLeft2 = 21
    driveLeft3 = 22
    driveRight1 = 10
    driveRight2 = 11
    driveRight3 = 12
else:
    driveLeft1 = 10
    driveLeft2 = 11
    driveLeft3 = 12
    driveRight1 = 20
    driveRight2 = 21
    driveRight3 = 22

intake = 31
wrist = 30

wheelLeft = 50
wheelRight = 51

if robotId == astroV2:
    frontLift = 41
    backLift = 40
else:
    frontLift = 40
    backLift = 41


#Solenoids

hatchKick = 1
hatchSlide = 0

climberLock1 = 2
climberLock2 = 3

#DIO

leftEncoder = (0,1)
rightEncoder = (2,3)

frontBottomSensor = 6
frontTopSensor = 7
backBottomSensor = 8
backTopSensor = 9

#Analog Input sensors
frontSensor = 1
backSensor = 0

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

'''BUTTONS/AXES'''
#call these constants when reading button states in subsystems

#OPERATOR
#axes
setSpeedWrist = 1 #drive the wrist up and down using an axes
intakeCargo = 2
outtakeCargo = 3
#buttons
ShootPositionWrist = 1 #brings wrist in a position to outtake carog
KickSimpleHatch = 2 #controlls original only hatch mech
ToggleSimpleHatch = 3 #controlls original only hatch mech
IntakePositionWrist = 4 #brings the wrist to intaking position on floor
ToggleNewHatch = 5 #controls hatch mech on arm

resetAutoClimb = 4#11 #when pressed this clears the auto climb cache to retry
autoClimb = 5#12 #while held button that will run the auto climb

#DRIVE
#axes
drive = 1
#buttons
flip = 0
halfSpeed = 3
driveForwardClimber = 7
driveBackwardClimber = 8
liftClimber = 9
lowerClimber = 10
liftFrontClimber = 13
lowerFrontClimber = 14
liftBackClimber = 12
lowerBackClimber = 15


def getJoystick(num):

    joystick0 = Joystick(0)
    joystick1 = Joystick(1)
    xbox = Joystick(2)

    if num == 0: return joystick0
    elif num == 1: return joystick1
    else: return xbox
