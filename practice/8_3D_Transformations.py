import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render(M):
    #enable depth test
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glLoadIdentity()

    #use orthogonal projection
    glOrtho(-1,1, -1,1, -1,1)

    #rotate "camera" position to see this 3D space better
    t = glfw.get_time()
    gluLookAt(.1*np.sin(t),.1,.1*np.cos(t), 0,0,0, 0,1,0)

    #draw coordinate system: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 1., 0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array([0., 0., 1.]))
    glEnd()

    #draw triangle: p'=Mp
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex3fv( (M @ np.array([0., .5, 0., 1.]))[:-1])
    glVertex3fv( (M @ np.array([0., 0., 0., 1.]))[:-1])
    glVertex3fv( (M @ np.array([.5, 0., 0., 1.]))[:-1])
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "3D Trans", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        #rotate -60 deg about x axis
        th = np.radians(-60)
        R = np.array([[1., 0., 0., 0.],
                      [0., np.cos(th), -np.sin(th), 0.],
                      [0., np.sin(th), np.cos(th), 0.],
                      [0., 0., 0., 1.]])
        
        #translate by (.4, .0, .2)
        T = np.array([[1., 0., 0., .4],
                      [0., 1., .1, 0.],
                      [0., 0., 1., .2],
                      [0., 0., 0., 1.]])

        render(R)  #p'=Rp
        #render(T)  #p'=Tp
        #render(T@R)  #p'=TRp
        #render(R@T)  #p'=PRp


        ########## Practice ##########
        #Tips: Use Slicing
        #You can use slicing for cleaner code
        th1 = np.radians(-60)
        R1 = np.identity(4)
        R1[:3, :3] = [[1., 0., 0.],
                     [0., np.cos(th), -np.sin(th)],
                     [0., np.sin(th), np.cos(th)]]
        T1 = np.identity(4)
        T1[:3, 3] = [.4, 0., .2]
        
        #render(R1)
        #render(T1)
        #render(T1@R1)
        #render(R1@T1)
        ########## End ##########
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":  
    main()      
