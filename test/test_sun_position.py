# this file is meant to test the sun position
# functionality of the flight software
import os,sys,inspect 
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
gncdir = os.path.dirname(parentdir)
docdir = os.path.dirname(gncdir)
sys.path.insert(0,parentdir)
sys.path.insert(0, gncdir)
sys.path.insert(0, docdir)


import numpy as np
import pytest
import math
from sun_position import *

def test_1():
    MJD = 54000
    a = approx_sun_position_ECI(MJD)
    b = (-1.50147E8,2.977588E6,-2.5599912E4)
    angle_diff = math.acos(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b)))*180/math.pi
    np.testing.assert_allclose(angle_diff, 0.5091389, atol=1) # Python test, checking that the approximate angle is fairly close to JPL


