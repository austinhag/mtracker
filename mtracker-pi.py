# This script is the tracker that is intended to be run on the Raspberry Pi.

# Import libraries
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
import time
from home import turnOnLights, broadcastWarning 
import json

# Setup variables
sleeptime = 30        # Number of minutes to sleep after detection until resuming
width = int(832)      # Width of image to capture
height = int(624)     # Height of image to capture
font = cv2.FONT_HERSHEY_SIMPLEX    # Font for markup on the image

# Setup face detector
# detector = cv2.CascadeClassifier('imports/haarcascade_frontalface_default.xml') # More accurate but slower
detector = cv2.CascadeClassifier('imports/lbpcascade_frontalface.xml')

# Setup face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

# Load config from json file
with open('config.json', 'r') as f:
    config = json.load(f)
    child = config["CHILD"]

# Load names from json file
with open('trainer/names.json', 'r') as f:
    data = json.load(f)
    names = ['Unknown']
    for name in data['names']: names.append(name)

# Initialize the camera 
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width,height))
time.sleep(0.1)

# Define min window size to be recognized as a face
minW = 75
minH = 60

# Setup array for face detection window
detects = [0] * 10

# Capture frames from the camera and start monitoring
print(f"Monitoring for {child}...")
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Extract image
    img = frame.array

    # Generate timestamp
    timestr = datetime.utcnow().strftime("%Y%m%d-%H%M%S_%f")        
    
    # Convert to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Detect faces in the image    
    faces = detector.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (minW, minH),
       )

    # Check each face in the image to see if it's a match
    for(x,y,w,h) in faces:
        # Check for a match
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check confidence level. Zero is a perfect match.
        if (confidence < 100):
            name = names[id]
        else:
            name = "Unknown"
        print(f"{timestr}: {name} - {100-confidence:.1f}%")

        # Save raw images
        cv2.imwrite(f"captures/{timestr}-{name}-{100-confidence:.1f}-RAW.jpg", img)

        # Add markup on image and save            
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(img, name, (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.imwrite(f"captures/{timestr}-{name}-{100-confidence:.1f}.jpg", img)

        # Check to see if the name is a match to the target
        if name == child:
            # If it's a match, record the instance
            detects.append(1)
            
            # If the face has been detected sufficiently over a defined window, raise the alarms
            if sum(detects)>=2:
                print(f'Found {child}!')
    
                # Turn on lights and broadcast warning
                turnOnLights('on')
                broadcastWarning()
    
                # Sleep for a defined period
                time.sleep(sleeptime)
    
                # Resume monitoring
                detects = [0] * 10
                turnOnLights('off')
                print('Resuming monitoring...')
        else:
            # If not detected, update sequence accordingly
            detects.append(0)
        
        # Update window to drop oldest observation
        detects.pop(0)

    # Clear capture buffer
    rawCapture.truncate(0)

    # Exit if ESC is pressed
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Exit and cleanup
print("Exiting...")
cv2.destroyAllWindows()
