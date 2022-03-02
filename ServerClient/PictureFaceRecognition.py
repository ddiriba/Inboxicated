import face_recognition
import cv2
import numpy as np
import os

class PictureFaceRecognition:
        def __init__(self, existing_db_dictionary):
                if current_face_encodings:
                        self.people_dictionary = existing_db_dictionary #returns phone as keys, encoding as values
                else:
                        print("Error!")
                self.recognized_face = None

        def delete_entry(self, phone_key):
                self.people_dictionary.pop(phone_key)

        def add_user_face_encoding(self, phone_key, encoding_val):
                self.people_dictionary[phone_key] = encoding_val

        def test_recognize_face(self, face_arr):#this function is now getting an array
                face_distances = face_recognition.face_distance(self.people_dictionary.values(), face_arr)
                print(face_distances)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                        self.recognized_face = self.people_dictionary.keys()[best_match_index]
                print("Recognized: ", self.recognized_face)
                return self.recognized_face

        def recognize_face(self, frame):
                unknown_image = frame[:,:,::-1]
                print("Image type: ", type(unknown_image))
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)
                print("Encoding type: ", type(unknown_face_encoding))
                print("Is encoding same as image? ", np.array_equal(unknown_image, unknown_face_encoding))
                matches = face_recognition.compare_faces(self.people_dictionary.values(), unknown_face_encoding)
                print(matches)
                face_distances = face_recognition.face_distance(self.people_dictionary.values(), unknown_face_encoding)
                print(face_distances)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                        self.recognized_face = self.people_dictionary.keys()[best_match_index]
                print("Recognized: ", self.recognized_face)
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
        face_recognizer.recognize_face("biden2.jpg")
