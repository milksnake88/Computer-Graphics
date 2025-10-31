import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import os

from camera import Camera
from bvhReader import BvhReader

cam = Camera()

WIDTH, HEIGHT = 1280, 1024
gridSize = np.arange(-10.0, 10.0, 0.1)
lastX, lastY = WIDTH/2, HEIGHT/2
first_click = True
left_button_down, right_button_down = False, False
perspective = True

#obj
vertex_pos, normal_pos, faceStrings, normalForEachVertex = None, None, None, None
vertexPosOnlyInVarr, vertexIndexOnlyInFace = None, None

objRenderingMode = False

#bvh
dropped = False
frame = None
lineRenderingMode, boxRenderingMode, motionMode = True, False, False


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
    global objRenderingMode
    global lineRenderingMode, boxRenderingMode, motionMode
    if key == glfw.KEY_V:
        if action == glfw.PRESS:
            perspective = not perspective
    cam.get_projection(perspective)
    #obj
    if key == glfw.KEY_O:
        if action == glfw.PRESS:
            objRenderingMode = not objRenderingMode
            objModel()

    #bvh
    if key == glfw.KEY_1:
        if action == glfw.PRESS:
            boxRenderingMode = False
            lineRenderingMode = True
    if key == glfw.KEY_2:
        if action == glfw.PRESS:
            lineRenderingMode = False
            boxRenderingMode = True

    if key == glfw.KEY_SPACE:
        if action == glfw.PRESS:
            motionMode = not motionMode
            

def drop_callback(window, paths):
    global dropped, bvh, cnt, frame, motionMode
    dropped = True
    motionMode = False
    if '\\' in paths[0]:
        fileName = paths[0].split('\\')[-1]
    elif '/' in paths[0]:
        fileName = paths[0].split('/')[-1]
    else:
        fileName = paths[0]
    with open(paths[0]) as f:
        bvh = BvhReader(f)

    print_information(fileName)
    cnt = -1
    frame = -1
    bvh.update_frame(frame)


############### obj file processing functions ############### 
def objModel():
    global varr1, varr2, varr3, varr4, varr5, varr6, varr7, varr8, varr9
    objFile = [os.path.join(os.getcwd(), 'bone1.obj'),
               os.path.join(os.getcwd(), 'bone2.obj'),
               os.path.join(os.getcwd(), 'bone3.obj'),
               os.path.join(os.getcwd(), 'head.obj'),
               os.path.join(os.getcwd(), 'harts.obj'),
               os.path.join(os.getcwd(), 'harts1.obj'),
               os.path.join(os.getcwd(), 'harts2.obj'),
               os.path.join(os.getcwd(), 'harts3.obj'),
               os.path.join(os.getcwd(), 'harts4.obj')]
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
    f8 = open(objFile[7], 'r')
    varr8 = get_varr(f8)
    f9 = open(objFile[8], 'r')
    varr9 = get_varr(f9)

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


##### your object bvh #####
def boxDrawing(head, tail):

	posOfHead = np.array([head[0], head[1], head[2]])
	posOfTail = np.array([tail[0], tail[1], tail[2]])

	#width = 3
	width = 0.05

	glColor3ub(102, 102, 255)
	
	point = np.empty((2,4), dtype=object)
	
	v1 = posOfHead - posOfTail
	v1 = v1 / (np.sqrt(np.dot(v1, v1)))
	up = np.array([0.0, 1, 0.0])
	if 1.0 - v1[1] < 0.001:
		up[2] += 0.1

	v2 = np.cross(v1, up)
	v2 = v2 / (np.sqrt(np.dot(v2, v2)))
	
	v3 = np.cross(v1, v2)
	v3 = v3 / (np.sqrt(np.dot(v3, v3)))

	v2 *= width
	v3 *= width

	point[0][0] = posOfHead + v2
	point[0][2] = posOfHead - v2
	point[0][1] = posOfHead + v3
	point[0][3] = posOfHead - v3

	point[1][0] = posOfTail + v2
	point[1][2] = posOfTail - v2
	point[1][1] = posOfTail + v3
	point[1][3] = posOfTail - v3

	glBegin(GL_QUADS)
	for i in range(2):
		glNormal3f(v1[0], v1[0], v1[0])
		for p in point[i]:
			glVertex3f(p[0], p[1], p[2])
	
	n1 = v2 + v3
	n1 = n1 / (np.sqrt(np.dot(n1, n1)))

	n2 = v2 - v3
	n2 = n2 / (np.sqrt(np.dot(n2, n2)))	

	glNormal3f(n1[0], n1[1], n1[2])
	glVertex3f(point[0][0][0], point[0][0][1], point[0][0][2])
	glVertex3f(point[1][0][0], point[1][0][1], point[1][0][2])
	glVertex3f(point[1][1][0], point[1][1][1], point[1][1][2])
	glVertex3f(point[0][1][0], point[0][1][1], point[0][1][2])

	glNormal3f(n2[0], n2[1], n2[2])
	glVertex3f(point[0][1][0], point[0][1][1], point[0][1][2])
	glVertex3f(point[1][1][0], point[1][1][1], point[1][1][2])
	glVertex3f(point[1][2][0], point[1][2][1], point[1][2][2])
	glVertex3f(point[0][2][0], point[0][2][1], point[0][2][2])

	glNormal3f(-n1[0], -n1[1], -n1[2])
	glVertex3f(point[0][2][0], point[0][2][1], point[0][2][2])
	glVertex3f(point[1][2][0], point[1][2][1], point[1][2][2])
	glVertex3f(point[1][3][0], point[1][3][1], point[1][3][2])
	glVertex3f(point[0][3][0], point[0][3][1], point[0][3][2])

	glNormal3f(-n2[0], -n2[1], -n2[2])
	glVertex3f(point[0][3][0], point[0][3][1], point[0][3][2])
	glVertex3f(point[1][3][0], point[1][3][1], point[1][3][2])
	glVertex3f(point[1][0][0], point[1][0][1], point[1][0][2])
	glVertex3f(point[0][0][0], point[0][0][1], point[0][0][2])

	glEnd()

	
def print_information(fileName):
    numOfFrames, FPS, numOfJoints, listOfJoints = bvh.get_information()
    print("1. File name: %s \n" %fileName,
          "2. Number of frames: %d \n" %numOfFrames,
          "3. FPS (which is 1/FrameTime): %f \n" %FPS,
          "4. Number of joints (including root): %d \n" %numOfJoints,
          "5. List of all joint names:", listOfJoints)

def get_position(joint):
    pos = [joint.worldpos[0], joint.worldpos[1], joint.worldpos[2]]
    return pos

def draw_joint(joint):
    pos = get_position(joint)

    if joint.parent:
        head = get_position(joint.parent)
        tail = pos
        if lineRenderingMode:
            glBegin(GL_LINES)
            glColor3ub(102,102,255)
            glVertex3f(head[0], head[1], head[2])
            glVertex3f(tail[0], tail[1], tail[2])
            glEnd()
        if boxRenderingMode:
            boxDrawing(head, tail)

    for child in joint.children:
        draw_joint(child)



############### render funtion ###############
    
def render():
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

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
        
    if objRenderingMode:
        #born1 color
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t1 = bvh.root.children[1].transformation #RightUpLeg
        #born1 transformation
        glPushMatrix()
        glMultMatrixf(t1.T)
        #born1 drawing
        glPushMatrix()
        glScalef(.2, .2, .2)
        glRotatef(45, 0, 0, -1)
        draw_glDrawArray(varr1)
        glPopMatrix()
        glPopMatrix()

        #born2 color
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t2 = bvh.root.children[2].transformation #LeftUpLeg
        #born2 transformation
        glPushMatrix()
        glMultMatrixf(t2.T)
        #born2 drawing
        glPushMatrix()
        glScalef(.2, .2, .2)
        glRotatef(45, 0, 0, 1)
        draw_glDrawArray(varr2)
        glPopMatrix()
        glPopMatrix()

        #born4 color
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t6 = bvh.root.children[2].children[0].transformation #LeftUpLeg
        #born2 transformation
        glPushMatrix()
        glMultMatrixf(t6.T)
        #born2 drawing
        glPushMatrix()
        glScalef(.005, .005, .005)
        glRotatef(90, -1, 0, 0)
        draw_glDrawArray(varr6)
        glPopMatrix()
        glPopMatrix()

        #born4 color
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t7 = bvh.root.children[1].children[0].transformation #LeftUpLeg
        #born2 transformation
        glPushMatrix()
        glMultMatrixf(t7.T)
        #born2 drawing
        glPushMatrix()
        glScalef(.005, .005, .005)
        glRotatef(90, -1, 0, 0)
        draw_glDrawArray(varr7)
        glPopMatrix()
        glPopMatrix()
        
        #born3 color
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t3 = bvh.root.children[0].transformation #Spine
        #born3 transformation
        glPushMatrix()
        glMultMatrixf(t3.T)
        #born3 drawing
        glPushMatrix()
        glScalef(.3, .3, .3)
        draw_glDrawArray(varr3)
        glPopMatrix()
        glPopMatrix()

        #Head color
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t4 = bvh.root.children[0].children[0].transformation #Head
        #Head transformation
        glPushMatrix()
        glMultMatrixf(t4.T)
        #Head drawing
        glPushMatrix()
        glScalef(.1, .1, .1)
        glRotatef(180, 0, 1, 0)
        draw_glDrawArray(varr4)
        glPopMatrix()
        glPopMatrix()

        #harts color
        objectColor = (1.,.2,.1,.5)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t5 = bvh.root.transformation #Hips
        #harts transformation
        glPushMatrix()
        glMultMatrixf(t5.T)
        #harts drawing
        glPushMatrix()
        glScalef(.009, .009, .009)
        glRotatef(90, -1, 0, 0)
        glTranslatef(1, -1, 0)
        draw_glDrawArray(varr5)
        glPopMatrix()
        glPopMatrix()

        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t8 = bvh.root.children[0].children[1].transformation #Spine
        #born3 transformation
        glPushMatrix()
        glMultMatrixf(t8.T)
        #born3 drawing
        glPushMatrix()
        glScalef(.005, .005, .005)
        glRotatef(90, -1, 0, 0)
        draw_glDrawArray(varr7)
        glPopMatrix()
        glPopMatrix()

        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        t9 = bvh.root.children[0].children[2].transformation #Spine
        #born3 transformation
        glPushMatrix()
        glMultMatrixf(t9.T)
        #born3 drawing
        glPushMatrix()
        glScalef(.005, .005, .005)
        glRotatef(90, -1, 0, 0)
        draw_glDrawArray(varr9)
        glPopMatrix()
        glPopMatrix()
        

    ##### bvh object #####
    if dropped:
        objectColor = (.4,.4,1.,.5)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specularObjectColor)
        glPushMatrix()
        #glScalef(.012, .012, .012)
        draw_joint(bvh.root)
        glPopMatrix()


############### main funtion ###############

def main():
    global frame, cnt
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

        if motionMode == True:
            cnt += 1
            frame = int(cnt/(60*(bvh.FPS)))%bvh.numOfFrames
            bvh.update_frame(frame)
            
        render()
        
        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()

