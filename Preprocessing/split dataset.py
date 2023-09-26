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

# Rename images
imageDir = "C:/Users/ASUS/Downloads/project-10-at-2023-06-30-09-31-526222b4/images"
for subdir, dirs, files in os.walk(imageDir):
    for file in files:
        path = os.path.join(subdir, file)
        filename = file.split('-')
        newPath = os.path.join(subdir, filename[1])
        os.rename(path, newPath)

# Rename annotation files
annotationDir = "C:/Users/ASUS/Downloads/project-10-at-2023-06-30-09-31-526222b4/Annotations"
for subdir, dirs, files in os.walk(annotationDir):
    for file in files:
        path = os.path.join(subdir, file)
        filename = file.split('-')
        newPath = os.path.join(subdir, filename[1])

        mytree = ET.parse(path)
        myroot = mytree.getroot()
        # iterating through the filename values.
        for name in myroot.iter('filename'):
            # updates the price value
            filename = name.text.split('-')
            name.text = filename[1]
            print(name.text)
        mytree.write(newPath)

counter = 1
for subdir, dirs, files in os.walk(imageDir):
    for file in files:
        # To split the data into train and test, we focus on counter and change the destination directory based on it
        destDir = "E:/splitted dataset/train" if counter <= 1407 else "E:/splitted dataset/test"
        destPath = os.path.join(destDir, file)

        sourcePath = os.path.join(subdir, file)
        shutil.copyfile(sourcePath, destPath)

        filename = file.split('.')
        tempName = os.path.join(annotationDir, filename[0] + '.xml')
        if path.exists(tempName):
            destPath = os.path.join(destDir, filename[0] + '.xml')
            shutil.copyfile(tempName, destPath)

        counter += 1

for subdir, dirs, files in os.walk("C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/Dataset/test"):
    for file in files:
        splitted = file.split(".")
        if splitted[-1] == "jpg":
            if not os.path.exists(os.path.join(subdir, splitted[0] + ".xml")):
                os.remove(os.path.join(subdir, file))

for subdir, dirs, files in os.walk("E:/additional dataset with labels/Annotations"):
    for file in files:
        splitted = file.split("-")
        if len(splitted) >= 2:
            os.remove(os.path.join(subdir, file))
