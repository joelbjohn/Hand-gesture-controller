import vgamepad as vg
import time
import keyboard # For non-blocking keyboard input

# --- Gamepad Initialization ---
gamepad = vg.VX360Gamepad()

# Press a button briefly to 'wake up' the virtual gamepad
# This helps some games detect it initially
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.2)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.5)

print("Virtual Xbox 360 Gamepad Initialized. You can now open your PC game.")
print("Controls:")
print("  W/A/S/D: Left Joystick (Up/Left/Down/Right)")
print("  Q: Left Trigger (Hold to press)")
print("  E: Right Trigger (Hold to press)")
print("  ESC: Exit program")
print("\nPress ESC in the console to stop.")

# --- Gamepad State Variables ---
# Joystick values range from -1.0 to 1.0 (float)
joystick_lx = 0.0
joystick_ly = 0.0

# Trigger values range from 0.0 to 1.0 (float)
trigger_lt = 0.0
trigger_rt = 0.0

# Sensitivity for analog controls (adjust as needed)
JOYSTICK_SENSITIVITY = 1.0 # Directly sets to max/min
TRIGGER_PRESS_VALUE = 1.0 # Sets to full press when key is held

running = True

# --- Main Game Loop ---
while running:
    # --- Read Keyboard Input ---
    # Joystick Input
    joystick_lx = 0.0
    joystick_ly = 0.0

    if keyboard.is_pressed('w'):
        joystick_ly = JOYSTICK_SENSITIVITY # Y-axis: Up
    elif keyboard.is_pressed('s'):
        joystick_ly = -JOYSTICK_SENSITIVITY # Y-axis: Down

    if keyboard.is_pressed('h'):
        joystick_lx = -JOYSTICK_SENSITIVITY # X-axis: Left
    elif keyboard.is_pressed('j'):
        joystick_lx = JOYSTICK_SENSITIVITY # X-axis: Right

    # Trigger Input
    trigger_lt = TRIGGER_PRESS_VALUE if keyboard.is_pressed('o') else 0.0
    trigger_rt = TRIGGER_PRESS_VALUE if keyboard.is_pressed('k') else 0.0

    # Exit Condition
    if keyboard.is_pressed('escape'):
        running = False

    # --- Update Gamepad State ---
    # Set left joystick position
    gamepad.left_joystick_float(x_value_float=joystick_lx, y_value_float=joystick_ly)

    # Set trigger pressures
    gamepad.left_trigger_float(value_float=trigger_lt)
    gamepad.right_trigger_float(value_float=trigger_rt)

    # Send the updated state to the virtual gamepad
    gamepad.update()

    # --- Small Delay ---
    # This is crucial to prevent the program from consuming 100% CPU
    # and allows other processes (like the game) to run smoothly.
    # Adjust this value: smaller values mean more responsive but higher CPU.
    # A value of 0.01 (100 updates/second) is usually good.
    time.sleep(0.01)

# --- Cleanup ---
# Reset all gamepad inputs to their default state before exiting
gamepad.reset()
gamepad.update()
print("Program stopped. Gamepad reset.")