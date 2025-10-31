import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render():
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
    
    glColor3ub(255, 255, 255)

    ###########################
    n = len(transFun_list)
    for i in reversed(range(n)):
        if transFun_list[i] == 'Q':
            glTranslatef(-0.1,0.,0.)
        elif transFun_list[i] == 'E':
            glTranslatef(.1,0.,0.)
        elif transFun_list[i] == 'A':
            glRotatef(10.,0.,0.,1.)
        elif transFun_list[i] == 'D':
            glRotatef(-10.,0.,0.,1.)
        else:
            break
    ###########################

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()


transFun_list = []

def get_transFun():
    global transFun_list
    key = input("Enter the key for transformation : ")
    transFun_list.append(key)
    return transFun_list


def main():
    get_transFun()
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016026608", None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)
    glfw.terminate()


def render_init():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)
    drawTriangle()    

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
        render_init()
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main_init()
    while True:
        main()
