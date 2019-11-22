# how to get the sun ECI without numpy 

def approx_sun_position_ECI(MJD):
    """
    This is using the equations given in Motenbruck and Gill's Satellite Orbits book
    Inputs:
    MJD - Modified Julian Day (J2000) as a Real Number
    Outputs:
    r_vec - numpy array with x, y, z of Sun position in ECI at input time
    """
    import math
    JD = MJD + 2400000.5
    OplusW = 282.94
    T = (JD - 2451545.0) / 36525

    M = math.radians(357.5256 + 35999.049 * T)

    long = math.radians(OplusW + math.degrees(M) + 6892 / 3600 * math.sin(M) + 72 / 3600 * math.sin(2*M))
    r_mag = (149.619 - 2.499 * math.cos(M) - 0.021 * math.cos(2*M)) * 10**6

    epsilon = math.radians(23.43929111)
    r_vec = (r_mag * math.cos(long), r_mag * math.sin(long) * math.cos(epsilon), r_mag * math.sin(long) * math.sin(epsilon))

    return r_vec
