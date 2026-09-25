"""
boom_barrier_gate.py
Supervisor-driven controller for an automated AI boom barrier.
Detects humans using an IR/AI camera feed and triggers a rotational motor.
"""

from controller import Supervisor
import math

# 1. Initialize Supervisor & Timestep
# Using Supervisor instead of Robot allows full environmental awareness
robot = Supervisor()
timestep = int(robot.getBasicTimeStep())

# 2. Initialize the Actuators & Smart Sensors
try:
    barrier_motor = robot.getDevice("barrier_motor")
    
    # Initialize the camera with built-in AI recognition
    ir_camera = robot.getDevice("ir_camera")
    ir_camera.enable(timestep)
    ir_camera.recognitionEnable(timestep)
    
    print("====================================================")
    print(" Smart AI Boom Barrier System Initialization Complete")
    print(" Scanning trajectory path for pedestrians...        ")
    print("====================================================")
except Exception as e:
    print(f"Initialization Error: Missing device name in Scene Tree! Details: {e}")

# 3. Define Operational Variables
# Threshold distance in meters to open the gate when a human approaches
TRIGGER_DISTANCE_METERS = 3.0  
GATE_OPEN_POSITION_RAD = 1.57   # ~90 degrees vertical
GATE_CLOSED_POSITION_RAD = 0.0  # Horizontal

# 4. Main Simulation Loop
while robot.step(timestep) != -1:
    
    # Grab the array of tracked objects detected by the AI camera engine
    seen_objects = ir_camera.getRecognitionObjects()
    target_human_in_zone = False
    
    # Process each detected object in the frame
    for obj in seen_objects:
        model_name = obj.get_model().lower()
        
        # Verify if the tracked entity is a Pedestrian or custom Human solid
        if "pedestrian" in model_name or "human" in model_name:
            # Extract 3D relative position coordinates [X, Y, Z] from camera lens axis
            relative_pos = obj.get_position()
            
            # Calculate absolute straight-line Euclidean distance (3D Pythagorean theorem)
            distance = math.sqrt(relative_pos[0]**2 + relative_pos[1]**2 + relative_pos[2]**2)
            
            print(f"[CAMERA ALERT] Tracked: '{obj.get_model()}' | Distance: {distance:.2f}m")
            
            # Evaluate if the human has crossed into the safety trigger perimeter
            if distance <= TRIGGER_DISTANCE_METERS:
                target_human_in_zone = True
                break # Target found inside perimeter, stop checking other objects

    # 5. Actuation State Machine
    if target_human_in_zone:
        # Command rotational motor to pivot upwards smoothly
        barrier_motor.setPosition(GATE_OPEN_POSITION_RAD)
    else:
        # No targets within the safety envelope; keep gate arm secured down
        barrier_motor.setPosition(GATE_CLOSED_POSITION_RAD)
