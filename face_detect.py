import cv2
import numpy

class Face_Detect:

    image = None
    convertedImage = None
    faces = None
    filepath = None
    video = None

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
    
    def drawRectangleVideo(self):
        for (x,y,w,h) in self.faces:
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        

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

    def detectFace(self):
        self.readImage()
        self.setFaces()
        self.printNumFaces()
        self.drawRectangleImage()

    def detectVideo(self):
        self.video = cv2.VideoCapture(0)
        self.captureVideo()
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
