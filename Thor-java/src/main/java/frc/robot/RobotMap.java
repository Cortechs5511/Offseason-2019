/*----------------------------------------------------------------------------*/
/* Copyright (c) 2017-2018 FIRST. All Rights Reserved.                        */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

package frc.robot;

import edu.wpi.first.wpilibj.Preferences;

/**
 * The RobotMap is a mapping from the ports sensors and actuators are wired into
 * to a variable name. This provides flexibility changing wiring, makes checking
 * the wiring easier and significantly reduces the number of magic numbers
 * floating around.
 */
public class RobotMap {

  // Known robots that might have slight variations in configuration
  // that we want to deploy the code to
  public final static int synapse = 0;
  public final static int astroV1 = 1;
  public final static int astroV2 = 2;

  // ID of robot we are deploying to
  // NOTE: Value will be updated when preferences are loaded
  public static int robotId = RobotMap.astroV2;

  // Can ID
  public static int driveLeft1 = 10;
  public static int driveLeft2 = 11;
  public static int driveLeft3 = 12;
  public static int driveRight1 = 20;
  public static int driveRight2 = 21;
  public static int driveRight3 = 22;

  public final static int intake = 30;
  public final static int wrist = 31;

  public final static int hatchWheels = 41;

  public final static int frontLift = 40;
  public final static int backLift = 42;

  public final static int wheelLeft = 50;
  public final static int wheelRight = 51;

  // Solenoids

  public final static int hatchKick = 1;
  public final static int hatchSlide = 2;

  // PWM

  public final static int frontLiftPwm = 1;
  public final static int backLiftPwm = 0;

  // DIO

  public final static int leftEncoderA = 0;
  public final static int leftEncoderB = 1;
  public final static int rightEncoderA = 2;
  public final static int rightEncoderB = 3;

  public static final int backFloor = 4;
  public static final int frontFloor = 5;

  public static final int frontBottomSensor = 6;
  public static final int topSwitch = 7;
  // frontTopSensor = 7
  public static final int backBottomSensor = 8;
  public static final int bottomSwitch = 9;
  // backTopSensor = 9

  // sets the system preferences

  /**
   * Looks up an integer value from the robot configuration file or creates the
   * value if not present.
   *
   * @param key    : Key to use to look up/set value.
   * @param defVal : Default value to set/return if not found.
   * @return : Value from configuration file or default if not found.
   */

  public static int getConfigInt(String key, int defVal) {
    Preferences config = Preferences.getInstance();
    int val = defVal;
    if (config.containsKey(key)) {
      val = config.getInt(key, defVal);
    } else {
      // Value not set in config, set to default value provided
      // so we will see it and be able to edit it in the system
      // preferences editor
      config.putInt(key, val);
    }
    return val;
  }

  /**
   * Looks a float value from the robot configuration file or creates the value if
   * not present.
   * 
   * : param key : Key to use to look up/set value. : param defVal : Default value
   * to set/return if not found. : return : Value from configuration file or
   * default if not found.
   */
  public static float getConfigFloat(String key, float defVal) {
    Preferences config = Preferences.getInstance();
    float val = defVal;
    if (config.containsKey(key)) {
      val = config.getFloat(key, defVal);
    } else {
      // Value not set in config, set to default value provided
      // so we will see it and be able to edit it in the system
      // preferences editor
      val = defVal;
      config.putFloat(key, val);
    }
    return val;
  }

  public static void loadPreferences() {
    robotId = getConfigInt("RobotId", astroV2);
    System.out.println("map.py robotId " + robotId);
    if (robotId == astroV1) {
      driveLeft1 = 20;
      driveLeft2 = 21;
      driveLeft3 = 22;
      driveRight1 = 10;
      driveRight2 = 11;
      driveRight3 = 12;
    }
  }

  // '''BUTTONS/AXES'''
  // call these constants when reading button states in subsystems

  // OPERATOR
  // axes
  public static final int intakeCargo = 2;
  public static final int outtakeCargo = 3;

  // buttons
  public static final int kickHatch = 6; // controlls original only hatch mech
  public static final int toggleHatch = 5; // controlls original only hatch mech
  public static final int drivehatch = 2;
  public static final int wristUp = 7;
  public static final int wristDown = 8;

  public static final int driveForwardClimber = 2;
  public static final int driveBackwardClimber = 3;
  public static final int liftClimber = 4;
  public static final int lowerClimber = 1;
  public static final int disableAll = 0;

  // AXES
  public static final int liftFrontClimber = 5;
  public static final int lowerFrontClimber = 5;
  public static final int liftBackClimber = 1;
  public static final int lowerBackClimber = 1;
  public static final int resetAutoClimb = 9;
  // stopAutoClimb = 11
  public static final int autoStart = 10;
  // DRIVE
  // axes
  public static final int drive = 1;
  // wristUp = 13
  // wristDown = 14
  public static final int wristUpVolts = 12;
  public static final int wristDownVolts = 15;
  // wristUpMagic = 11
  public static final int wristDownMagic = 16;

  // buttons
  public static final int halfSpeed = 1;
  public static final int flip = 2;

}
