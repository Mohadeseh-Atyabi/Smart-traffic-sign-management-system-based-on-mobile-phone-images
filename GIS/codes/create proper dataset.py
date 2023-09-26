import os
import math
import numpy as np
import xlsxwriter
import pandas as pd
from GPS_of_objects import get_gps_coordinates


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth given their decimal degree latitude and longitude,
    using the Haversine formula.

    Arguments:
    lat1 -- latitude of point 1 in decimal degrees
    lon1 -- longitude of point 1 in decimal degrees
    lat2 -- latitude of point 2 in decimal degrees
    lon2 -- longitude of point 2 in decimal degrees

    Returns:
    The distance between the two points in kilometers.
    """

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles.
    distance = c * r

    return distance


id_to_class = {0: 'background', 1: 'Area with Camera', 2: 'At the junction', 3: 'Give Way', 4: 'Keep Left',
               5: 'Keep Right', 6: 'Maximum Speed', 7: 'No Entry', 8: 'No Stopping', 9: 'No Waiting',
               10: 'No through road', 11: 'On approaches to junctions', 12: 'One-way Traffic', 13: 'Pedestrian Route',
               14: 'Sharp deviation of Route (group)', 15: 'Sharp deviation of route (single)', 16: 'Stop',
               17: 'Taxi Station', 18: 'Transport with Crane'
               }

# First we have to filter the repetitive signs in continues files
img_directory = "C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/test_data"
image_files = sorted([os.path.join(img_directory, f) for f in os.listdir(img_directory) if f.endswith('.jpg')])
threshold = 10
# Loop through the image files in pairs
# total_list = [[image_name, class_id, [(lat, lon)]]]
total_list = []
for row in range(0, len(image_files) - 1):
    # Read the two images
    img_name = image_files[row].split(".")[0].split("\\")[-1]
    IMG_PATH = f'C:/Users/ASUS/OneDrive/Desktop/test_data/{img_name}.jpg'
    print(IMG_PATH)
    img_id = img_name.split('[')[-1].split(']')[0]
    # img_path = f'../../codes/TrainModel/test_data/{img_name}.jpg'
    print(img_name)
    # format of distances is [class_id, confidence, x, y, w, h, tvec]
    info_of_obj = np.load(f'C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/camera calibration/distance in images/{img_name}.npy', allow_pickle=True)
    for obj in info_of_obj:
        class_id = obj[0]
        confidence = obj[1]
        x = obj[2]
        y = obj[3]
        w = obj[4]
        h = obj[5]
        tvec = obj[6]

        location, point1, point2 = get_gps_coordinates(image_files[row], image_files[row + 1], tvec[0][0] / 100, tvec[2][0] / 100)
        print(location)

        if len(total_list) == 0:
            arr = [img_name, class_id, id_to_class[int(class_id)], [point1], IMG_PATH]
            total_list.append(arr)
        else:
            observed = False
            for j in reversed(total_list):
                # print(j)
                # We search for last 10 images
                temp_img_id = j[0].split('[')[-1].split(']')[0]
                if int(img_id) - int(temp_img_id) <= 5:
                    if j[1] == class_id:
                        if abs(haversine(point1[0], point1[1], point2[0], point2[1]) * 1000) < threshold:
                            observed = True
                            j[0] = img_name
                            j[4] = IMG_PATH
                            j[3].append(point1)

            if not observed:
                arr = [img_name, class_id, id_to_class[int(class_id)], [point1], IMG_PATH]
                total_list.append(arr)

res = [[ele for ele in list if len(list[3]) > 2] for list in total_list]
total_list = [lst for lst in res if len(lst) > 0]

for lists in total_list:
    df = pd.DataFrame(lists[3])
    lat = df[0].mean()
    lon = df[1].mean()
    del lists[3]
    lists.append(lat)
    lists.append(lon)

print("total list: ", total_list)

with xlsxwriter.Workbook('test.xlsx') as workbook:
    worksheet = workbook.add_worksheet()

    worksheet.write_row(0, 0, ['image_name', 'class_id', 'class_name', 'image_path', 'latitude', 'longitude'])
    for row_num, data in enumerate(total_list):
        print("data: ", data)
        worksheet.write_row(row_num+1, 0, data)



