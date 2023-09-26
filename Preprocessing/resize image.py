from PIL import Image
import os

source_directory = "C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/camera calibration/final test"
destination_directory = "C:/Users/ASUS/OneDrive/Desktop/Folders/BS Project/codes/camera calibration/final test"
for subdir, dirs, files in os.walk(source_directory):
    for file in files:
        print(file)
        source_path = os.path.join(subdir, file)
        # Open the image
        img = Image.open(source_path)

        # Resize the image
        new_img = img.resize((1920, 1280))

        destination_path = os.path.join(destination_directory, file)
        # Save the resized image as PNG format
        new_img.save(destination_path, quality=95, **new_img.info)
