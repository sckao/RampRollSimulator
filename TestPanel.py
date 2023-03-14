# Ramp and Roll Simulator
# Author: Kevin Kao
# Contact: kaoshihchuan@gmail.com
import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as tkmsg

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import RampRoll as RampRoll


class Plots:

    __instance__ = None

    def __init__(self):

        self.canvas = None
        self.fig = plt.figure(figsize=(8, 7))

        self.ax1 = plt.subplot2grid((2, 1), (0, 0))
        self.ax1.set_xlabel('Time (sec)')
        self.ax1.set_ylabel('Velocity (m/s)')
        self.ax2 = plt.subplot2grid((2, 1), (1, 0))
        self.ax2.set_xlabel('Time (sec)')
        self.ax2.set_ylabel('Travel distance (m)')

        Plots.__instance__ = self

    def config(self, root_tk):

        # ==== Scan profile display =====
        self.canvas = FigureCanvasTkAgg(self.fig, master=root_tk)  # A tk.DrawingArea.
        self.canvas.get_tk_widget().grid(row=1, column=0, rowspan=15, columnspan=11, sticky='NSWE')
        # self.fig.tight_layout(w_pad=0.8, h_pad=0.0)

        # ##############    TOOLBAR    ###############
        toolbar_frame = tk.Frame(master=root_tk)
        toolbar_frame.grid(row=0, column=0, columnspan=6)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()

    def __del__(self):
        Plots.__instance__ = None

    @staticmethod
    def get_instance():

        if Plots.__instance__ is None:
            Plots()

        return Plots.__instance__


class GuiWindow:
    __instance__ = None

    def __init__(self, rootgui):
        self.window = rootgui

        # define the scanning display
        self.frame00 = tk.Frame(self.window)
        self.frame00.grid(row=0, column=0, sticky=tk.NSEW, rowspan=2)
        self.frame01 = tk.Frame(self.window)
        self.frame01.grid(row=0, column=1, sticky=tk.N, padx=10, pady=40)
        self.frame02 = tk.Frame(self.window)
        self.frame02.grid(row=1, column=1, sticky=tk.N, padx=10, pady=0)

        self.label_font_16 = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.label_font_12 = tkfont.Font(family="Helvetica", size=12, weight="bold")
        self.report_font_12 = tkfont.Font(family="Helvetica", size=12)

        self.rr_obj = RampRoll.RampRoll()
        self.angle_height_opt_list = ['height', 'angle', 'width']
        self.length_unit_opt_list = ['m', 'cm', 'Inches']
        self.unit_factor: float = 1.

        self.car_mass_var = tk.DoubleVar(self.window, value=1.0)
        self.ramp_angle_var = tk.DoubleVar(self.window, value=0.5)
        self.ramp_length_var = tk.DoubleVar(self.window, value=1.0)
        self.ramp_friction_coeff_var = tk.DoubleVar(self.window, value=0.1)
        self.floor_friction_coeff_var = tk.DoubleVar(self.window, value=0.1)
        self.air_drag_coeff_var = tk.DoubleVar(self.window, value=0.002)
        self.sim_dt_var = tk.DoubleVar(self.window, value=0.001)
        self.floor_limit_var = tk.DoubleVar(self.window, value=100)
        self.ramp_h_var = tk.DoubleVar(self.window, value=0.0)
        self.ramp_l_var = tk.DoubleVar(self.window, value=0.0)
        self.ramp_w_var = tk.DoubleVar(self.window, value=0.0)
        self.cal_angle_var = tk.StringVar(self.window, value='0.0')
        self.angle_opt_var = tk.StringVar(self.window, value=self.angle_height_opt_list[0])
        self.unit_opt_var = tk.StringVar(self.window, value=self.length_unit_opt_list[0])
        self.angle_unit_var = tk.StringVar(self.window, value=self.length_unit_opt_list[0])
        self.angle_report_var = tk.StringVar(self.window, value='')
        self.distant_report_var = tk.StringVar(self.window, value='0.0')

        ramp_friction_coeff = self.ramp_friction_coeff_var.get()
        floor_friction_coeff = self.floor_friction_coeff_var.get()
        self.rr_obj.set_ramp_friction_coeff(ramp_friction_coeff)
        self.rr_obj.set_floor_friction_coeff(floor_friction_coeff)

        # ========= config matplot display =============
        self.plot = Plots()
        self.plot.config(self.frame00)

        rr_label = tk.Label(self.frame01, text='Ramp & Roll Simulator', font=self.label_font_12)
        rr_label.grid(row=0, column=0, columnspan=2)
        mass_label = tk.Label(self.frame01, text='Car Mass (kg)', width=15)
        mass_label.grid(row=1, column=0)
        mass_entry = tk.Entry(self.frame01, textvariable=self.car_mass_var,
                              width=10, justify='right')
        mass_entry.grid(row=1, column=1)
        length_label = tk.Label(self.frame01, text='Ramp Length ', width=15)
        length_label.grid(row=2, column=0)
        ramp_length_entry = tk.Entry(self.frame01, textvariable=self.ramp_length_var,
                                     width=10, justify='right')
        ramp_length_entry.grid(row=2, column=1)

        ramp_unit_menu = tk.OptionMenu(self.frame01,
                                       self.unit_opt_var,
                                       *self.length_unit_opt_list,
                                       command=lambda selection: self.set_unit_for_height()
        )
        ramp_unit_menu.grid(row=2, column=2, sticky=tk.EW)

        angle_menu = tk.OptionMenu(self.frame01,
                                   self.angle_opt_var,
                                   *self.angle_height_opt_list,
                                   command=lambda selection: self.set_unit_for_height()
                                   )
        angle_menu.grid(row=3, column=0, sticky=tk.EW)

        ramp_angle_entry = tk.Entry(self.frame01, textvariable=self.ramp_angle_var,
                                    width=10, justify='right')
        ramp_angle_entry.grid(row=3, column=1)

        ramp_angle_label = tk.Label(self.frame01, textvariable=self.angle_unit_var)
        ramp_angle_label.grid(row=3, column=2, sticky=tk.EW)

        cal_angle_label = tk.Label(self.frame01, text='Angle (degree)', width=15)
        cal_angle_label.grid(row=4, column=0, pady=0)
        cal_result_report = tk.Label(self.frame01, textvariable=self.angle_report_var, width=10)
        cal_result_report.grid(row=4, column=1, pady=0)

        rr_btn = tk.Button(self.frame01, text='Run', command=self.run_ramp_roll,
                           font=self.label_font_16)
        rr_btn.grid(row=5, column=0, columnspan=2, sticky=tk.EW)

        dist_report_label = tk.Label(self.frame01, text='Distance (m)', font=self.label_font_12)
        dist_report_label.grid(row=6, column=0, pady=0, sticky=tk.EW)
        dist_result_report = tk.Label(self.frame01, textvariable=self.distant_report_var,
                                      font=self.label_font_12)
        dist_result_report.grid(row=6, column=1, pady=0, sticky=tk.EW)

        # angle calculator
        '''
        cal_label = tk.Label(self.frame01, text='Slope Angle Calculator', font=self.label_font_12)
        cal_label.grid(row=6, column=0, columnspan=2, pady=20)
        angle_result_label = tk.Label(self.frame01, text='Angle (deg)', width=15)
        angle_result_label.grid(row=7, column=0, pady=0)
        angle_result = tk.Label(self.frame01, textvariable=self.cal_angle_var, width=10, font=self.report_font_12)
        angle_result.grid(row=7, column=1, pady=0)
        rh_label = tk.Label(self.frame01, text='Ramp Height', width=15)
        rh_label.grid(row=8, column=0)
        rh_entry = tk.Entry(self.frame01, textvariable=self.ramp_h_var,
                            width=10, justify='right')
        rh_entry.grid(row=8, column=1)
        rs_label = tk.Label(self.frame01, text='Slope Length', width=15)
        rs_label.grid(row=9, column=0)
        rs_entry = tk.Entry(self.frame01, textvariable=self.ramp_l_var,
                            width=10, justify='right')
        rs_entry.grid(row=9, column=1)
        # rw_label = tk.Label(self.frame01, text='Bottom Length', width=15)
        # rw_label.grid(row=10, column=0)
        # rw_entry = tk.Entry(self.frame01, textvariable=self.ramp_w_var,
        #                     width=10, justify='right')
        # rw_entry.grid(row=10, column=1)
        cal_btn = tk.Button(self.frame01, text='Get Angle', command=self.get_angle,
                            font=self.label_font_12)
        cal_btn.grid(row=11, column=0, columnspan=2, sticky=tk.EW)
        '''
        adv_label = tk.Label(self.frame02, text='Advance Parameters', font=self.label_font_12)
        adv_label.grid(row=0, column=0, columnspan=2)
        ramp_friction_btn = tk.Button(self.frame02, text='Ramp Friction', command=self.set_ramp_friction_coeff,
                                      width=15)
        ramp_friction_btn.grid(row=1, column=0)
        ramp_friction_entry = tk.Entry(self.frame02, textvariable=self.ramp_friction_coeff_var,
                                       width=10, justify='right')
        ramp_friction_entry.grid(row=1, column=1, padx=1)
        floor_friction_btn = tk.Button(self.frame02, text='Floor Friction', command=self.set_floor_friction_coeff,
                                       width=15)
        floor_friction_btn.grid(row=2, column=0)
        floor_friction_entry = tk.Entry(self.frame02, textvariable=self.floor_friction_coeff_var,
                                        width=10, justify='right')
        floor_friction_entry.grid(row=2, column=1, padx=1)

        air_drag_btn = tk.Button(self.frame02, text='Air Drag Coefficient', command=self.set_air_drag_coeff,
                                 width=15)
        air_drag_btn.grid(row=3, column=0)
        air_drag_entry = tk.Entry(self.frame02, textvariable=self.air_drag_coeff_var,
                                  width=10, justify='right')
        air_drag_entry.grid(row=3, column=1, padx=1)

        # delta_t_btn = tk.Button(self.frame02, text='Sim Delta t (s)', command=self.set_delta_t,
        #                         width=15)
        # delta_t_btn.grid(row=4, column=0)
        #  delta_t_entry = tk.Entry(self.frame02, textvariable=self.sim_dt_var,
        #                          width=10, justify='right')
        # delta_t_entry.grid(row=4, column=1, padx=1)

        floor_limit_btn = tk.Button(self.frame02, text='Floor limit (m)', command=self.set_floor_limit,
                                    width=15)
        floor_limit_btn.grid(row=5, column=0)
        floor_limit_entry = tk.Entry(self.frame02, textvariable=self.floor_limit_var,
                                     width=10, justify='right')
        floor_limit_entry.grid(row=5, column=1, padx=1)
        load_default_btn = tk.Button(self.frame02, text='Load default values', command=self.load_default_parameters,
                                     width=15, font=self.label_font_12)
        load_default_btn.grid(row=6, column=0, columnspan=2, sticky=tk.EW)

        self.window.update_idletasks()

        GuiWindow.__instance__ = self
    # end __init__

    def __del__(self):
        GuiWindow.__instance__ = None
    # end __del__

    def change_to_meter(self):

        unit_opt = self.unit_opt_var.get()
        if unit_opt == 'm':
            self.unit_factor = 1.
        if unit_opt == 'cm':
            self.unit_factor = 0.01
        if unit_opt == 'Inches':
            self.unit_factor = 0.0254

    def set_unit_for_height(self):
        angle_height_opt = self.angle_opt_var.get()
        unit_opt = self.unit_opt_var.get()
        if angle_height_opt == self.angle_height_opt_list[1]:
            self.angle_unit_var.set('degree')
        else:
            self.angle_unit_var.set(unit_opt)

    def run_ramp_roll(self):

        m_car = self.car_mass_var.get()
        length_ramp = self.ramp_length_var.get()
        angle_height = self.ramp_angle_var.get()
        angle_height_opt = self.angle_opt_var.get()
        self.change_to_meter()

        theta_ramp = angle_height
        if angle_height_opt == 'height':
            if angle_height >= length_ramp or length_ramp <= 0.0:
                tkmsg.showinfo('Error Input',
                               ' Slope length must be larger than ramp height and greater than zero !'
                               )
                return
            theta_rad = np.arcsin(angle_height/length_ramp)
            theta_ramp = theta_rad*180/np.pi
        if angle_height_opt == 'width':
            if angle_height >= length_ramp or length_ramp <= 0.0:
                tkmsg.showinfo('Error Input',
                               ' Slope bottom width must be greater than zero !'
                               )
                return
            theta_rad = np.arccos(angle_height/length_ramp)
            theta_ramp = theta_rad*180/np.pi

        self.angle_report_var.set('%.3f' % theta_ramp)

        self.rr_obj.set_car_mass(m_car)
        self.rr_obj.set_ramp_angle(theta_ramp)
        va, sa, ta = self.rr_obj.run(length_ramp*self.unit_factor)
        final_dist = '%.3f' % sa[-1]

        self.distant_report_var.set(final_dist)

        self.plot.ax1.cla()
        self.plot.ax2.cla()
        self.plot.ax1.grid()
        self.plot.ax2.grid()
        self.plot.ax1.plot(ta, va, 'r')
        self.plot.ax2.plot(ta, sa, 'b')
        self.plot.ax1.set_ylabel('Velocity (m/s)')
        self.plot.ax1.set_xlabel('Time (sec)')
        self.plot.ax2.set_ylabel('Travel distance (m)')
        self.plot.ax2.set_xlabel('Time (sec)')

        self.plot.canvas.draw()
        self.plot.canvas.flush_events()

    def set_ramp_friction_coeff(self):

        friction_coeff = self.ramp_friction_coeff_var.get()
        self.rr_obj.set_ramp_friction_coeff(friction_coeff)

    def set_floor_friction_coeff(self):

        friction_coeff = self.floor_friction_coeff_var.get()
        self.rr_obj.set_floor_friction_coeff(friction_coeff)

    def set_air_drag_coeff(self):

        air_drag_coeff = self.air_drag_coeff_var.get()
        self.rr_obj.set_air_drag_coeff(air_drag_coeff)

    def set_delta_t(self):

        dt = self.sim_dt_var.get()
        self.rr_obj.set_sim_delta_t(dt)

    def set_floor_limit(self):
        floor_lim = self.floor_limit_var.get()
        self.rr_obj.set_floor_limit(floor_lim)

    def load_default_parameters(self):

        default_ramp_friction = 0.1
        default_floor_friction = 0.1
        default_air_drag = 0.002
        default_sim_dt = 0.001
        default_floor_limit = 100
        self.ramp_friction_coeff_var.set(default_ramp_friction)
        self.floor_friction_coeff_var.set(default_floor_friction)
        self.air_drag_coeff_var.set(default_air_drag)
        self.floor_limit_var.set(default_floor_limit)
        self.sim_dt_var.set(default_sim_dt)

        self.rr_obj.set_ramp_friction_coeff(default_ramp_friction)
        self.rr_obj.set_floor_friction_coeff(default_floor_friction)
        self.rr_obj.set_air_drag_coeff(default_air_drag)
        self.rr_obj.set_sim_delta_t(default_sim_dt)
        self.rr_obj.set_floor_limit(default_floor_limit)

    def get_angle(self):

        h = self.ramp_h_var.get()
        s = self.ramp_l_var.get()
        # w = self.ramp_w_var.get()

        # if h > 0.0 and w > 0.0:
        #     theta_rad = np.arctan(h/w)
        #     theta_deg = theta_rad*180/np.pi
        #     self.cal_angle_var.set('%.3f' % theta_deg)
        # elif s > 0.0 and w > 0.0 and s > w:
        #     theta_rad = np.arccos(w/s)
        #     theta_deg = theta_rad*180/np.pi
        #     self.cal_angle_var.set('%.3f' % theta_deg)
        if s > 0.0 and s > h:
            theta_rad = np.arcsin(h/s)
            theta_deg = theta_rad*180/np.pi
            self.cal_angle_var.set('%.3f' % theta_deg)
        else:
            print('Error!')
            self.cal_angle_var.set('Error Inputs')
            tkmsg.showinfo('Error Input', ' Slope length must be larger than ramp height and greater than zero !')
