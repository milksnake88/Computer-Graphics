import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os

from camera import Camera

cam = Camera()

WIDTH, HEIGHT = 1280, 1024
gridSize = np.arange(-10.0, 10.0, 0.1)
lastX, lastY = WIDTH/2, HEIGHT/2
first_click = True
left_button_down, right_button_down = False, False
perspective = True

path = None
vertex_pos, normal_pos, faceStrings, normalForEachVertex = None, None, None, None
vertexPosOnlyInVarr, vertexIndexOnlyInFace = None, None

singleMeshRenderingMode = False
hierarchicalModelRenderingMode = False

polygonMode = True
forcedSmoothShading = False


############### callback funtions ###############

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
    global singleMeshRenderingMode, hierarchicalModelRenderingMode
    global polygonMode, forcedSmoothShading
    if key == glfw.KEY_V:
        if action == glfw.PRESS:
            perspective = not perspective
    cam.get_projection(perspective)

    if key == glfw.KEY_H:
        if action == glfw.PRESS:
            singleMeshRenderingMode = False
            hierarchicalModelRenderingMode = True
            hierarchicalModel()

    if key == glfw.KEY_Z:
        if action == glfw.PRESS:
            polygonMode = not polygonMode

    if key == glfw.KEY_S:
        if action == glfw.PRESS:
            forcedSmoothShading = not forcedSmoothShading
            if singleMeshRenderingMode:
                singleMeshModel()
            if hierarchicalModelRenderingMode:
                hierarchicalModel()

def drop_callback(window, paths):
    global singleMeshRenderingMode, hierarchicalModelRenderingMode
    global path
    singleMeshRenderingMode = True
    hierarchicalModelRenderingMode = False
    path = paths
    singleMeshModel()
    printInformation()

def singleMeshModel():
    global path
    global varr
    f = open(path[0], 'r')
    varr = get_varr(f)
    fileName = path[0].split('\\')[-1]

def printInformation():
    global path
    fileName = path[0].split('\\')[-1]
    global totalNumOfFaces, numOfFacesWith3Vertices, numOfFacesWith4Vertices, numOfFacesWithMoreThan4Vertices
    print('1. File name = %s \n' %fileName,
          '2. Total number of faces = %d \n' %totalNumOfFaces,
          '3. Number of faces with 3 vertices = %d \n' %numOfFacesWith3Vertices,
          '4. Number of faces with 4 vertices = %d \n' %numOfFacesWith4Vertices,
          '5. Number of faces with more than 4 vertices = %d \n' %numOfFacesWithMoreThan4Vertices)



############### obj file processing functions ############### 
def hierarchicalModel():
    global varr1, varr2, varr3, varr4, varr5, varr6, varr7
    objFile = [os.path.join(os.getcwd(), 'DarkBlueGem.obj'),
               os.path.join(os.getcwd(), 'Bear.obj'),
               os.path.join(os.getcwd(), 'Tree.obj'),
               os.path.join(os.getcwd(), 'Apple.obj'),
               os.path.join(os.getcwd(), 'Bow.obj'),
               os.path.join(os.getcwd(), 'Ghost.obj'),
               os.path.join(os.getcwd(), 'Star.obj')]
    f1 = open(objFile[0], 'r')
    varr1 = get_varr(f1)    
    f2 = open(objFile[1], 'r')
    varr2 = get_varr(f2)
    f3 = open(objFile[2], 'r')
    varr3 = get_varr(f3)
    f4 = open(objFile[3], 'r')
    varr4 = get_varr(f4)
    f5 = open(objFile[4], 'r')
    varr5 = get_varr(f5)
    f6 = open(objFile[5], 'r')
    varr6 = get_varr(f6)
    f7 = open(objFile[6], 'r')
    varr7 = get_varr(f7)


def get_varr(f):
    global vertex_pos, normal_pos, faceStrings, normalForEachVertex
    global totalNumOfFaces, numOfFacesWith3Vertices, numOfFacesWith4Vertices, numOfFacesWithMoreThan4Vertices

    totalNumOfFaces = 0
    numOfFacesWith3Vertices = 0
    numOfFacesWith4Vertices = 0
    numOfFacesWithMoreThan4Vertices = 0

    vertexStrings = []
    vertexNomalStrings = []
    faceStrings = []
    
    lines = f.readlines()
    for line in lines:
        if line.startswith('v '):
            vertexStrings.append(line.strip('v '))
        if line.startswith('vn '):
            vertexNomalStrings.append(line.strip('vn '))
        if line.startswith('f '):
            faceStrings.append(line.strip('f '))
    
    for face in faceStrings:
        if len(face.split()) == 3:
            numOfFacesWith3Vertices += 1
        elif len(face.split()) == 4:
            numOfFacesWith4Vertices += 1
        else:
            numOfFacesWithMoreThan4Vertices += 1
    totalNumOfFaces = numOfFacesWith3Vertices + numOfFacesWith4Vertices + numOfFacesWithMoreThan4Vertices

    if (numOfFacesWith4Vertices > 0 or numOfFacesWithMoreThan4Vertices > 0):
        faceStrings = triangulate()

    vertex_pos = vertexStrings2Array(vertexStrings)
    normal_pos = normalStrings2Array(vertexNomalStrings)
        
    return createVertexArraySeparate()


def createVertexArraySeparate():
    global vertexPosOnlyInVarr, vertexIndexOnlyInFace, forcedSmoothShading
    varr = np.zeros((len(faceStrings)*6, 3), 'float32')
    vertexIndex = 0
    normalIndex = 0
    vertexPosOnlyInVarr = np.zeros((len(faceStrings)*3, 3))
    vertexIndexOnlyInFace = np.zeros((len(faceStrings), 3))
    i, k, t = 0, 0, 0
    for vertexAndNormalIndex in faceStrings:
        j = 0
        for index in vertexAndNormalIndex.split():
            if '//' in index:
                vertexIndex = int(index.split('//')[0])-1
                normalIndex = int(index.split('//')[-1])-1
            elif '/' in index:
                if len(index.split('/')) == 2:
                    vertexIndex = int(index.split('/')[0])-1
                    normalIndex = int(index.split('/')[0])-1
                else:
                    vertexIndex = int(index.split('/')[0])-1
                    normalIndex = int(index.split('/')[-1])-1
            else:
                vertexIndex = int(f.split()[0])-1
                normalIndex = int(f.split()[0])-1

            vertexPosOnlyInVarr[t] = vertex_pos[vertexIndex]
            vertexIndexOnlyInFace[k][j] = vertexIndex
            
            if forcedSmoothShading:
                normalForEachVertex = calculateNormal(len(vertex_pos))
                varr[i] = normalForEachVertex[vertexIndex]
            else:
                varr[i] = normal_pos[normalIndex]
                
            varr[i+1] = vertex_pos[vertexIndex]
            i += 2
            j += 1
            t += 1
        k += 1
    return varr

        
############### obj file processing functions ###############
def vertexStrings2Array(vertexStrings):
    vertex_pos = np.zeros((len(vertexStrings), 3))
    i = 0
    for vertice in vertexStrings:
        j = 0
        for v in vertice.split():
            vertex_pos[i][j] = (float(v))
            j += 1
            if j == 3:
                break
        i += 1
    return vertex_pos

def normalStrings2Array(vertexNomalStrings):
    normal_pos = np.zeros((len(vertexNomalStrings), 3))
    i = 0
    for normal in vertexNomalStrings:
        j = 0
        for n in normal.split():
            normal_pos[i][j] = (float(n))
            j += 1
            if j == 3:
                break
        i += 1
    return normal_pos

def calculateNormal(l):
    faceNormal = np.zeros((len(faceStrings), 3))
    normalForEachVertex = np.zeros((l, 3))
    i,j = 0,0
    m = 0
    for i in range(len(faceStrings)):
        faceNormal[i] = np.cross(vertexPosOnlyInVarr[j],vertexPosOnlyInVarr[j+1])
        i += 1
        j += 3
    for m in range(l):
        neighborFaceIndex = []
        n = 0
        for line in vertexIndexOnlyInFace:
            if m in line:
                neighborFaceIndex.append(n)
            n += 1
        normalSum = np.zeros(3)
        for index in neighborFaceIndex:
            normalSum += faceNormal[index]
        normalSum_norm = np.sqrt(np.dot(normalSum,normalSum))
        normalForEachVertex[m] = normalSum/normalSum_norm
    return normalForEachVertex
    

def triangulate():
    facesList = []
    nPolygons = []
    for face in faceStrings:
        if(len(face.split()) >= 4):
            nPolygons.append(face)
        else:
            facesList.append(face)
    for face in nPolygons:
        for i in range(1, len(face.split())-1):
            seq = [str(face.split()[0]), str(face.split()[i]), str(face.split()[i+1])]
            string = ' '.join(seq)
            facesList.append(string)
    return facesList



############### object funtions ###############

##### Grid #####
def drawGrid():
    for i in gridSize:
        glBegin(GL_LINES)
        glColor3ub(255,255,255)
        glVertex3f(i, 0.0, -10.0)
        glVertex3f(i, 0.0, 10.0)
        glVertex3f(-10.0, 0.0, i)
        glVertex3f(10.0, 0.0, i)
        glEnd()

##### your object #####
def draw_glDrawArray(varr):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize,
                    ctypes.c_void_p(varr.ctypes.data+3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))



############### render funtion ###############
    
def render():
    global singleMeshRenderingMode, hierarchicalModelRenderingMode
    global polygonMode
    global varr, varr1, varr2, varr3, varr4, varr5, varr6, varr7
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    if polygonMode:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    cam.get_projection(perspective)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    cam.get_gluLookAt()
    
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glEnable(GL_NORMALIZE)

    glPushMatrix()
    lightPos0 = (10.,0.,0.,0.)
    lightPos1 = (-10, 10, 0.,1.)
    lightPos2 = (0.,0.,50.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos0)
    glLightfv(GL_LIGHT1, GL_POSITION, lightPos1)
    glLightfv(GL_LIGHT2, GL_POSITION, lightPos2)
    glPopMatrix()

    lightColor0 = (1.,1.,1.,1.)
    lightColor1 = (1.,1.,1.,.8)
    lightColor2 = (1.,1.,.5,.5)
    ambientLightColor0 = (.075,.075,.075,1.)
    ambientLightColor1 = (.05,.05,.05,1.)
    ambientLightColor2 = (.025,.025,.025,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor0)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, lightColor1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, lightColor1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambientLightColor1)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, lightColor2)
    glLightfv(GL_LIGHT2, GL_SPECULAR, lightColor2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambientLightColor2)

    objectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
    drawGrid()

    ##### object #####
    if singleMeshRenderingMode:
        #single obj color
        objectColor = (1.,1,0.2,.5)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        #single obj
        glPushMatrix()
        draw_glDrawArray(varr)
        glPopMatrix()

    t = glfw.get_time()
        
    if hierarchicalModelRenderingMode:
        #DarkBlueGem color
        objectColor = (.2,.1,1.,.5)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        #DarkBlueGem base transformation
        glPushMatrix()
        glRotatef(t*(18/np.pi), 0, 1, 0)
        #DarkBlueGem base drawing
        glPushMatrix()
        glTranslatef(0,-0.7,0)
        glRotatef(-90,1,0,0)
        glScalef(2., 2., 2.)
        draw_glDrawArray(varr1)
        glPopMatrix()

        #Bear transformation
        objectColor = (.5,.3,0.,1.)
        specularObjectColor = (1.,1.,1.,.3)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        glPushMatrix()
        glTranslatef(-0.4,0,0)
        glRotatef(np.sin(t)*10,0,0,1)
        #Bear drawing
        glPushMatrix()
        glScalef(0.007, 0.007, 0.007)
        glColor3ub(130,60,0)
        draw_glDrawArray(varr2)
        glPopMatrix()

        #Bow transformation&drawing
        objectColor = (.3,.1,0.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        glPushMatrix()
        glColor3ub(255,153,204)
        glScalef(0.4,0.4,0.4)
        glTranslatef(-1.7,1.5,0)
        glRotatef(t*(180/np.pi),1,0,0)
        draw_glDrawArray(varr5)
        glPopMatrix()
        
        #Ghost transformaion&drawing
        objectColor = (1.,.9,.9,.8)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        glPushMatrix()
        glColor3ub(255,255,0)
        glTranslatef(0.,1.9+0.1*np.sin(2*t),0.)
        glScalef(0.03, 0.03, 0.03)
        draw_glDrawArray(varr6)
        glPopMatrix()
        
        glPopMatrix()

        
        #Tree transformation
        objectColor = (.2,.8,.1,1.)
        specularObjectColor = (1.,1.,1.,.3)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 70)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        glPushMatrix()
        glTranslatef(.4,0,0)
        glRotatef(np.sin(t)*10,0,0,1)
        #Tree drawing
        glPushMatrix()
        glScalef(0.2, 0.2, 0.2)
        glColor3ub(102,204,0)
        draw_glDrawArray(varr3)
        glPopMatrix()

        #Apple transformation&drawing
        objectColor = (.7,0.,.1,.5)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 60)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        glPushMatrix()
        glScalef(0.002,0.002,0.002)
        glTranslatef(-90,530,100)
        glRotatef(80*np.sin(1.6*t), 0,0,1)
        glColor3ub(255,0,0)
        draw_glDrawArray(varr4)
        glPopMatrix()
        glPushMatrix()
        glScalef(0.002,0.002,0.002)
        glTranslatef(90,250,200)
        glRotatef(80*np.sin(1.6*t), 0,0,1)
        glColor3ub(255,0,0)
        draw_glDrawArray(varr4)
        glPopMatrix()

        #Star transformation&drawing
        objectColor = (1.,1.,.1,.8)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 80)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        glPushMatrix()
        glTranslatef(-0.06,1.8,0.)
        glScalef(0.008,0.008,0.008)
        glRotatef(t*(180/np.pi),0,1,0)
        glColor3ub(160,160,160)
        draw_glDrawArray(varr7)
        glPopMatrix()
        
        glPopMatrix()

        
        glPopMatrix()


############### main funtion ###############

def main():
    
    if not glfw.init():
        return
    window = glfw.create_window(WIDTH,HEIGHT,'Obj File Viewer', None,None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)
    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_input_mode(window, glfw.STICKY_MOUSE_BUTTONS, glfw.TRUE)
    glfw.set_key_callback(window, key_callback)

    glfw.set_drop_callback(window, drop_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        render()
        
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()

