import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
########
import vgamepad as vg
gamepad = vg.VX360Gamepad()
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.2)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
gamepad.update()
time.sleep(0.5)
########
wCam, hCam = 1280, 768
################################
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img = detector.findHands(img)

    #SET ALL VALUES TO 0
    gamepad.left_trigger_float(value_float=0)
    gamepad.right_trigger_float(value_float=0)
    gamepad.right_joystick_float(x_value_float=0, y_value_float=0)

    if detector.results.multi_hand_landmarks:
        # Loop through each detected hand
            for i, hand_landmarks in enumerate(detector.results.multi_hand_landmarks):
                # Get the handedness (e.g., 'Left', 'Right') for the current hand
                handedness = detector.results.multi_handedness[i].classification[0].label

                # Create a list of landmark coordinates for the current hand
                lmList = []
                h, w, c = img.shape # Get current frame dimensions
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])

                # Ensure there are enough landmarks to perform calculations (at least thumb and index finger)
                if len(lmList) != 0: # Landmark IDs 4 (thumb tip) and 8 (index finger tip) are crucial
                    x1_thumb, y1_thumb = lmList[4][1], lmList[4][2] # Thumb tip coordinates
                    x2_index, y2_index = lmList[8][1], lmList[8][2] # Index finger tip coordinates
                    x3_base, y3_base = lmList[0][1], lmList[0][2]

                    # --- CODE FOR RIGHT HAND (TRIGGERS) ---
                    if handedness == 'Right':
                        cv2.circle(img, (x1_thumb, y1_thumb), 15, (255, 0, 255), cv2.FILLED)
                        cv2.circle(img, (x2_index, y2_index), 15, (255, 0, 255), cv2.FILLED)
                        cv2.line(img, (x1_thumb, y1_thumb), (x2_index, y2_index), (255, 0, 255), 3)
                        #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                        length_acc = np.abs(x2_index - x1_thumb)
                        length_break = np.abs(y2_index - y1_thumb)
                        #print(int(length_acc),int(length_break))

                        trigger_rt = np.interp(length_acc,[30,170],[0,1])
                        trigger_lt = np.interp(length_break,[30,170],[0,1])
                        #print(length)
                        # Hand range 30 - 170
                        # Trigger Range 0 - 1 float

                        if length_acc>length_break:            
                            gamepad.right_trigger_float(value_float=trigger_rt)
                            gamepad.left_trigger_float(value_float=0)
                        else:
                            gamepad.right_trigger_float(value_float=0)
                            gamepad.left_trigger_float(value_float=trigger_lt)

                        # Optional: Print values for debugging
                        # print(f"Left Hand - Accel: {int(length_acc)}, Brake: {int(length_break)}")

                    # --- CODE FOR LEFT HAND (RIGHT JOYSTICK) ---
                    elif handedness == 'Left':
                        cv2.circle(img, (x3_base, y3_base), 15, (255, 0, 255), cv2.FILLED)
                        cv2.circle(img, (x1_thumb, y1_thumb), 15, (255, 0, 255), cv2.FILLED)
                        cv2.line(img, (x3_base, y3_base), (x1_thumb, y1_thumb), (255, 0, 255), 3)
                        #cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)        

                        dx = x3_base - x1_thumb
                        dy = y3_base - y1_thumb

                        # Use atan2 to get the angle in radians (-pi to pi)
                        angle_radians = math.atan2(dy, dx)

                        # Convert to degrees (-180 to 180)
                        angle_degrees = math.degrees(angle_radians)

                        # Normalize to 0 to 360 degrees for easier quadrant checking
                        # (e.g., -90 becomes 270, -135 becomes 225)
                        if angle_degrees < 0:
                            angle_degrees += 360

                        # Apply custom mapping rules based on the 0-360 range
                        if 0 <= angle_degrees <= 180:
                            # Quadrant 1 (0 to 90) and Quadrant 2 (90 to 180)
                            degrees = angle_degrees
                        elif 180 < angle_degrees <= 270:
                            # Quadrant 3 (180 to 270)
                            degrees = 180.0
                        else: # 270 < angle_degrees < 360
                            # Quadrant 4 (270 to 360)
                            degrees = 0.0

                        joystick_lx = np.interp(degrees,[0,180],[1,-1])
                        gamepad.left_joystick_float(x_value_float=joystick_lx, y_value_float=0) 
    
                        # Optional: Print values for debugging
                        # print(f"Right Hand - Joystick X: {joystick_x:.2f}, Y: {joystick_y:.2f}")

        # Update the virtual gamepad state with all set values for this frame
    gamepad.update()
    time.sleep(0.01) # Small delay to prevent CPU overuse

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)

