import numpy as np

def ecef_to_wgs84(x, y, z):
    """

    :param x:
    :param y:
    :param z:
    :return:
    """
    a = 6378137.0
    b = 6356752.314245
    e_sq = 1 - (b ** 2 / a ** 2)
    ep_sq = (a ** 2 - b ** 2) / b ** 2

    p = np.sqrt(x ** 2 + y ** 2)
    th = np.arctan2(a * z, b * p)

    lon = np.arctan2(y, x)
    lat = np.arctan2(z + ep_sq * b * np.sin(th) ** 3,
                     p - e_sq * a * np.cos(th) ** 3)

    N = a / np.sqrt(1 - e_sq * np.sin(lat) ** 2)
    alt = p / np.cos(lat) - N

    return np.degrees(lat), np.degrees(lon), alt


def ecef_to_enu(pos_array, ref_pos):
    """
    ECEF zu ENU
    :param pos_array:
    :param ref_pos:
    :return:
    """
    lat_ref, lon_ref, _ = ecef_to_wgs84(*ref_pos)
    lat_rad, lon_rad = np.radians(lat_ref), np.radians(lon_ref)

    slat, clat = np.sin(lat_rad), np.cos(lat_rad)
    slon, clon = np.sin(lon_rad), np.cos(lon_rad)

    R = np.array([
        [-slon, clon, 0],
        [-slat * clon, -slat * slon, clat],
        [clat * clon, clat * slon, slat]
    ])

    diff = pos_array - ref_pos
    return (R @ diff.T).T