/*----------------------------------------------------------------------------*/
/* Copyright (c) 2017-2018 FIRST. All Rights Reserved.                        */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

package frc.robot;

import edu.wpi.first.wpilibj.Joystick;
import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

/**
 * This class is the glue that binds the controls on the physical operator
 * interface to the commands and command groups that allow control of the robot.
 */
public class OI {

  private XboxController operator;
  private Joystick driverLeft;
  private Joystick driverRight;

  /**
   * Constructor creates controllers used by driver and operator.
   */
  OI() {
    driverLeft = new Joystick(0);
    driverRight = new Joystick(1);
    operator = new XboxController(2);
  }

  /**
   * Helper method that gets or sets number from SmartDashboard.
   * 
   * <p>
   * NOTE: If the value is not present on the dashboard, it will be added to the
   * dashboard using the default value applied.
   * </p>
   * 
   * @param key    The unique string associated with the number (label on
   *               SmartDashboard).
   * @param defVal The default value to used if number is not available.
   * @return Value from dashboard or default value if value not yet on dashboard.
   */
  public static double getSetNumber(String key, double defVal) {
    double val = defVal;
    if (SmartDashboard.containsKey(key)) {
      val = SmartDashboard.getNumber(key, val);
    } else {
      SmartDashboard.putNumber(key, val);
    }
    return val;
  }

  /**
   * Get access to the gamepad used by the operator.
   * 
   * @return Reference to controller.
   */
  public XboxController getOperatorGamepad() {
    return operator;
  }

  /**
   * Get access to the left joystick used by the driver to control the robot.
   * 
   * @return Reference to controller.
   */
  public Joystick getDriverLeft() {
    return driverRight;
  }

  /**
   * Get access to the right joystick used by the driver to control the robot.
   * 
   * @return Reference to controller.
   */
  public Joystick getDriverRight() {
    return driverLeft;
  }

  //// CREATING BUTTONS
  // One type of button is a joystick button which is any button on a
  //// joystick.
  // You create one by telling it which joystick it's on and which button
  // number it is.
  // Joystick stick = new Joystick(port);
  // Button button = new JoystickButton(stick, buttonNumber);

  // There are a few additional built in buttons you can use. Additionally,
  // by subclassing Button you can create custom triggers and bind those to
  // commands the same as any other Button.

  //// TRIGGERING COMMANDS WITH BUTTONS
  // Once you have a button, it's trivial to bind it to a button in one of
  // three ways:

  // Start the command when the button is pressed and let it run the command
  // until it is finished as determined by it's isFinished method.
  // button.whenPressed(new ExampleCommand());

  // Run the command while the button is being held down and interrupt it once
  // the button is released.
  // button.whileHeld(new ExampleCommand());

  // Start the command when the button is released and let it run the command
  // until it is finished as determined by it's isFinished method.
  // button.whenReleased(new ExampleCommand());
}
