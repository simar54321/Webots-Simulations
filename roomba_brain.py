from controller import Robot
import random

TIME_STEP = 64
MAX_SPEED = 6.28  # Standard max speed for custom Webots motors

robot = Robot()

# 1. Setup the Wheels (You fixed these!)
left_motor = robot.getDevice('left_wheel motor')
right_motor = robot.getDevice('right_wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# 2. Setup the SINGLE Bumper (TouchSensor)
# Make sure your TouchSensor's name field in the Scene Tree is "my_bumper"
bumper = robot.getDevice('my_bumper')
bumper.enable(TIME_STEP)

turn_timer = 0
print(">>> CUSTOM ROOMBA: ONLINE AND READY TO CLEAN <<<")

# 3. The Main Cleaning Loop
while robot.step(TIME_STEP) != -1:
    
    # Default state: Drive straight forward
    left_speed = MAX_SPEED
    right_speed = MAX_SPEED

    # If the turn timer is active, override the forward drive and spin!
    if turn_timer > 0:
        turn_timer -= 1
        # Spin in place (Left wheel reverse, Right wheel forward)
        left_speed = -MAX_SPEED
        right_speed = MAX_SPEED
        
    # If we are NOT currently turning, check if we just hit a wall
    else:
        # getValue() returns 1.0 if the bumper is compressed, 0.0 if clear
        if bumper.getValue() > 0.0:
            print("Bonk! Wall detected. Spinning...")
            # Spin for a random amount of time to bounce off at a new angle
            turn_timer = random.randint(15, 40)

    # Apply the speeds to the physical wheels
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)