import numpy as np

WGS84_a = 6378137.0
WGS84_b = 6356752.314245

# Helper function for YPR_to_OPK gets the xyz position in wgs84 given lat lon alt
def ecef_from_lla(lat, lon, alt: float):
    """
    Compute ECEF XYZ from latitude, longitude and altitude.

    All using the WGS84 model.
    Altitude is the distance to the WGS84 ellipsoid.
    Check results here http://www.oc.nps.edu/oc2902w/coord/llhxyz.htm

    >>> lat, lon, alt = 10, 20, 30
    >>> x, y, z = ecef_from_lla(lat, lon, alt)
    >>> np.allclose(lla_from_ecef(x,y,z), [lat, lon, alt])
    True
    """
    a2 = WGS84_a ** 2
    b2 = WGS84_b ** 2
    lat = np.radians(lat)
    lon = np.radians(lon)
    L = 1.0 / np.sqrt(a2 * np.cos(lat) ** 2 + b2 * np.sin(lat) ** 2)
    x = (a2 * L + alt) * np.cos(lat) * np.cos(lon)
    y = (a2 * L + alt) * np.cos(lat) * np.sin(lon)
    z = (b2 * L + alt) * np.sin(lat)
    return x, y, z

def YPR_to_OPK(YPR, geo):
    opk = None

    if geo and "latitude" in geo and "longitude" in geo:
        ypr = np.array([None, None, None])

        try:
            # YPR conventions (assuming nadir camera)
            # Yaw: 0 --> top of image points north
            # Yaw: 90 --> top of image points east
            # Yaw: 270 --> top of image points west
            # Pitch: 0 --> nadir camera
            # Pitch: 90 --> camera is looking forward
            # Roll: 0 (assuming gimbal)

            ypr = np.array(
                [
                    float(YPR.get("yaw")),
                    float(YPR.get("pitch")),
                    float(YPR.get("roll")),
                ]
            )
            # ypr[1] += 90  # DJI's values need to be offset
        except ValueError:
            Print("Invalid YPR input")

        if np.all(ypr) is not None:
            ypr = np.radians(ypr)

            # Convert YPR --> OPK
            # Ref: New Calibration and Computing Method for Direct
            # Georeferencing of Image and Scanner Data Using the
            # Position and Angular Data of an Hybrid Inertial Navigation System
            # by Manfred Bäumker
            y, p, r = ypr

            # YPR rotation matrix
            cnb = np.array(
                [
                    [
                        np.cos(y) * np.cos(p),
                        np.cos(y) * np.sin(p) * np.sin(r) - np.sin(y) * np.cos(r),
                        np.cos(y) * np.sin(p) * np.cos(r) + np.sin(y) * np.sin(r),
                    ],
                    [
                        np.sin(y) * np.cos(p),
                        np.sin(y) * np.sin(p) * np.sin(r) + np.cos(y) * np.cos(r),
                        np.sin(y) * np.sin(p) * np.cos(r) - np.cos(y) * np.sin(r),
                    ],
                    [-np.sin(p), np.cos(p) * np.sin(r), np.cos(p) * np.cos(r)],
                ]
            )

            # Convert between image and body coordinates
            # Top of image pixels point to flying direction
            # and camera is looking down.
            # We might need to change this if we want different
            # camera mount orientations (e.g. backward or sideways)

            # (Swap X/Y, flip Z)
            cbb = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])

            delta = 1e-7

            p1 = np.array(
                ecef_from_lla(
                    geo["latitude"] + delta,
                    geo["longitude"],
                    geo.get("altitude", 0),
                )
            )
            p2 = np.array(
                ecef_from_lla(
                    geo["latitude"] - delta,
                    geo["longitude"],
                    geo.get("altitude", 0),
                )
            )
            xnp = p1 - p2
            m = np.linalg.norm(xnp)

            if m == 0:
                print("Cannot compute OPK angles, divider = 0")
                return opk

            # Unit vector pointing north
            xnp /= m

            znp = np.array([0, 0, -1]).T
            ynp = np.cross(znp, xnp)

            cen = np.array([xnp, ynp, znp]).T

            # OPK rotation matrix
            ceb = cen.dot(cnb).dot(cbb)

            # opk = {}
            # opk["omega"] = np.degrees(np.arctan2(-ceb[1][2], ceb[2][2]))
            # opk["phi"] = np.degrees(np.arcsin(ceb[0][2]))
            # opk["kappa"] = np.degrees(np.arctan2(-ceb[0][1], ceb[0][0]))
            opk = [
                round(float( np.degrees(np.arctan2(-ceb[1][2], ceb[2][2])) ),3),
                round(float( np.degrees(np.arcsin(ceb[0][2])) ),3),
                round(float( np.degrees(np.arctan2(-ceb[0][1], ceb[0][0])) ),3),
            ]

    return opk