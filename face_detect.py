import cv2
import numpy

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

filepath = input("Enter image file name: ")

image = cv2.imread(filepath)
grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(grayscale, scaleFactor = 1.05, minNeighbors = 5, minSize = (30, 30), flags = None)

num_faces = len(faces)

print(f"Detected {num_faces} faces\n")

for (x,y,w,h) in faces:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
image = image[y:y+h, x:x+w]

cv2.imwrite("image.png", image)
cv2.waitKey(0)