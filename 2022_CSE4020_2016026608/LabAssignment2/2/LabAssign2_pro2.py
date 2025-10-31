import glfw
from OpenGL.GL import *

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    glVertex2f(0.5,0.5)
    glVertex2f(-0.5,0.5)
    glVertex2f(-0.5,-0.5)
    glVertex2f(0.5,-0.5)
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016026608", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()
        
        glfw.swap_buffers(window)

    glfw.terminate()


#render with different primitive types

def render_with_key(primitiveType):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(primitiveType)
    glVertex2f(0.5,0.5)
    glVertex2f(-0.5,0.5)
    glVertex2f(-0.5,-0.5)
    glVertex2f(0.5,-0.5)
    glEnd()

def get_primitiveType():
    global primitiveType
    key = input("Enter the key to change the primitive type : ")
    if key == '1':
        primitiveType = GL_POINTS
    elif key == '2':
        primitiveType = GL_LINES
    elif key == '3':
        primitiveType = GL_LINE_STRIP
    elif key == '4':
        primitiveType = GL_LINE_LOOP
    elif key == '5':
        primitiveType = GL_TRIANGLES
    elif key == '6':
        primitiveType = GL_TRIANGLE_STRIP
    elif key == '7':
        primitiveType = GL_TRIANGLE_FAN
    elif key == '8':
        primitiveType = GL_QUADS
    elif key == '9':
        primitiveType = GL_QUAD_STRIP
    else :
        primitiveType = GL_POLYGON
    return primitiveType

def main_with_key():
    get_primitiveType()
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016026608", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render_with_key(primitiveType)
        
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
    main_with_key()

