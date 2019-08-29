/*----------------------------------------------------------------------------*/
/* Copyright (c) 2018 FIRST. All Rights Reserved.                             */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

package frc.robot.subsystems;

import com.ctre.phoenix.motorcontrol.NeutralMode;
import com.ctre.phoenix.motorcontrol.SensorCollection;
import com.ctre.phoenix.motorcontrol.can.WPI_TalonSRX;

import edu.wpi.first.wpilibj.command.Subsystem;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import frc.robot.OI;
import frc.robot.RobotMap;
import frc.robot.commands.cargo.CargoHumanControl;

/**
 * Subsystem to manipulate the cargo intake/outake arm and rollers.
 */
public final class CargoMech extends Subsystem {

  /**
   * Different modes of operation for intake wheels.
   */
  public enum IntakeMode {
    /** Spin wheels to pull ball in. */
    intake,
    /** Spin wheels to push ball out. */
    outtake,
    /** Stop wheels from spinning. */
    stop;
  }

  private static final boolean DEBUG = false;

  private double F;
  private int range;
  private double maxVolts;
  private double wristUpVolts;
  private double wristDownVolts;
  private WPI_TalonSRX intake;
  private WPI_TalonSRX wrist;
  private boolean wristAtHome;
  private int wristPosition;
  private boolean wristAtBottom;

  /**
   * Constructs new instance and allocates motor controllers and sensors.
   */
  public CargoMech() {
    super("Cargo");
    int timeout = 15;

    this.F = 0.25;

    // this.angle = 0
    // SmartDashboard.putNumber("angle", this.angle)

    this.range = -1200;

    this.maxVolts = 10.0;
    this.wristUpVolts = 4;
    this.wristDownVolts = -4;

    // below is the talon on the intake
    this.intake = new WPI_TalonSRX(RobotMap.intake);
    this.intake.setName("Cargo", "Intake_" + RobotMap.intake);
    this.intake.setNeutralMode(NeutralMode.Brake);
    this.intake.configVoltageCompSaturation(this.maxVolts);

    this.intake.configContinuousCurrentLimit(20, timeout); // #20 Amps per motor
    this.intake.configPeakCurrentLimit(30, timeout); // 30 Amps during Peak Duration
    this.intake.configPeakCurrentDuration(100, timeout); // Peak Current for max 100 ms
    this.intake.enableCurrentLimit(true);

    // Talon motor object created
    this.wrist = new WPI_TalonSRX(RobotMap.wrist);
    this.wrist.setName("Cargo", "Wrist_" + RobotMap.wrist);
    this.wrist.configFactoryDefault();
    this.wrist.setInverted(true);
    this.wrist.configVoltageCompSaturation(this.maxVolts);
    this.wrist.setNeutralMode(NeutralMode.Brake);
    this.wrist.configClearPositionOnLimitF(true, timeout);
    this.wrist.configContinuousCurrentLimit(20, timeout); // 20 Amps per motor
    this.wrist.configPeakCurrentLimit(30, timeout); // 30 Amps during Peak Duration
    this.wrist.configPeakCurrentDuration(100, timeout); // Peak Current for max 100 ms
    this.wrist.enableCurrentLimit(true);

    // Take initial sensor reading
    readSensors();
  }

  /**
   * This method is called once every iteration by the Scheduler (50 times a
   * second).
   */
  public void periodic() {
    super.periodic();
    // Since reading sensor values takes time, only read them once per iteration.
    readSensors();
  }

  /**
   * Set power/direction of intake wheels based on mode passed in.
   * 
   * @param mode The operation you want (intake, outtake or stop).
   */
  public void setIntake(IntakeMode mode) {
    double power = 0.0;
    if (mode == IntakeMode.intake) {
      power = 0.9;
    } else if (mode == IntakeMode.outtake) {
      power = -0.9;
    }
    intake.set(power);
  }

  /**
   * Set power on wrist motor (unchecked - what you set we apply).
   * 
   * @param power Desired power to apply to motor where negative values move wrist
   *              away from home position towards floor (down) and positive values apply
   *              power to return wrist to home position (up).
   */
  public void setWristPower(double power) {
    wrist.set(power);
  }

  /**
   * Immediately turns off power to both wrist and intake motors.
   */
  public void disable() {
    wrist.set(0);
    intake.set(0);
  }

  /**
   * Helper method used to read the sensors just one time each iteration.
   */
  private void readSensors() {
    SensorCollection wristSensors = wrist.getSensorCollection();
    wristAtHome = wristSensors.isRevLimitSwitchClosed();
    wristAtBottom = wristSensors.isFwdLimitSwitchClosed();
    if (wristAtHome) {
      wristPosition = range;
      wristSensors.setQuadraturePosition(range, 0);
    } else {
      wristPosition = wristSensors.getQuadraturePosition();
    }

    // Now that we've read our sensors, lets update some dashboard values as well
    SmartDashboard.putNumber("Wrist Angle", getAngle());
    SmartDashboard.putBoolean("Limit Switch", wristAtBottom);
    SmartDashboard.putBoolean("Limit Switch Reverse", wristAtHome);

    // Add extra SmartDashboard controls and info if DEBUG constant set to true
    if (DEBUG) {
      SmartDashboard.putNumber("Wrist Position", getPosition());
      SmartDashboard.putNumber("Wrist Output", wrist.get());
      F = OI.getSetNumber("F Gain", F);
      wristUpVolts = OI.getSetNumber("Wrist Up Volts", wristUpVolts);
      wristDownVolts = OI.getSetNumber("Wrist Down Volts", wristDownVolts);
      SmartDashboard.putBoolean("Wrist PinState Quad A", wristSensors.getPinStateQuadA());
      SmartDashboard.putBoolean("Wrist PinState Quad B", wristSensors.getPinStateQuadB());
    }
  }

  /**
   * Nominal output voltage to apply to lift wrist arm (before applying gravity).
   * 
   * @return Output voltage to move wrist up. If DEBUG enabled, you can
   *         see/adjust this value on the dashboard.
   */
  public double getWristUpVolts() {
    return wristUpVolts;
  }

  /**
   * Nominal output power to apply to raise wrist arm (before applying gravity).
   * 
   * @return Power in range of [-1.0, +1.0] required to move wrist up. If DEBUG enabled, you can
   *         see/adjust this value on the dashboard.
   */
  public double getWristUpPower() {
    return wristDownVolts / maxVolts;
  }

  /**
   * Nominal output voltage to apply to lower wrist arm (before applying gravity).
   * 
   * @return Voltage to move wrist down. If DEBUG enabled, you can
   *         see/adjust this value on the dashboard.
   */
  public double getWristDownVolts() {
    return wristDownVolts;
  }

  /**
   * Nominal output power to apply to lower wrist arm (before applying gravity).
   * 
   * @return Power in range of [-1.0, +1.0] required to move wrist down. If DEBUG enabled, you can
   *         see/adjust this value on the dashboard.
   */
  public double getWristDownPower() {
    return wristDownVolts / maxVolts;
  }

  /**
   * Indicates if cargo arm is resting in its home position.\
   * 
   * @return true if arm retracted and resting on upper limit switch.
   */
  public boolean isWristAtHome() {
    return wristAtHome;
  }

  /**
   * Indicates if cargo arm is resting in its home position.\
   * 
   * @return true if arm retracted and resting on upper limit switch.
   */
  public boolean isWristAtBottom() {
    return wristAtBottom;
  }

  /**
   * Returns the raw quaduture position of the cargo arm.
   * 
   * @return Integer count from wrist quadrature encoder.
   */
  public int getPosition() {
    return wristPosition;
  }

  /**
   * Returns the current angle of the wrist in degrees.
   * 
   * @param angDegs
   * @return Angle in degrees - 0 when arm straight up, 90 when horizontal. Angle
   *         will be negative when arm is leaning on back rest.
   */
  public double getAngle() {
    double angle = Math.abs(getPosition() * 115 / range);
    return (angle - 25);
  }

  /**
   * Computes a power adjustment based on wrist angle.
   * 
   * @param angDegs Angle in degrees to compute gravity for (0 when arm straight
   *                up, 90 when horizontal).
   * @return Adjustement to power to compensate for load of arm based on angle.
   */
  public double computeGravity(double angDegs) {
    return Math.sin(Math.toRadians(angDegs)) * F;
  }

  @Override
  public void initDefaultCommand() {
    // Set the default command to be human controlled - NOTE
    // may need to pass reference to "this" to command constructor
    // if this method is invoked in the CargoMech constructor.
    setDefaultCommand(new CargoHumanControl());
  }

}
