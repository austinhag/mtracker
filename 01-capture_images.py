# Use this script to generate images to train the model.
#
# The script is designed to be run on a desktop not a Raspberry Pi. To use on a 
# Raspberry Pi, the PiCamera library should be used instead of cv2 for video
# capture.

# Import libraries
import cv2
import os

# Setup variables
frames = 30  # Total number of frames to capture
folder = 'dataset/faces/'  # Path for saving gathered images

# Setup camera and settings
cam = cv2.VideoCapture(0)
cam.set(3, 1920) # Set frame width
cam.set(4, 1080) # Set frame height

# Setup face detector 
# detector = cv2.CascadeClassifier('imports/haarcascade_frontalface_default.xml') # More accurate but slower
detector = cv2.CascadeClassifier('imports/lbpcascade_frontalface.xml')

# Enter name of individual being analyzed
target = input('Enter name and press return: ')

# Set current file number
current = 0
imagePaths = [os.path.join(folder,f) for f in os.listdir(folder)]     
for imagePath in imagePaths:
    name = os.path.split(imagePath)[-1].split("-")[0]
    if name.upper() == target.upper():
        id = int(os.path.split(imagePath)[-1].split("-")[1].split(".")[0])
        if id > current: current = id

# Capture images 
print("Starting face capture...")
for count in range(0, frames):
    # Read in image
    ret, img = cam.read()
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

    # Process each face 
    for (x,y,w,h) in faces:
        # Save the captured image 
        current += 1
        cv2.imwrite(f"{folder}{target}-{current}.jpg", gray[y:y+h,x:x+w])

# Cleanup
print("Complete. Exiting...")
cam.release()
cv2.destroyAllWindows()
