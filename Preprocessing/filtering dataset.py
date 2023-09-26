from PIL import Image as img
import os
import re
from exif import Image
import geopy.distance


def decimal_coord(coord, ref):
    decimal_degrees = coord[0] + coord[1] / 60 + coord[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
        img = Image(src)
        if img.has_exif:
            try:
                coords = (decimal_coord(img.gps_latitude, img.gps_latitude_ref),
                          decimal_coord(img.gps_longitude, img.gps_longitude_ref))
            except AttributeError:
                print('No Coordinates')
        else:
            print('The Image has no EXIF information')
            print(f"Image {src.name}, OS Version:{img.get('software', 'Not Known')} ------")
    return coords


# Filter the data based on their location
rootdir = "E:/Dataset/Projects"
count = 1
previous_coord = ()
destPath = "C:/Users/ASUS/OneDrive/Desktop/place/"
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir, file)
        coord = image_coordinates(path)
        if count == 1:
            previous_coord = coord
            image = img.open(path)
            new_image = image.resize((1920, 1280))
            new_image.save(destPath + str(count) + ".jpg", quality=95, **image.info)
            count += 1
            continue

        if geopy.distance.geodesic(coord, previous_coord).m > 7:
            previous_coord = coord
            image = img.open(path)
            new_image = image.resize((1920, 1280))
            new_image.save(destPath + str(count) + ".jpg", quality=95, **image.info)
            count += 1

# Filter the data based on their time
rootdir = "C:/Users/ASUS/OneDrive/Desktop/place/"
count = 1
for subdir, dirs, files in os.walk(rootdir):
    sorted_files = sorted(files, key=lambda x: int(x.split('.')[0]))
    print(files[0])
    for file in sorted_files:
        path = os.path.join(subdir, file)
        print(path)
        temp = re.split('/', path)
        number = re.split("\\.", temp[-1])
        print(number[0])
        if int(number[0]) % 3 == 1:
            image = img.open(path)
            new_image = image.resize((1920, 1280))
            new_image.save("E:/Dataset after filtering/" + str(count) + ".jpg", quality=95, **image.info)
            count += 1
