import glfw
from OpenGL.GL import *
import numpy as np

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()


gComposedM = np.array([[1.,0.,0.],
                       [0.,1.,0.],
                       [0.,0.,1.]])    


def get_Transformation():
    global gComposedM
    key = input("Enter the key for transformation : ")
    if key == 'W':
        newM = np.array([[0.9,0.,0.],
                         [0.,1.,0.],
                         [0.,0.,1.]])
    elif key == 'E':
        newM = np.array([[1.1,0.,0.],
                         [0.,1.,0.],
                         [0.,0.,1.]])
    elif key == 'S':
        th = np.radians(10)
        newM = np.array([[np.cos(th),-np.sin(th),0.],
                         [np.sin(th),np.cos(th),0.],
                         [0.,0.,1.]])
    elif key == 'D':
        th = np.radians(-10)
        newM = np.array([[np.cos(th),-np.sin(th),0.],
                         [np.sin(th),np.cos(th),0.],
                         [0.,0.,1.]])
    elif key == 'X':
        newM = np.array([[1.,-0.1,0.],
                         [0.,1.,0.],
                         [0.,0.,1.]])
    elif key == 'C':
        newM = np.array([[1.,0.1,0.],
                         [0.,1.,0.],
                         [0.,0.,1.]])
    elif key == 'R':
        newM = np.array([[1.,0.,0.],
                         [0.,-1.,0.],
                         [0.,0.,1.]])                     
    else:
        newM = np.array([[1.,0.,0.],
                         [0.,1.,0.],
                         [0.,0.,1.]])
        gComposedM = np.array([[1.,0.,0.],
                               [0.,1.,0.],
                               [0.,0.,1.]])
    gComposedM = newM @ gComposedM
    return gComposedM


def main():
    T = get_Transformation()
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016026608", None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render(T)

        glfw.swap_buffers(window)

    glfw.terminate()


def main_init():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016026608", None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        T = np.array([[1.,0.,0.],
                      [0.,1.,0.],
                      [0.,0.,1.]])
        render(T)

        glfw.swap_buffers(window)

    glfw.terminate()
    

if __name__ == "__main__":
    main_init()
    while True:
        main()
