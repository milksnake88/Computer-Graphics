import glfw  #import X : access X's attribute or method using X.attribute, X.method()
from OpenGL.GL import *  #from X import * : access X's attribute or method just using attribute, method()
import numpy as np


def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glVertex2f(0., 1.)
    glVertex2f(-1., -1.)
    glVertex2f(1., -1.)
    glEnd()

########## Practice ##########
#1)Resize the Triangle
def render_resize():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glVertex2f(0., 0.5)
    glVertex2f(-.5, -.5)
    glVertex2f(.5, -.5,)
    glEnd()
    
#2)Change the Primitive Type
def render_change_primitive():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_POINTS)
    #glBegin(GL_LINES)
    #glBegin(GL_LINE_STRIP)
    #glBegin(GL_LINE_LOOP)
    #glBegin(GL_TRIANGLES)
    #glBegin(GL_TRIANGLE_STRIP)
    #glBegin(GL_TRIANGLE_FAN)
    #glBegin(GL_QUADS)
    #glBegin(GL_QUAD_STRIP)
    #glBegin(GL_POLYGON)
    glVertex2f(0., 0.5)
    glVertex2f(-.5, -.5)
    glVertex2f(.5, -.5,)
    glEnd()

#3)Colored Triangle
def render_colored():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)  #Colors in interior are interpolated
    glColor3f(1., 0., 0.)
    glVertex2f(0., 1.)
    glColor3f(0. ,1., 0.)
    glVertex2f(-1., -1.)
    glColor3f(0., 0., 1.)
    glVertex2f(1., -1.)
    glEnd()

#4)Red Triangle
def render_red():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)  #Set red color for each vertex? You can do it just by:
    glColor3f(1., 0., 0.)
    glVertex2f(0., 1.)
    glVertex2f(-1., -1.)
    glVertex2f(1., -1.)
    glEnd()

#5)Other forms of OpenGL Functions
def render_other_forms():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 0, 0)  #ub:unsigned byte
    glVertex2fv((0., 1.))  #v:vector(tuple,list,array), omit "v" for scalar form
    glVertex2fv([-1., -1.])
    glVertex2fv(np.array([1., -1.]))
    glEnd()
########## End ##########    


def main():
    
    #Initialize the library
    if not glfw.init():
        return

    #Create a windowed mode window and its OpenGL context
    window = glfw.create_window(640, 480, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    #Make the window's context current
    glfw.make_context_current(window)

    #Loop until the user closes the window
    while not glfw.window_should_close(window):

        #Poll event
        glfw.poll_events()

        #Render here, e.g. using pyOpenGL
        render()
        #render_resize()
        #render_change_primitive()
        #render_colored()
        #render_red()
        #render_other_forms()

        #Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":  #If the python interpreter in running this source file as the main program,
    main()                  #it sets the special __name__ variable to have a value "__main__".
                            #If this file is being imported from another module,
                            #__name__ will be set to the module's name.

    
