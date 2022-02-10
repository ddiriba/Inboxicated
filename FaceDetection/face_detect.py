# Face Detection class implementation
# This file was created with the help of a tutorial from RealPython.com
import cv2
import numpy

class Face_Detect:

    image = None
    convertedImage = None
    faces = None
    filepath = None
    video = None

    # constructor which sets cascade
    def __init__(self, cascade):
        self.cascade = cv2.CascadeClassifier(cascade)

    # sets filepath for image input
    def setPath(self, filepath):
        self.filepath = filepath
    
    # reads in image input and converts it to grayscale
    def readImage (self):
        self.image = cv2.imread(self.filepath)
        self.convertedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    # uses the cascade to detect the faces within the given image
    def setFaces(self):
        self.faces = self.cascade.detectMultiScale(self.convertedImage, scaleFactor = 1.05, minNeighbors = 5, minSize = (30, 30), flags = None)

    # prints number of faces - isn't necessary to functionality, more for sanity checks
    def printNumFaces(self):
        num_faces = len(self.faces)
        print(f"Detected {num_faces} faces\n")

    # handles drawing the green rectangle around the detected faces
    # also crops and saves the image (should use a naming scheme in future for saving images)
    def drawRectangleImage(self):
        for (x,y,w,h) in self.faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.image = self.image[y:y+h, x:x+w]
        cv2.imwrite("image.png", self.image)
    
    # handles drawing the green rectangle around detected faces from a video feed
    def drawRectangleVideo(self):
        for (x,y,w,h) in self.faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    # handles video input, output, and facial detection
    def captureVideo(self):
        while True:
            ret, self.image = self.video.read()
            self.convertedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.setFaces()
            self.drawRectangleVideo()
            cv2.imshow("Press 'q' to take a photo and end video capture", self.image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.drawRectangleImage()
                cv2.imshow("Captured Face", self.image)
                cv2.waitKey(0)
                break
    
    # calls related functions for facial detection (image)
    def detectFace(self):
        self.readImage()
        self.setFaces()
        self.printNumFaces()
        self.drawRectangleImage()

    # calls related functions for facial detection (video)
    def detectVideo(self):
        self.video = cv2.VideoCapture(0)
        self.captureVideo()
        self.video.release()
        cv2.destroyAllWindows()

# default cascade for face detection
# this cascade is a file gotten from haarcascades for OpenCV
cascade = "haarcascade_frontalface_default.xml"

# basic test code to ensure everything works independently
if __name__ == "__main__":
    captureType = 0
    while not captureType == 1 and not captureType == 2:
        captureType = int(input("Would you like to capture an image or a video?\n1. Image\n2. Video: "))
    if captureType == 1:
        filepath = input("Enter image file name: ")
        faceDetect = Face_Detect(cascade)
        faceDetect.setPath(filepath)
        faceDetect.detectFace()
    if captureType == 2:
        faceDetect = Face_Detect(cascade)
        faceDetect.detectVideo()
