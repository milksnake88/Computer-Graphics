import glfw
from OpenGL.GL import *
import numpy as np

def render(M):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    #draw coordinate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([1., 0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0., 0.]))
    glVertex2fv(np.array([0., 1.]))
    glEnd()

    #draw a triangle: p'=Mp
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv(M@np.array([0., .5]))
    glVertex2fv(M@np.array([0., 0.]))
    glVertex2fv(M@np.array([.5, 0.]))
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "2D Trans", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    #set the number of screen refresh to wait before calling glfw.swap_buffer()
    #if your monitor refresh rate is 60Hz, the while loop is repeated every 1/60 sec
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        #get the current time, in seconds
        t = glfw.get_time()

        #uniform scale
        s = np.sin(t)
        M = np.array([[s, 0. ],
                      [0., s ]])
        
        ########## Practice ##########
        #1)nonuniform scale
        s1 = np.sin(t)
        M1 = np.array([[s, 0.],
                       [0., s*.5]])

        #2)rotation
        th = t
        M2 = np.array([[np.cos(th), -np.sin(th)],
                       [np.sin(th), np.cos(th)]])

        #3)reflection
        M3 = np.array([[-1., 0.],
                       [0., 1.]])

        #4)shear
        a = np.sin(t)
        M4 = np.array([[1., a],
                      [0., 1.]])

        #5)identity matrix
        M5 = np.identity(2)
        ########## End ##########
        

        render(M)
        #render(M1)
        #render(M2)
        #render(M3)
        #render(M4)
        #render(M5)

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":  
    main()      
