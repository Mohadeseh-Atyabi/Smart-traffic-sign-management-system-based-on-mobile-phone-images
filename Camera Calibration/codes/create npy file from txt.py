import os
import json
import numpy as np

directory = "C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/test_bndbox"
threshold = 0.8

for subdir, dirs, files in os.walk(directory):
    for file in files:
        # load dictionary from file
        path = os.path.join(subdir, file)
        with open(path, 'r') as f:
            my_dict_serializable = json.load(f)

        # convert lists back to numpy arrays
        my_dict = {}
        for k, v in my_dict_serializable.items():
            if isinstance(v, list):
                my_dict[k] = np.array(v)
            else:
                my_dict[k] = v
        # print the resulting dictionary
        # print(my_dict)
        boxes = my_dict['boxes']
        scores = my_dict['scores']
        labels = my_dict['labels']
        print(labels)
        array_to_save = []

        for i, score in enumerate(scores):
            # print(i[0], i[1])
            if score >= threshold:
                coordinates = boxes[i]
                class_name = labels[i]
                confidence = scores[i]
                xmin = coordinates[0]
                ymin = coordinates[1]
                width = coordinates[2] - coordinates[0]
                height = coordinates[3] - coordinates[1]

                a = [class_name, confidence, int(xmin), int(ymin), width, height]
                array_to_save.append(a)
                # print(array_to_save)

        np.save(f'C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/camera calibration/detections/detections_{file.split(".")[0]}.npy', array_to_save)
        print(f'detections_{file.split(".")[0]}.npy', 'saved!')
