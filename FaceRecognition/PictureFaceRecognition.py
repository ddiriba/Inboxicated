import face_recognition
import cv2
import numpy as np
import os

class PictureFaceRecognition:
        def __init__(self, folder_address, current_face_encodings):
                self.folder_address = folder_address
                if current_face_encodings:
                        self.current_faces_encodings = current_face_encodings
                else:
                        self.current_faces_encodings, self.names = self.load_faces()
                self.recognized_face = None
        
        def load_faces(self):
                # DAWIT find a way to return a list of encodings
                if os.path.isdir(self.folder_address):
                        face_encodings_list = []
                        faces_names_list = []
                        for image_file in os.listdir(self.folder_address):
                                cwd = os.path.join(self.folder_address, image_file)
                                print(image_file)
                                im = face_recognition.load_image_file(cwd)
                                im_face_encoding = face_recognition.face_encodings(im)[0]
                                print(type(im_face_encoding))
                                face_encodings_list.append(im_face_encoding)
                                faces_names_list.append(os.path.splitext(image_file)[0])
                        return face_encodings_list, faces_names_list

        def recognize_face(self, frame):
                #frame = frame[:,:,::-1]
                print("Frame type: ", type(frame))
                unknown_image = face_recognition.load_image_file(frame)
                print("Image after converting type: ", type(unknown_image))
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
                print("Encoding type: ", type(unknown_face_encoding))
                print("Is encoding same as image? ", np.array_equal(unknown_image, unknown_face_encoding))
                matches = face_recognition.compare_faces(self.current_faces_encodings, unknown_face_encoding)
                print(matches)


if __name__ == "__main__":
        images_path = os.path.join(os.getcwd(), "current_faces")
        print(os.getcwd())
        print(images_path)
        print(repr(images_path))
        face_recognizer = PictureFaceRecognition(images_path, None)        
        print("Finished loading known faces.")
        face_recognizer.recognize_face("biden2.jpg")
