import face_recognition
import cv2
import numpy as np
import os
#from Thermal.thermal import SeekPro

# code based on https://github.com/ageitgey/face_recognition/tree/master/examples

class Face_Recognition:
    def __init__(self, folder_address, testing_face_rec=False):
        self.folder_address = folder_address
        #cam = SeekPro()
        #self.video_capture = cam
        self.currently_saved_faces_encodings, self.currently_saved_faces_names = self.load_faces()
        self.test = testing_face_rec

    def load_faces(self):
        if os.path.isdir(self.folder_address):
            print(self.folder_address)
            face_encodings_list = []
            faces_names_list = []
            for image_file in os.listdir(self.folder_address):
                print(faces_names_list)
                cwd = os.path.join(os.getcwd(), "current_faces")
                cwd = os.path.join(cwd, image_file)
                
                #print path + image file name
                #print(cwd)
                
                im = face_recognition.load_image_file(cwd)
                im_face_encoding = face_recognition.face_encodings(im)[0]
                face_encodings_list.append(im_face_encoding)
                faces_names_list.append(os.path.splitext(image_file)[0])
            return face_encodings_list, faces_names_list

    def recognize_face(self):
        face_locations = []
        while True:
            ret, frame = self.video_capture.read()
            rgb_frame = frame[:,:,::-1]
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.currently_saved_faces_encodings, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(self.currently_saved_faces_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.currently_saved_faces_names[best_match_index]
                if self.test:
                    cv2.rectangle(frame, (left,top), (right, bottom), (0,0,255), 2)
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            if self.test:
                cv2.imshow("Face Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Found ", name)
                break
        self.video_capture.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    images_path = os.path.join(os.getcwd(), "current_faces")
    print(os.getcwd())
    print(images_path)
    face_recognizer = Face_Recognition(images_path, testing_face_rec=True)        
    print("Finished loading known faces.")
    face_recognizer.recognize_face()
