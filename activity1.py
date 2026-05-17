import cv2
import numpy as np

# Set up webcam capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:

    # Capture frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define skin color range
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    # Create mask
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Apply mask
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Find contours
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw largest contour
    if contours:

        max_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(max_contour) > 500:

            # Bounding rectangle
            x, y, w, h = cv2.boundingRect(max_contour)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # Center point
            center_x = int(x + w / 2)
            center_y = int(y + h / 2)

            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (0, 0, 255),
                -1
            )

    # Show frames
    cv2.imshow("Original Frame", frame)
    cv2.imshow("Filtered Frame", result)

    # Press q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release webcam
cap.release()
cv2.destroyAllWindows()