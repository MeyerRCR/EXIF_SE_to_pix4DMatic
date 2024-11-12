Meyer Taffel | Redcastle Resources | 2024

#################################################

This python tool converts orientation values from Spatial Explorer v8 (SE) to pix4DMatic.

In SE, export a CSV of the EXIF data for active images.
This script creates a csv with the corrected yaw pitch roll values for pix4DMatic.
Additionally, the script will copy all the active* images from the src directories to a single directory for easy uploading in pix4DMatic.

*IE on a flightline

#################################################

Dependancies:
None

Setup:
Update filepaths in /Exif_SE_to_Pix4DMatic_v1.1.py (@line 21)

Run:
python .\EXIF_SE_to_pix4D_v1.1.py