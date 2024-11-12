# Meyer Taffel | Redcastle Resources | 2024

import os, glob, shutil
from Util import data_io
from Util import util



###############################################
### Use this script to:
###
###   Transform the EXIF orientation from Spatial Explorer (SE) to Pix4DMatic (edits Yaw and Pitch)
###
###   Find all the images from the flights that are on the flight lines (they have EXIFs) and copy them to a new folder
###############################################




###############################################
### UPDATE THESE FILEPATHS FOR YOUR PROJECT ###
###############################################

# List of directories where the original images are stored (typically one directory per flight)
img_src_dirs = [
    r'E:\Taffel\TetherLogging2\TL2-unit47-RECON-5FFC85-2024-10-15-18-06-54\data\cam0',
    r'E:\Taffel\TetherLogging2\TL2-unit47-RECON-5FFC85-2024-10-15-19-03-51\data\cam0',
    r'E:\Taffel\TetherLogging2\TL2-unit47-RECON-5FFC85-2024-10-15-19-30-35\data\cam0',
]

# Source directory to put all the copied images
images_dir = r'E:\Taffel\TetherLogging2\Images\Unit47'

# Location of CSV file (exported by SE)
csv_filepath = r'E:\Taffel\TetherLogging2\Projects\unit47Exif.csv'

# Choose the suffix added to the new csv file
new_csv_name = "_transformed_yaw_pitch.csv"



###############################################
###   DO NOT EDIT UNLESS YOU'RE DEVEOPING   ###
###############################################


# Load EXIF data
print("Loading EXIF from CSV")

exif_data = data_io.get_csv(csv_filepath, skipHeaders=7, get_range=[0,7])
image_names = []


# Edit Yaw and Pitch and grab image names from CSV
print("Transforming Yaw and Pitch | SE -> pix4DMatic")

for row in exif_data:
    row[4] = util.transform_yaw(row[4])     # Transform yaw to match expected in pix4DMatic
    row[5] *= -1                            # Transform pitch by 180deg
    row += [0.050, 0.050, 2.000]            # Add default positional accuracy [in meters] to csv
    image_names.append(row[0])              # store the image names from the csv


# Copying images (IF HAS EXIF) from multiple SE directories to single directory
print(f"Copying images with EXIF to {images_dir}")

os.makedirs(images_dir, exist_ok=True) # Create the images dir if it doesn't already exist

count = 0 # record how many files copied
for img_src_dir in img_src_dirs:                                            # Loop through each image source directory 
    for image in glob.glob(os.path.join(img_src_dir, '*.jpg')):             # Get each image path
        image_name = os.path.basename(image)                                # Extract image name
        if image_name in image_names:                                       # Only copy if image has EXIF info from CSV
            if os.path.join(images_dir, image_name) in glob.glob(os.path.join(images_dir, '*.jpg')): # Check if image already exists in images_directory
                print(f'Skipping \{image_name} It already exists in {images_dir}')
            else:
                print(f'copying \{image_name} to {images_dir}')
                shutil.copy(image, images_dir) # copy image to new directory
                count += 1
print(f"\nCopying complete. Images at: {images_dir}\nCopied: {count} Skipped: {len(image_names)-count}")


# Create a CSV with the transformed EXIF data
if exif_data:
    new_csv_filepath = csv_filepath.replace('.csv', new_csv_name)                                                           # Rename new csv file
    headers = "Filename, Latitude, Longitude, Altitude, Yaw, Pitch, Roll, Accuracy X, Accuracy Y, Accuracy Z".split(", ")   # Set headers
    data_io.write_csv(new_csv_filepath, exif_data, headers=headers)                                                         # Write new CSV
    print(f"\nEdited CSV at: {new_csv_filepath}")

print("\nScript completed succesfully. Check logs above for source directory of outputs.")