import cv2
import os
from PIL import Image

#MAKE SURE TO RUN THIS IN THE DIRECTORY THAT HAS BOTH EXTRACTED CHILE AND GREEK DB 
#(or adjust the if statements to save properly)


#main directory
directory = os.getcwd()

#new directories to save the converted images
directory_names = ["Chile Drunk", "Chile Sober", "Greek Drunk", "Greek Sober"]
for dirname in directory_names:
    if not os.path.exists(dirname):
        os.mkdir(dirname)

#recursively go through directory
for subdir, dirs, files in os.walk(directory):
    for file in files:
        filepath = subdir + os.sep + file

        if filepath.endswith(".jpg") or filepath.endswith(".png"): #only images to be inspected (no jpegs are present)
            new_file_name = file[:-4]
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            converted_image = cv2.applyColorMap(img, cv2.COLORMAP_MAGMA)
            #converted_image = cv2.applyColorMap(img, cv2.COLORMAP_INFERNO)
            #converted_image = cv2.applyColorMap(img, cv2.COLORMAP_PLASMA)
            print(converted_image.shape)
            if "ExtractedChile_DB" in filepath:
                if "Drunk" in filepath:
                    new_file_path = directory + "\Chile Drunk\\"
                elif "Sober" in filepath:
                    new_file_path = directory + "\Chile Sober\\"
            elif "ExtractedGreek_DB" in filepath:
                if "Drunk" in filepath:
                    new_file_path = directory + "\Greek Drunk\\"
                elif "Sober" in filepath:
                    new_file_path = directory + "\Greek Sober\\"
            saving_file_path = new_file_path + new_file_name + ".jpg"
            cv2.imwrite(saving_file_path, converted_image)
            test_img = cv2.imread(saving_file_path, cv2.IMREAD_COLOR)
            print(test_img.shape) #checking new output shape
            
'''
For testing only
'''
#img = cv2.imread("test_image.jpeg", cv2.IMREAD_GRAYSCALE)

#converted_image = cv2.applyColorMap(img, cv2.COLORMAP_MAGMA)
#print(img.shape)
#print(converted_image.shape)
#cv2.imshow('stinky', img)
#cv2.waitKey(0)