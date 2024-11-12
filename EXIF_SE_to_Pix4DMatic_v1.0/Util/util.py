def array_safe_str_to_float(arr):
    for i, a in enumerate(arr):
        try:
            arr[i] = float(a)
        except:
            arr[i] = a.strip()
    return arr

def transform_yaw(yaw):
    if yaw < 0:
        return (yaw*-1) - 180
    return (yaw*-1) + 180