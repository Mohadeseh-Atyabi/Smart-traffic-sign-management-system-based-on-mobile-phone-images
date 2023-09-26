import os.path
import shutil
from os import path
import xml.etree.ElementTree as ET

'''
Pascal VOC Format:

    Split the dataset into train and test sets. Our total dataset has 1759 images.
    We use 80% of the data for training (1407 images) and other 20% for testing (352 images).
    First of all we have to rename the images and their annotations and then split them. 
'''

# Rename annotation files
for subdir, dirs, files in os.walk("C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/Dataset/train"):
    for file in files:
        path = os.path.join(subdir, file)
        filename = file.split(".")
        if filename[-1] == 'xml':
            mytree = ET.parse(path)
            myroot = mytree.getroot()
            # iterating through the filename values.
            for obj in myroot.findall('.//object[name="Stop"]'):
                print(file)
                myroot.remove(obj)
            mytree.write(path)