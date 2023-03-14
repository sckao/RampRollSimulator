import numpy as np
import tkinter.messagebox as tkmsg

# import matplotlib.pyplot as plt


# a = 2*sqrt(ck)/ m , k = mg(sinA - u*cosA)
# b = c/k
# c: air drag coefficient
def v_ramp(t: float, c: float, m: float, theta: float, u: float, g=9.8):

    theta_rad = theta*np.pi/180.
    k = m*g*(np.sin(theta_rad) - (u*np.cos(theta_rad)))
    v = 0
    if k <= 0.:
        tkmsg.showinfo('Error',
                       ' Car cannot slide down ! Ramp friction is too large or slope is not enough !'
                       )
        return v

    a = 2*np.sqrt(c*k)/m
    b = c/k
    if c > 0.0:
        v = (np.exp(a*t) - 1) / (np.exp(a*t)+1)
        v = v/np.sqrt(b)

    else:
        v = (k/m)*t

    return v


# a = sqrt(u*m*g/c)
# b = sqrt(u*g*c/m)
def v_slowdown(t: float, a: float, b: float):

    v = a*np.arctan(-1.*b*t)

    return v


class RampRoll:

    def __init__(self):

        self.m: float = 1.
        self.g: float = 9.8
        # ramp angle ind degree
        self.theta = 30.0
        # friction coefficient of the ramp
        self.u_r = 0.1
        self.u_f = 0.1
        # air drag coefficient
        self.c = 0.002
        # simulation delta t (s)
        self.dt = 0.001
        self.floor_limit = 100

    def set_car_mass(self, m_: float):
        self.m = m_

    def set_ramp_angle(self, angle_deg: float):
        self.theta = angle_deg

    def set_ramp_friction_coeff(self, u_: float):
        self.u_r = u_

    def set_floor_friction_coeff(self, u_: float):
        self.u_f = u_

    def set_air_drag_coeff(self, c_: float):
        self.c = c_

    def set_sim_delta_t(self, delta_t):
        self.dt = delta_t

    def set_floor_limit(self, floor_limit):
        self.floor_limit = floor_limit

    def kinematic_energy(self, v):

        k = 0.5*self.m*v*v
        return k

    def friction_loss(self, ds, u_friction):
        w = u_friction*self.m*self.g*ds
        return w

    def air_drag_loss(self, v, ds):
        w = self.c*v*v*ds
        return w

    def get_velocity_from_kinematics(self, k):
        if k < 0.:
            return 0.
        v = np.sqrt(2*k/self.m)
        return v

    def run(self, slope_length=5):

        t = 0.
        dt = self.dt
        s = -1*slope_length
        va = []
        ta = []
        sa = []
        while s < 0.0:
            vi = v_ramp(t, self.c, self.m, self.theta, self.u_r, self.g)
            if vi == 0. and t > 0.:
                break
            # print(' vi = %.3f , %.3f ' % (vi, vj))
            s = s + (vi*dt)
            va.append(vi)
            ta.append(t)
            sa.append(s)
            t = t + dt
        # print(' number of accelerating = %d , s = %.3f' % (len(va), sa[-2]))
        if len(va) < 1:
            return va, sa, ta

        v = va[-1]
        # a1 = np.sqrt(self.u*self.m*self.g/self.c)
        # b1 = np.sqrt(self.u*self.c*self.g/self.m)
        i = 0
        while v > 0:

            t = t + dt
            k = self.kinematic_energy(v)
            w_friction = self.friction_loss(v*dt, self.u_f)
            w_drag = self.air_drag_loss(v, v*dt)
            v = self.get_velocity_from_kinematics(k - w_friction - w_drag)
            # print('[%d] v = %.4f' % (i, v))
            dv = v - va[-1]
            a = dv/dt
            # print(' a = %.5f ' % a)
            s = s + (v*dt)

            va.append(v)
            ta.append(t)
            sa.append(s)
            i = i + 1
            if s > self.floor_limit:
                break

        # print(' number of decelerating = %d , s = %.3f' % (len(va), sa[-2]))
        '''
        plt.figure(figsize=(8, 7))
        ax1 = plt.subplot2grid((2, 1), (0, 0))
        ax2 = plt.subplot2grid((2, 1), (1, 0))
        ax1.plot(ta, va, 'r')
        ax1.grid()
        ax2.plot(ta, sa, 'b')
        ax2.grid()
        ax1.set_ylabel('Velocity (m/s)')
        ax1.set_xlabel('Time (sec)')
        ax2.set_ylabel('Total distance (m)')
        ax2.set_xlabel('Time (sec)')

        plt.show()
        '''
        return va, sa, ta

# rr = RampRoll()
# rr.set_car_mass(0.5)
# rr.run(4)
