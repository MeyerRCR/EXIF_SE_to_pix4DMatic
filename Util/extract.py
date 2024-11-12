# Map [lat, lon, alt] to dict
def geo(pos):
    return {
        "latitude": pos[0],
        "longitude": pos[1],
        "altitude": pos[2],
    }

# Map [yaw, pitch, roll] to dict
def ypr(ornt):
    return {
        "yaw": ornt[0],
        "pitch": ornt[1],
        "roll": ornt[2],
    }