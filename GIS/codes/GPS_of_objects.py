import numpy as np
from exif import Image
import math


def get_gps_location(first_gps_coord, second_gps_coord, distance, angle):
    lat1, long1 = first_gps_coord
    lat2, long2 = second_gps_coord

    R = 6371000  # radius of the Earth in meters

    # calculate the distance between the two GPS coordinates
    delta_lat = math.radians(lat2 - lat1)
    delta_long = math.radians(long2 - long1)
    a = math.sin(delta_lat/2) * math.sin(delta_lat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(delta_long/2) * math.sin(delta_long/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c

    # calculate the bearing between the two GPS coordinates
    bearing = math.atan2(math.sin(delta_long) * math.cos(math.radians(lat2)), math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) - math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(delta_long))

    # calculate the new GPS coordinates of the object
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    bearing += angle
    new_lat = math.asin(math.sin(lat1) * math.cos(distance/R) + math.cos(lat1) * math.sin(distance/R) * math.cos(bearing))
    new_long = long1 + math.atan2(math.sin(bearing) * math.sin(distance/R) * math.cos(lat1), math.cos(distance/R) - math.sin(lat1) * math.sin(new_lat))
    new_lat = math.degrees(new_lat)
    new_long = math.degrees(new_long)

    return new_lat, new_long


def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref == "W":
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def get_gps_coordinates(first_path, second_path, dist_x, dist_y):

    with open(first_path, 'rb') as src:
        img = Image(src)
        lat_start_deg = img.gps_latitude
        lat_ref = img.gps_latitude_ref
        lon_start_deg = img.gps_longitude
        lon_ref = img.gps_longitude_ref

    with open(second_path, 'rb') as src:
        img1 = Image(src)
        lat_start_deg1 = img1.gps_latitude
        lat_ref1 = img1.gps_latitude_ref
        lon_start_deg1 = img1.gps_longitude
        lon_ref1 = img1.gps_longitude_ref

    # Distance to move in x and y directions
    distance_x_meters = -dist_y
    distance_y_meters = -dist_x

    # Calculate straight-line distance
    distance = np.sqrt(distance_x_meters**2 + distance_y_meters**2)

    # Calculate initial bearing
    bearing = np.arctan2(distance_x_meters, distance_y_meters)

    point1 = (decimal_coords(lat_start_deg, lat_ref), decimal_coords(lon_start_deg, lon_ref))
    point2 = (decimal_coords(lat_start_deg1, lat_ref1), decimal_coords(lon_start_deg1, lon_ref1))
    location = get_gps_location(point1, point2, distance, bearing)

    return location, point1, point2


# print(get_gps_coordinates("C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/test_data/20230303_082328[373].jpg", "C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/TrainModel/test_data/20230303_082328[374].jpg", 2.5, 4.6))
