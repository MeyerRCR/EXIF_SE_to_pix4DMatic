from Util import data_io
from Util import helpers as hlp

def transform_yaw(yaw):
    if yaw < 0:
        return (yaw*-1) - 180
    return (yaw*-1) + 180

headers = "Filename, Latitude, Longitude, Altitude, Yaw, Pitch, Roll".split(", ")

exif_data = data_io.get_csv(r'.\test_data\unit26Exif.csv', skipHeaders=8, get_range=[0,7])

for row in exif_data:
    row = hlp.array_safe_str_to_float(row)
    row[4] = transform_yaw(row[4])
    row[5] *= -1

if exif_data:
    data_io.write_csv(r'.\test_data\unit26Exif_newY.csv', exif_data, headers=headers)