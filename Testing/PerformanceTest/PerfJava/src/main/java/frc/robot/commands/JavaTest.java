/*----------------------------------------------------------------------------*/
/* Copyright (c) 2017-2018 FIRST. All Rights Reserved.                        */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

package frc.robot.commands;

import edu.wpi.first.wpilibj.command.Command;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import frc.robot.Robot;

/**
 * An example command.  You can replace me with your own command.
 */
public class JavaTest extends Command {

  private int iteration;
  private double runTime;
  private double sum;

  public JavaTest() {
    super("JavaTest");
    iteration = 1;
    sum = 0.0;
    runTime = 0.0;
  }


  // Called repeatedly when this Command is scheduled to run
  @Override
  protected void execute() {
    loop(iteration);
  }

  private void loop(int count) {
    for (int i = 0; i < iteration; i++) {
      compute(128);
    }
  }

  private double compute(int n) {
    sum = 0;
    for (int i = 0; i < n; i++) {
      sum += Math.cos(i) + Math.sin(i) + Math.sqrt(i);
    }
    return sum;
  }

  // Make this return true when this Command no longer needs to run execute()
  @Override
  protected boolean isFinished() {
    return true;
  }

  // Called once after isFinished returns true
  @Override
  protected void end() {
    runTime = timeSinceInitialized();
    SmartDashboard.putNumber("runTime", runTime);
    SmartDashboard.putNumber("iteration", iteration);
    SmartDashboard.putNumber("Iterations Per Sec", iteration/runTime);
    SmartDashboard.putNumber("sum", sum);

    if (runTime < 0.1) {
      iteration = iteration * 2;
    }
    else if (runTime > 0.25) {
      iteration = (int) (iteration * 0.5);
    }
  }

  // Called when another command which requires one or more of the same
  // subsystems is scheduled to run
  @Override
  protected void interrupted() {
    end();
  }
}
