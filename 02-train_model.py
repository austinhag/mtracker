# Use this script to take the generated images and train the model.
#
# Images in the source directory should already be cropped down to only
# include a detected face.

# Import libraries
import os
import cv2
import numpy as np
from PIL import Image
import json

# Path where gathered images were saved
folder = 'dataset/faces'  

# Setup face recognizor
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Setup arrays for reading in files
names = []
samples = []
ids = []

# Load images
imagePaths = [os.path.join(folder,f) for f in os.listdir(folder)]     
for imagePath in imagePaths:
    # Process file name
    name = os.path.split(imagePath)[-1].split("-")[0]
    id = int(os.path.split(imagePath)[-1].split("-")[1].split(".")[0])

    # Process name
    if name not in names:
        names.append(name)
    id = names.index(name)

    # Read in image
    img = Image.open(imagePath)
    img_numpy = np.array(img,'uint8')

    # Append each face
    samples.append(img_numpy)
    ids.append(id)

# Train the model
print ("Training the model...")
recognizer.train(samples, np.array(ids))

# Save the model
recognizer.write('trainer/trainer.yml')

# Save the names
with open('trainer/names.json', 'w') as outfile:
    json.dump({'names':names}, outfile)

# Print the numer of faces trained and end program
print(f"Complete. {len(np.unique(ids))} faces trained.")
