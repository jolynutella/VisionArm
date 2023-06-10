import os
from picamera import PiCamera
import time
import cv2 as cv 
import numpy as np
import argparse
import imutils

# Camera settings
camWidth = 1280
camHeight = 480

# Final image capture settings
scaleRatio = 0.5

# Camera resolution height must be divisible by 16, and width by 32
camWidth = int((camWidth + 31) / 32) * 32
camHeight = int((camHeight + 15) / 16) * 16
print("Used camera resolution: " + str(camWidth) + " x " + str(camHeight))

# Buffer for captured image settings
imgWidth = int(camWidth * scaleRatio)
imgHeight = int(camHeight * scaleRatio)
capture = np.zeros((imgHeight, imgWidth, 4), dtype=np.uint8)
print("Scaled image resolution: " + str(imgWidth) + " x " + str(imgHeight))

# Initialize the camera
camera = PiCamera(stereo_mode='side-by-side', stereo_decimate=False)
camera.resolution = (camWidth, camHeight)
camera.framerate = 20
camera.hflip = False
camera.awb_mode = 'incandescent'

# Create windows to display camera images
cv.namedWindow("Left camera")
cv.namedWindow("Right camera")
cv.namedWindow("DiffLeftRight")

# Move windows to prevent overlapping
cv.moveWindow("Left camera", 0, 100)
cv.moveWindow("Right camera", 380, 100)
cv.moveWindow("DiffLeftRight", 190, 460)

if __name__ == '__main__':
    def nothing(*arg):
        pass


def main():
    global capture
    
    for frame in camera.capture_continuous(capture, format="bgra", use_video_port=True, resize=(imgWidth, imgHeight)):
        
        # Extract and divide the frame (picture) for both cameras
        imgRight = frame[0:imgHeight, 0:int(imgWidth/2)]
        imgLeft = frame[0:imgHeight, int(imgWidth/2):imgWidth]

        # Convert images to grayscale
        bwRight = cv.cvtColor(imgRight, cv.COLOR_BGR2GRAY)
        bwLeft = cv.cvtColor(imgLeft, cv.COLOR_BGR2GRAY)

        # Display the grayscale image from the right camera
        cv.imshow("Right camera", bwRight)
        
        # Display the grayscale image from the left camera
        cv.imshow("Left camera", bwLeft)

        # Create a new image with the same dimensions as bwLeft and bwRight
        diffImg = np.zeros((bwLeft.shape[0], bwLeft.shape[1]), dtype=np.uint8)

        # Iterate through every pixel in the images and compare their brightness values
        for y in range(bwLeft.shape[0]):
            for x in range(bwLeft.shape[1]):
                # Set the pixel to the average brightness value of both images
                diffImg[y, x] = bwRight[y, x] * 0.5 + bwLeft[y, x] * 0.5

        # Display the resulting image
        cv.imshow("DiffLeftRight", diffImg)

        # Exit when the Esc key is pressed
        if cv.waitKey(30) == 27:
            break
    cv.destroyAllWindows()


# Run the main program
main()