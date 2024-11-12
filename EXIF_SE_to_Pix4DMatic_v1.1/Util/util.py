# Given array of strings, returns new array with numerical strings converted to float
def array_safe_str_to_float(arr):
    for i, a in enumerate(arr):
        try:
            arr[i] = float(a)
        except:
            arr[i] = a.strip()
    return arr

# Transform yaw from SE to Pix4DMatic
# Spatial Explorer v8 Convention:   no yaw is 0, left yaw is -180... right yaw is +1...
# Pix4DMatic Convention:            no yaw is 0, left yaw is -1...   right yaw is +1...
def transform_yaw(yaw):
    if yaw < 0:
        return (yaw*-1) - 180
    return (yaw*-1) + 180