/*----------------------------------------------------------------------------*/
/* Copyright (c) 2018 FIRST. All Rights Reserved.                             */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

package frc.robot.commands.cargo;

import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.command.Command;
import frc.robot.Robot;
import frc.robot.RobotMap;
import frc.robot.subsystems.CargoMech;
import frc.robot.subsystems.CargoMech.IntakeMode;

/**
 * The default command that runs on the CargoMech subsystem allowing the user to
 * manually control it.
 */
public class CargoHumanControl extends Command {
  /** Desired angle to drop off cargo. */
  private static final double ROCKET_ANGLE = 10.0;

  /** How close we need to be to desired angle to call it good enough. */
  private static final double ANGLE_TOLERANCE = 5.0;

  /**
   * Power to apply when we want wrist in home position on rest and its fallen
   * off.
   */
  private static final double HOLD_POWER = 0.25;

  /** Controller used by operator to control cargo mechanism. */
  private XboxController xbox;

  /**
   * Will toggle between true/false as user presses button on POV (not 100% sure
   * about this).
   */
  private boolean povPressed;

  // Command constructor needs to require all subsystems that it manipulates.
  public CargoHumanControl() {
    requires(Robot.cargoMech);
  }

  // Called just before this Command runs the first time
  @Override
  protected void initialize() {
    // Defer getting reference to XBox controller until initialize() is
    // called to avoid construction nightmares.
    xbox = Robot.m_oi.getOperatorGamepad();
  }

  /**
   * Called repeatedly when this Command is scheduled to run.
   * 
   * <p>This is the Java Command implementation of the periodic(),
   * setWrist(), moveWrist() and wristZBounds() method from the
   * original CargoMech.py Python Subsystem.</p>
   */
  @Override
  protected void execute() {
    CargoMech cm = Robot.cargoMech;

    // Set power to intake rollers
    if (xbox.getRawAxis(RobotMap.intakeCargo) > 0.4) {
      cm.setIntake(IntakeMode.intake);
    } else if (xbox.getRawAxis(RobotMap.outtakeCargo) > 0.4) {
      cm.setIntake(IntakeMode.outtake);
    } else {
      cm.setIntake(IntakeMode.stop);
    }

    // Check for change in state of pov button
    int pov = xbox.getPOV();
    if ((pov >= 0) && povPressed) {
      povPressed = false;
    } else if ((pov >= 0) && !povPressed) {
      povPressed = true;
    }

    double wristPower = 0.0;
    double curAng = cm.getAngle();

    if (povPressed) {
      // Seek wrist angle for rocket delivery of cargo
      double err = ROCKET_ANGLE - curAng;
      // From Python port
      double mult = Math.abs(curAng - 50) / 100 + 0.5; // increase constant if the arm is not moving enough close to the
                                                       // setpoint
      if (err > ANGLE_TOLERANCE) {
        // Need to move arm down
        wristPower = cm.getWristDownPower() * mult;
      } else if (err < -ANGLE_TOLERANCE) {
        // Need to move arm up
        wristPower = cm.getWristUpPower() * mult;
      }
      wristPower += cm.computeGravity(curAng);
    } else if (xbox.getRawButton(RobotMap.wristUp)) {
      wristPower = cm.getWristUpPower() + cm.computeGravity(curAng);
    } else if (xbox.getRawButton(RobotMap.wristDown)) {
      wristPower = cm.getWristDownPower() + cm.computeGravity(curAng);
    }

    // Check bounds on wrist power based on angle
    if (wristPower < 0) {
      if (curAng > 80) {
        // Set power to zero if trying to move down and almost at bottom
        wristPower = 0;
      }
    } else if (wristPower > 0) {
      if (curAng < -20) {
        // Set power to zero if trying to move past home switch
        wristPower = 0;
      } else if (curAng < 10) {
        // Set power to hold power if fell off
        wristPower = HOLD_POWER;
      }
    }
    cm.setWristPower(wristPower);

  }

  // Make this return true when this Command no longer needs to run execute()
  @Override
  protected boolean isFinished() {
    return false;
  }

  // Called once after isFinished returns true
  @Override
  protected void end() {
    // Stop all motors if our command terminates
    Robot.cargoMech.disable();
  }

  // Called when another command which requires one or more of the same
  // subsystems is scheduled to run
  @Override
  protected void interrupted() {
    // We will go ahead and stop motors, however we probably don't actually
    // need to if another command is interrupting us and taking control
    end();
  }
}
