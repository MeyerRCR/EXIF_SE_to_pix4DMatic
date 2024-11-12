import os, glob, shutil

src_dir = r'E:\Taffel\TetherLogging2\unit47_images'
image = r'E:\Taffel\TetherLogging2\unit47_images\00000000000000003282767105411468_1413050838265238_1413050838271360.jpg'

# if not images in images_dir #make this work
if image not in glob.glob(os.path.join(src_dir, '*.jpg')):
    print(f'copying {image} to {src_dir}')
    # shutil.copy(image, images_dir) # copy image to new directory
else:
    print(f'Skipping {image}. It already exists in {src_dir}')
