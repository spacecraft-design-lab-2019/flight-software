import math


def R2(q):
    """
    Matrix equivilent to right-hand quaternion for mulitplication
    (eg. q1 * q2 = R(q2)q1)
    """
    s = q[0]
    v = q[1:4]
    R = [[s, -v[0], -v[1], -v[2]],
                  [v[0], s, v[2], -v[1]],
                  [v[1], -v[2], s, v[0]],
                  [v[2], v[1], -v[0], s]]
    return R      

def L2(q):
    """
    Matrix equivilent to left-hand quaternion for mulitplication
    (eg. q1 * q2 = L(q1)q2)
    """
    s = q[0]
    v = q[1:4]
    L = [[s, -v[0], -v[1], -v[2]],
                  [v[0], s, -v[2], v[1]],
                  [v[1], v[2], s, -v[0]],
                  [v[2], -v[1], v[0], s]]
    return L

def quatrot2(q1, r):
    """
    Rotates a vector `q2` using the quaternion `q1`.
    """
    vector = False
    r = [0,r[0],r[1],r[2]]
    vector = True
    rotated = matTimesVec(L2(q1),matTimesVec(transpose(R2(q1)),r))

    if vector:
        return rotated[1:4]
    else:
        return rotated

def vecTimesMat(x, M):
    """
    Vector multiplication for lists.
    Performs x^T * M
    """
    return [dot(m, x) for m in transpose(M)]

def matTimesVec(M, x):
    """
    Vector multiplication for lists.
    Performs M * x
    """
    return [dot(m, x) for m in M]

def transpose(M):
    I = range(len(M))
    J = range(len(M[0]))
    return [[M[i][j] for i in I] for j in J]

def dot(v1, v2):
    return sum(x*y for x,y in zip(v1,v2))

def scale(vec, scalar):
    return [x*scalar for x in vec]

def norm(vec):  
    return math.sqrt(dot(vec, vec))

def sub(vec1, vec2):
    """
    Inputs: 2 vectors
    Outputs: vector1 - vector2 in vector form
    """
    return [x - y for x, y in zip(vec1, vec2)]

def normalize(vec):
    """
    Inputs: vector
    Outputs: normalized vector
    """
    mag = norm(vec)
    if all([v == 0 for v in vec]): #returns 0 vector if vec = [0,0,0]
        return vec
    else:
        return [x/mag for x in vec]

def sense2vector(meas, r_sat, q_eci2body, albedo = True):
    """
    Inputs:
        meas: raw measurement values from 6 sun sensors. Arranged: [x, -x, y, -y, z, -z]
        r_Earth2Sun: Earth to Sun vector
        r_sat: position of satellite in ECI
    Outputs:
        sat2sun: satellite to sun 3-vector (in body frame)
    """

    irrad_vec = [meas[0] - meas[1],  meas[2] - meas[3], meas[4] - meas[5]] #create irradiance vector from sensor values
    irrad_vec = normalize(irrad_vec) # normalize irradiance vector

    if albedo:
        alb = quatrot2(q_eci2body, scale(normalize(r_sat), 0.2)) #convert to body frame
        sat2sun = normalize(sub(irrad_vec, alb)) #vector subt. irradiance vec and albedo vec, normalize
    else:
        sat2sun = irrad_vec

    return sat2sun #in body frame