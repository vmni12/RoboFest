#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT11, GearSetting.RATIO_36_1, False)
left_motor_b = Motor(Ports.PORT12, GearSetting.RATIO_36_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT19, GearSetting.RATIO_36_1, True)
right_motor_b = Motor(Ports.PORT20, GearSetting.RATIO_36_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
leftAntiFall = Line(brain.three_wire_port.a)
rightAntiFall = Line(brain.three_wire_port.b)
RangeOutput = Sonar(brain.three_wire_port.c)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

#region Variables

# Reversinxg from edge
fallDistance = 5 # less than how close the table is (you shouldnt need to edit this)
reverseDistance = 5 # how far back to reverse when it almost runs off the table (in)
reverseTurn = 45 # how many degrees to turn after backing up
lockDistance = 16.10

#drive
drivetrain.set_drive_velocity(100, PERCENT)
drivetrain.set_turn_velocity(100, PERCENT)

# debugging
showDebug = True # shows debug info on the display, reccomended to keep on

#endregion Variables

#region Logic
wait(3, SECONDS)
while True:
    # wander
    while not (leftAntiFall.reflectivity(PERCENT)<fallDistance or rightAntiFall.reflectivity(PERCENT)<fallDistance):
        drivetrain.drive(FORWARD)

        while RangeOutput.distance(INCHES) < lockDistance:
            drivetrain.drive(FORWARD)
            wait(5, MSEC)

        wait(5, MSEC) # idk if that fixes crashing or smth but the block compiler does it so ok
    
    # when its about to fall off
    drivetrain.drive_for(REVERSE, reverseDistance, INCHES, wait=True)
    drivetrain.turn_for(RIGHT, reverseTurn,DEGREES, wait=True)

    # GUI

    # debugging
        #resetPrint()
        # brain.screen.print("Left Percentage: " + leftAntiFall.reflectivity(PERCENT))
        # brain.screen.print("Right Percentage: " + rightAntiFall.reflectivity(PERCENT))

    wait(5, MSEC) # again, idk what this is for but vex says its good
#endregion Logic
