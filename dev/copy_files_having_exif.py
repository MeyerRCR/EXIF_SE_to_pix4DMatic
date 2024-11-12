import os
import glob
import shutil

from Util import data_io

# Get list of images from Spatial Explorer Export EXIF to CSV
csv_filepath = r'.\test_data\unit26Exif.csv' # CHANGE to match csv filelocation
filenames_nested = data_io.get_csv(csv_filepath, skipHeaders=8, get_range=[0,1]) # you can adjust variables if the CSV format changes

dest_dir = r'E:\Taffel\TetherLogging2\Images\Unit26'

src_dirs = [
    r'E:\Taffel\TetherLogging2\TL2-unit26-RECON-5FFC85-2024-10-14-22-06-06\data\cam0',
    r'E:\Taffel\TetherLogging2\TL2-unit26-RECON-5FFC85-2024-10-14-22-29-49\data\cam0',
]

for src_dir in src_dirs:
    filenames = []
    for file in filenames_nested:
        filenames.append( os.path.join(src_dir, file[0]) )

    for image in glob.glob(os.path.join(src_dir, '*.jpg')):
        if image in filenames:
            print(f'copying {image} to {dest_dir}')
            shutil.copy(image, dest_dir)
