
import ulab as np
from pycubedmini import cubesat
from sim_comms import sim_communicate, passthrough_msg

# wait until an input from the computer before continuing
cubesat.RGB = (255, 0, 0) # set LED to red
input()
cubesat.RGB = (0, 255, 0) # set LED to green


# all initial values
x_k = np.array([[0.1535], [0.2737], [0.0438],[-0.9485], [0],[0],[0]]) # quaternion, gyro bias
P_k = np.array([[3.000e-6, 0, 0, 0, 0, 0], [0, 3.000e-6, 0, 0, 0, 0], [0, 0, 3.000e-6, 0, 0, 0], [0, 0, 0, 3.046e-4, 0, 0], [0, 0, 0, 0, 3.046e-4, 0],[0, 0, 0, 0, 0, 3.046e-4]])
# w_k = np.array([[-0.0381], [0.0554], [0.2084]])
# r_sun_body = np.array([[0.4199], [0.7489], [-0.5127]])
# r_B_body = np.array([[-0.4968], [0.8665], [0.0484]])
# r_sun_inert = np.array([[0.2627], [-0.7082],[-0.6553]])
# r_B_inert = np.array([[0.6693],[-0.6818], [0.2952]])
Q = np.array([[3.046e-10, 0, 0, 0, 0, 0], [0, 3.046e-10, 0, 0, 0, 0], [0, 0, 3.046e-10, 0, 0, 0],[0, 0, 0, 3.046e-10, 0, 0],[0, 0, 0, 0, 3.046e-10, 0],[0, 0, 0, 0, 0,3.046e-10]])
R = np.array([[.0003, 0, 0, 0, 0, 0], [0, .0003, 0, 0, 0, 0],[0, 0, .0003, 0, 0, 0],[0, 0, 0, .0076, 0, 0],[0, 0, 0, 0, .0076, 0],[0, 0, 0, 0, 0, .0076]])
dt = np.array([.1])


while True:
    x_k.transpose()
    x_k_list = list(x_k)
    x_k.transpose()
    P_k_list = [list(i) for i in list(P_k)] # make this a function
    sensors = sim_communicate([x_k_list, P_k_list])
    w_k = sensors[0]
    r_sun_body = sensors[1]
    r_B_body = sensors[2]
    r_sun_inert = sensors[3]
    r_B_inert = sensors[4]
    np.MEKFstep(x_k, P_k, w_k, r_sun_body, r_B_body, r_sun_inert, r_B_inert, Q, R, dt)



'''
Should return:
x_k1 =
    0.1641
    0.2768
    0.0434
   -0.9458
    0.0019
   -0.0029
   -0.0027
P_k1 =
   1.0e-03 *
    0.0038    0.0000   -0.0000   -0.0151   -0.0000    0.0000
    0.0000    0.0038   -0.0000   -0.0000   -0.0151    0.0001
   -0.0000   -0.0000    0.0038    0.0000    0.0001   -0.0151
   -0.0151   -0.0000    0.0000    0.3039    0.0002   -0.0001
   -0.0000   -0.0151    0.0001    0.0002    0.3043   -0.0003
    0.0000    0.0001   -0.0151   -0.0001   -0.0003    0.3041
'''