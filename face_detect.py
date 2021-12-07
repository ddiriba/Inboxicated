import cv2
import numpy

class Face_Detect:

    image = None
    convertedImage = None
    faces = None
    filepath = None
    video = cv2.VideoCapture(0)

    def __init__(self, cascade):
        self.cascade = cv2.CascadeClassifier(cascade)

    def setPath(self, filepath):
        self.filepath = filepath

    def readImage (self):
        self.image = cv2.imread(self.filepath)
        self.convertedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def setFaces(self):
        self.faces = self.cascade.detectMultiScale(self.convertedImage, scaleFactor = 1.05, minNeighbors = 5, minSize = (30, 30), flags = None)

    def printNumFaces(self):
        num_faces = len(self.faces)
        print(f"Detected {num_faces} faces\n")

    def drawRectangleImage(self):
        for (x,y,w,h) in self.faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            self.image = self.image[y:y+h, x:x+w]
        cv2.imwrite("image.png", self.image)
        cv2.waitKey(0)
    
    def drawRectangleVideo(self):
        for (x,y,w,h) in self.faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('Video', self.image)

    def captureVideo(self):
        print("To exit video capture, press 'q'")
        while True:
            ret, self.image = self.video.read()
            self.convertedImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.setFaces()
            self.drawRectangleVideo()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



    def detectFace(self):
        self.readImage()
        self.setFaces()
        self.printNumFaces()
        self.drawRectangleImage()

    def detectVideo(self):
        self.video.release()
        cv2.destroyAllWindows()
        pass

cascade = "haarcascade_frontalface_default.xml"

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
