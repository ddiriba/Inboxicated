import face_recognition
import cv2
import numpy as np
import os

class PictureFaceRecognition:
        def __init__(self, existing_db_dictionary):
                if existing_db_dictionary:
                        self.people_dictionary = existing_db_dictionary #returns phone as keys, encoding as values
                else:
                        self.people_dictionary = {}
                self.recognized_face = None

        def delete_entry(self, phone_key):
                self.people_dictionary.pop(phone_key)

        def add_user_face_encoding(self, phone_key, encoding_val):
                self.people_dictionary[phone_key] = encoding_val
        
        def check_if_frame_contains_face(self, image_encoding):
                if image_encoding:
                        print("contains face")
                        return True
                else:
                        print("there's no face in the image")
                        return False

        def recognize_face(self, frame):
                unknown_image = frame
                matches = face_recognition.compare_faces(list(self.people_dictionary.values()), unknown_image)
                face_distances = face_recognition.face_distance(list(self.people_dictionary.values()), unknown_image)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                        self.recognized_face = list(self.people_dictionary.keys())[best_match_index]
                # remeber to set self.recognized_face to none
                return self.recognized_face

        def reset_recognized_face(self):
                self.recognized_face = None


if __name__ == "__main__":
        images_path = os.path.join(os.getcwd(), "current_faces")
        print(os.getcwd())
        print(images_path)
        print(repr(images_path))
        face_recognizer = PictureFaceRecognition(images_path, None)        
        print("Finished loading known faces.")
        #face_recognizer.recognize_face("biden2.jpg")
