import glfw
from OpenGL.GL import *
import numpy as np

def render(M, u):
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
    glVertex2fv(M @ np.array([0., .5]) + u)
    glVertex2fv(M @ np.array([0., 0.]) + u)
    glVertex2fv(M @ np.array([.5, 0.]) + u)
    glEnd()


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "2D Trans", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    glfw.swap_interval(1)
    
    while not glfw.window_should_close(window):
        glfw.poll_events()

        t = glfw.get_time()

        th = t
        R = np.array([[np.cos(th), -np.sin(th)],
                      [np.sin(th), np.cos(th)]])
        
        u = np.array([np.sin(t), 0])

        render(R, u)
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":  
    main()      
