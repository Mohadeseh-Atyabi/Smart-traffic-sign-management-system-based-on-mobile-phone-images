import os
import xml.etree.ElementTree as ET
import numpy as np

directory = "C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/camera calibration/final test/Annotations"
name_to_id = {'chessboard': 0, 'sticker': 1, 'closet': 2}

for subdir, dirs, files in os.walk(directory):
    for file in files:
        array_to_save = []
        path = os.path.join(subdir, file)
        tree = ET.parse(path)
        root = tree.getroot()
        for obj in root.iter('object'):
            bndbox = obj.find('bndbox')

            class_name = name_to_id[obj.find('name').text]
            confidence = 0.66
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            width = int(bndbox.find('xmax').text) - int(bndbox.find('xmin').text)
            height = int(bndbox.find('ymax').text) - int(bndbox.find('ymin').text)

            a = [class_name, confidence, int(xmin), int(ymin), width, height]
            print(a)
            array_to_save.append(a)

        np.save(f'../detections/detections_{file.split(".")[0]}.npy', array_to_save)
        print(f'detections_{file.split(".")[0]}.npy', 'saved!')
