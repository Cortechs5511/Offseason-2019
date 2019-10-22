import wpilib
talons = {
  "frontLeft": 2,
  "backLeft": 3,
  "frontRight": 0,
  "backRight": 1,
}

joystick = {
  "leftJs": 0,
  "rightJs": 1
}
leftJs = wpilib.Joystick(joystick["leftJs"])
rightJs = wpilib.Joystick(joystick["rightJs"])
