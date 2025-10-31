import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from camera import Camera

cam = Camera()

WIDTH, HEIGHT = 1280, 1024
gridSize = np.arange(-10.0, 10.0, 0.1)
lastX, lastY = WIDTH/2, HEIGHT/2
first_click = True
left_button_down, right_button_down = False, False
perspective = True
 



########## callback funtions ##########

def cursor_pos_callback(window, xpos, ypos):
    global first_click, lastX, lastY
    if first_click:
        lastX = xpos
        lastY = ypos
        first_click = False
        
    xoffset = xpos-lastX
    yoffset = -(ypos-lastY)
    lastX = xpos
    lastY = ypos
    
    if left_button_down:
        cam.process_cursor_movement(xoffset, yoffset, 'left_button')
    if right_button_down:
        cam.process_cursor_movement(xoffset, yoffset, 'right_button')


def button_callback(window, button, action, mod):
    global left_button_down
    global right_button_down
    global first_click
    
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            left_button_down = True
            first_click = True
        elif action == glfw.RELEASE:
            left_button_down = False
    elif button==glfw.MOUSE_BUTTON_RIGHT:
        if action == glfw.PRESS:
            right_button_down = True
            first_click = True
        elif action == glfw.RELEASE:
            right_button_down = False

                
def scroll_callback(window, x_wheeloffset, y_wheeloffset):
        cam.update_zoom(x_wheeloffset, y_wheeloffset)


def key_callback(window, key, scancode, action, mods):
    global perspective
    if key == glfw.KEY_V:
        if action == glfw.PRESS:
            perspective = not perspective
    cam.get_projection(perspective)




########## object funtions ##########

##### Grid #####
def drawGrid():
    for i in gridSize:
        glBegin(GL_LINES)
        glColor3ub(255, 255, 255)
        glVertex3f(i, 0.0, -10.0)
        glVertex3f(i, 0.0, 10.0)
        glVertex3f(-10.0, 0.0, i)
        glVertex3f(10.0, 0.0, i)
        glEnd()

##### your object #####
"""
def createVertexAndIndexArrayIndexed():
    varr = np.array([
            (-0.1, .1, .1), # v0
            (-0.1, .1, -0.1), # v1
            (.1, .1, -0.1), # v2
            (.1, .1, .1), # v3
            (-0.1, -0.1, .1), # v4
            (-0.1, -0.1, -0.1), # v5
            (.1, -0.1, -0.1), # v6
            (.1, -0.1, .1), # v7
            ], 'float32')
    iarr = np.array([
            (0, 1, 2, 3),
            (0, 1, 5, 4),
            (1, 2, 6, 5),
            (3, 2, 6, 7),
            (0, 3, 7, 4),
            (4, 5, 6, 7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(3, GL_FLOAT, 3*varr.itemsize, varr)
    glDrawElements(GL_QUADS, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
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
"""



########## render funtion ##########
    
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    """"
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    """
    glLoadIdentity()
    
    cam.get_projection(perspective)
    cam.get_gluLookAt()
    drawGrid()

    ##### object #####
    """
    drawFrame()
    glColor3ub(255, 255, 255)
    drawCube_glDrawElements()
    """




########## main funtion ##########
"""
gVertexArrayIndexed = None
gIndexArray = None
"""
def main():
    """
    global gVertexArrayIndexed, gIndexArray
    """
    if not glfw.init():
        return
    window = glfw.create_window(WIDTH,HEIGHT,'Basic OpenGL Viewer', None,None)
    if not window:
        glfw.terminate()
        return

    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_input_mode(window, glfw.STICKY_MOUSE_BUTTONS, glfw.TRUE)
    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)

    """
    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
    """

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        render()
        
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
