import cv2
import numpy as NotImplemented

# set up web cam capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame by frame
    ret, frame = cap.read()

    if not ret:
        print('Error: Failed to capture image.')
        break


    # convert to HSV for color filtering 
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #Define the range for skin color in HSV
    lower_skin = np.array([0,20,70], dtype=np.unit8)
    upper_skin = np.array([20,255,255],dtype=np.unit8)
    
    #create a mask to detect skin color
    mask = cv2.inRange(hsv,lower_skin,upper_skin)

    #Apply the mask to the frame
    result = cv2.bitwise_and(frame,frame,mask=mask)

    #Find contours (hand shape) in the maskedf image
    contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If contours are found ,draw them
    if contours:
        max_contour = max(contours,key= cv2.contourArea) #Get Largest Contour
        if cv2.contourArea(max_contour) >500: # Ignoroe small contour
            # Draw the bounding box around the detected hand
            x,y,w,h= cv2.boundingRect(max_contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h), (0,255,0),2)

            # get the center of the hand further tracking or intereption
            center_x = int(x+w/2)
            center_y = int(y+h/2)
            cv2.circle(frame, (center_x, center _y), 5, (0,0,255),-1)#Red dot at center

        # Display the original and result frames
        cv2.imshow('original Frame',frame)
        cv2.imshow('Filtered Frame',result)

        # Break he loop when 'q' is pressed
        if cv2.waitkey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()