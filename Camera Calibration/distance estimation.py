import os
import cv2
import numpy as np
from screeninfo import get_monitors


def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None


# Load previously saved data
with np.load('CameraParameters.npz') as file:
    mtx, dist, rvecs, tvecs = [file[i] for i in ('cameraMatrix', 'distortion', 'rotation', 'translation')]

class_to_id = {'background': 0, 'Area with Camera': 1, 'At the junction': 2, 'Give Way': 3, 'Keep Left': 4,
               'Keep Right': 5, 'Maximum Speed': 6, 'No Entry': 7, 'No Stopping': 8, 'No Waiting': 9,
               'No through road': 10, 'On approaches to junctions': 11, 'One-way Traffic': 12, 'Pedestrian Route': 13,
               'Sharp deviation of Route (group)': 14, 'Sharp deviation of route (single)': 15, 'Stop': 16,
               'Taxi Station': 17, 'Transport with Crane': 18
               }

id_to_size = {0: (0, 0), 1: (45, 45), 2: (180, 180), 3: (60, 60), 4: (37, 37), 5: (25, 25), 6: (60, 60), 7: (40, 40),
              8: (40, 40), 9: (40, 40), 10: (60, 60), 11: (180, 240), 12: (60, 60), 13: (60, 60), 14: {'small': (20, 60), 'big': (33, 50)},
              15: (45, 60), 16: (40, 40), 17: (50, 75), 18: {'big': (50, 75), 'small': (50, 33)}}

threshold = 0.8
directory = "C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/camera calibration/detections"
for subdir, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.npy'):
            # This is the total array that stores information about each objects for creating proper dataset for GIS
            total_arr = []
            print(file)
            # Load object detection results
            path = os.path.join(subdir, file)
            detections = np.load(path)

            name = file.split('.')[0].split('detections_')[1]
            image = cv2.imread(
                f"C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/test_data/{name}.jpg")
            # image = cv2.imread(f"C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/camera calibration/test multiple obj/images/{name}.jpg")

            # Find object poses using solvePnP
            for detection in detections:
                class_id, confidence, x, y, w, h = detection
                if class_id == 18:
                    if w > h:
                        width, height = 50, 33
                    else:
                        width, height = 50, 75
                elif class_id == 14:
                    if h/w > 2:
                        width = 20
                        height = 60
                    else:
                        width = 33
                        height = 50
                elif class_id == 13:
                    if h/w > 1.5:
                        continue
                    else:
                        width = id_to_size[class_id][0]
                        height = id_to_size[class_id][1]
                else:
                    print(class_id)
                    width = id_to_size[class_id][0]
                    height = id_to_size[class_id][1]
                # Define 3D coordinates of the object points [x, y, z]
                object_points = np.array([[0, 0, 0], [width, 0, 0], [width, height, 0], [0, height, 0]],
                                         dtype=np.float32)
                # print(object_points)

                if confidence > threshold:
                    # Find object pose using solvePnP
                    image_points = np.array([[x, y + h], [x + w, y + h], [x + w, y], [x, y]], dtype=np.float32)
                    # print(image_points)
                    ret, rvec, tvec = cv2.solvePnP(object_points, image_points, mtx, dist)
                    # Build an array for each object detected in image that is used in "create proper dataset"
                    arr = [class_id, confidence, x, y, w, h, tvec]
                    total_arr.append(arr)
                    # Calculate distance to object
                    distance = np.linalg.norm([tvec[1][0], tvec[2][0]])
                    print(tvec)
                    print(f'{class_id}: {distance:.2f} cm')
                    print(x, y, w, h, image.shape)
                    cv2.rectangle(image,
                                  (int(x), int(y)),
                                  (int(x + w), int(y + h)),
                                  (0, 0, 255), 2)

                    cv2.putText(image, f"{get_key_from_value(class_to_id, class_id)}",
                                (int(x), int(y) - 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),
                                2)

                    cv2.putText(image, f"x: {tvec[0]}",
                                (int(x), int(y) - 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),
                                2)

                    cv2.putText(image, f"z: {tvec[2]}",
                                (int(x), int(y) - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),
                                2)

            # Get the primary monitor
            monitor = get_monitors()[0]
            screen_res = monitor.width - 10, monitor.height - 10
            # Resize the image to the screen size
            resized_img = cv2.resize(image, screen_res)
            # Show the image with full size
            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('image', resized_img)

            # Wait for a key event
            cv2.waitKey(0)

            # Destroy all windows
            cv2.destroyAllWindows()

            np.save(f'C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/camera calibration/distance in images/{name}.npy', np.array(total_arr, dtype=object))
            print(".np file saved")