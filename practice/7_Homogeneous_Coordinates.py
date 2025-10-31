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

    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (M @ np.array([0., .5, 1.]))[:-1])
    glVertex2fv( (M @ np.array([0., 0., 1.]))[:-1])
    glVertex2fv( (M @ np.array([.5, 0., 1.]))[:-1])
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "2D Trans", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        #rotate 60 deg about z axis
        th = np.radians(60)
        R = np.array([[np.cos(th), -np.sin(th), 0.],
                      [np.sin(th), np.cos(th), 0.],
                      [0., 0., 1.]])

        #translate by (.4, .1)
        T = np.array([[1., 0., .4],
                      [0., 1., .1],
                      [0., 0., 1.]])

        render(R)  #p'=Rp
        #render(T)  #p'=Tp
        #render(T@R)  #p'=TRp
        #render(R@T)  #p'=PRp
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":  
    main()      
