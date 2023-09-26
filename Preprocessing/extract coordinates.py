from exif import Image
import geopy.distance


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
        img = Image(src)
        if img.has_exif:
            try:
                coords = (decimal_coords(img.gps_latitude,
                          img.gps_latitude_ref),
                          decimal_coords(img.gps_longitude,
                          img.gps_longitude_ref))
            except AttributeError:
                print('No Coordinates')
        else:
            print('The Image has no EXIF information')
            print(f"Image {src.name}, OS Version:{img.get('software', 'Not Known')} ------")
    return coords


coords1 = image_coordinates("C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/test_data/20230303_082003[1].jpg")
coords2 = image_coordinates("E:/Dataset/Projects/20221007_094824/20221007_095040[137].jpg")

print(coords1)
print(coords2)

if geopy.distance.geodesic(coords1, coords2).m < 7:
    print(":)")
