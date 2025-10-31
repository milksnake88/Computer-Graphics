import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class Camera:
    def __init__(self):
        self.cam_pos = np.array([1., 1., 0.])
        self.target_pos = np.array([0., 0., 0.])
        self.world_up = np.array([0., 1., 0.])

        self.cam_back = np.array([1.,1.,0.])/np.sqrt(np.dot(np.array([1.,1.,0.]),np.array([1.,1.,0.])))
        self.cam_right = np.array([0.,0.,-1.])
        self.cam_up = np.cross(self.cam_back, self.cam_right)

        self.mouse_sensitivity = 0.1
        
        self.azimuth = -90
        self.elevation = -45
        
        self.xoffset = 0
        self.yoffset = 0

        self.left = -1
        self.right = 1
        self.bottom = -1
        self.top = 1
        self.zNear = -100
        self.zFar = 100


    def get_projection(self, perspective):
        if perspective:
            Projection = gluPerspective(45, 1, 0.001, 10)
        else:
            Projection = glOrtho(self.left, self.right, self.bottom, self.top, self.zNear, self.zFar)
        return Projection


    def get_gluLookAt(self):
        self.update_cam_cood()
        return gluLookAt(self.cam_pos[0],self.cam_pos[1],self.cam_pos[2],
                         self.target_pos[0],self.target_pos[1],self.target_pos[2],
                         self.cam_up[0],self.cam_up[1],self.cam_up[2])

    
    def process_cursor_movement(self, xoffset, yoffset, button):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity
        
        if button == 'left_button':
            self.azimuth += xoffset
            self.elevation += yoffset
            self.update_orbit()   
        if button == 'right_button':
            self.xoffset = (self.mouse_sensitivity**2) * xoffset
            self.yoffset = (self.mouse_sensitivity**2) * yoffset
            self.update_pan()


    def update_orbit(self):
        distance = np.sqrt(np.dot(self.cam_pos-self.target_pos, self.cam_pos-self.target_pos))
        self.cam_pos[0] = self.target_pos[0] + distance*(np.cos(np.radians(-self.elevation))*np.sin(np.radians(-self.azimuth)))
        self.cam_pos[1] = self.target_pos[1] + distance*(np.sin(np.radians(-self.elevation)))
        self.cam_pos[2] = self.target_pos[2] + distance*(np.cos(np.radians(-self.elevation))*np.cos(np.radians(-self.azimuth)))
        self.update_cam_cood()

        
    def update_pan(self):
        self.cam_pos += (self.cam_right*(-self.xoffset))+(self.cam_up*(-self.yoffset))
        self.target_pos += (self.cam_right*(-self.xoffset))+(self.cam_up*(-self.yoffset))
        self.update_cam_cood()

        
    def update_zoom(self, x_wheeloffset, y_wheeloffset):
        y_wheeloffset *= self.mouse_sensitivity
 
        if self.right-y_wheeloffset > 0.0001:
            self.cam_pos += (self.cam_back * -(y_wheeloffset*2))
            self.left -= -y_wheeloffset
            self.right += -y_wheeloffset
            self.bottom -= -y_wheeloffset
            self.top += -y_wheeloffset
            self.zNear -= -y_wheeloffset
            self.zFar += -y_wheeloffset

        self.update_cam_cood()

        
    def update_cam_cood(self):
        cam_back = self.cam_pos-self.target_pos
        self.cam_back = (cam_back)/(np.sqrt(np.dot(cam_back,cam_back)))
        cam_right = np.cross(self.world_up,self.cam_back)
        self.cam_right = (cam_right)/(np.sqrt(np.dot(cam_right,cam_right)))
        self.cam_up = np.cross(self.cam_back,self.cam_right)

