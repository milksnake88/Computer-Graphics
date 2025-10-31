import numpy as np

class Joint:
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.offset = np.identity(4)
        self.channels = []
        self.children = []
        self.frames = []

        self.worldpos = np.array([0., 0., 0., 1.])

        
    def add_child(self, child):
        self.children.append(child)

    def update_frame(self, frame):
        xpos, ypos, zpos = 0., 0., 0.
        xrot, yrot, zrot = 0., 0., 0.

        dRotation = np.identity(4)
        dTranslation = np.identity(4)
        
        if frame >= 0:
            index = 0
            for channel in self.channels:
                if channel.lower() == 'xposition':
                    xpos = self.frames[frame][index]
                    dTranslation[0][3] = xpos
                elif channel.lower() == 'yposition':
                    ypos = self.frames[frame][index]
                    dTranslation[1][3] = ypos
                elif channel.lower() == 'zposition':
                    zpos = self.frames[frame][index]
                    dTranslation[2][3] = zpos
                elif channel.lower() == 'xrotation':
                    xrot = self.frames[frame][index]
                    theta = np.radians(xrot)
                    myDRotation = np.array([[1., 0., 0., 0.],
                                             [0., np.cos(theta), -np.sin(theta), 0.],
                                             [0., np.sin(theta), np.cos(theta), 0.],
                                             [0., 0., 0., 1.]])
                    dRotation = np.dot(dRotation, myDRotation)
                elif channel.lower() == 'yrotation':
                    yrot = self.frames[frame][index]
                    theta = np.radians(yrot)
                    myDRotation = np.array([[np.cos(theta), 0., np.sin(theta), 0.],
                                             [0., 1., 0., 0.],
                                             [-np.sin(theta), 0., np.cos(theta), 0.],
                                             [0., 0., 0., 1.]])
                    dRotation = np.dot(dRotation, myDRotation)
                elif channel.lower() == 'zrotation':
                    zrot = self.frames[frame][index]
                    theta = np.radians(zrot)
                    myDRotation = np.array([[np.cos(theta), -np.sin(theta), 0., 0.],
                                             [np.sin(theta), np.cos(theta), 0., 0.],
                                             [0., 0., 1., 0.],
                                             [0., 0., 0., 1.]])
                    dRotation = np.dot(dRotation, myDRotation)
                index += 1

        self.dRotation = dRotation
        self.dTranslation = dTranslation

        if self.parent:
            self.local2world = np.dot(self.parent.transformation, self.offset)
        else:
             self.local2world = np.dot(self.offset, self.dTranslation)

        self.transformation = np.dot(self.local2world, self.dRotation)
        self.worldpos = np.array([self.local2world[0][3],
                                  self.local2world[1][3],
                                  self.local2world[2][3],
                                  self.local2world[3][3]])
                    
        
        if frame < 0:
            self.worldpos = self.parent.worldpos + self.offset[:,3] if self.parent else self.offset[:,3]

        for child in self.children:
            child.update_frame(frame)
    
                    
class BvhReader:
    def __init__(self, f):
        self.file = f
        
        self.numOfFrames = 0
        self.FPS = 0
        self.numOfJoints = 0
        self.listOfJoints = []

        self.dicOfJoints = {}
        self.root = None

        self.bvhJoints()

    def bvhJoints(self):
        lines = self.file.readlines()
        jointStack = []
        channelData = []
        frame = 0
        numOfJoints = 0
        
        for l in lines:
            line = l.strip()
            words = line.split()
            #hierarchy
            if line.startswith('HIERARCHY'):
                pass
            elif line.startswith('ROOT') or line.startswith('JOINT'):
                parent = jointStack[-1] if line.startswith('JOINT') else None
                joint = Joint(parent, words[-1])
                self.listOfJoints.append(joint.name)
                self.dicOfJoints[joint.name] = joint
                numOfJoints += 1
                if parent:
                    parent.add_child(joint)
                jointStack.append(joint)
                if line.startswith('ROOT'):
                    self.root = joint
            elif line.startswith('{'):
                pass
            elif line.startswith('OFFSET'):
                for i in range(1, len(words)):
                    jointStack[-1].offset[i-1][3] = float(words[i])
            elif line.startswith('CHANNELS'):
                for i in range(2, len(words)):
                    jointStack[-1].channels.append(words[i])
            elif line.startswith('End'):
                joint = Joint(jointStack[-1], jointStack[-1].name + 'EndSite')
                jointStack[-1].add_child(joint)
                jointStack.append(joint)
                self.dicOfJoints[joint.name] = joint
            elif line.startswith('}'):
                jointStack.pop()
            #motion
            else:
                if line.startswith('MOTION'):
                    pass
                elif line.startswith('Frames:'):
                    self.numOfFrames = int(words[-1])
                elif line.startswith('Frame Time:'):
                    self.FPS = float(words[-1])
                else:
                    for i in range(len(words)):
                        channelData.append(float(words[i]))
                    frame += 1

        
        for i in range(self.numOfFrames):
            channelData = self.get_channelData(self.root, channelData)

        self.numOfJoints = numOfJoints
                                               

    def update_frame(self, frame):
        self.root.update_frame(frame)
        
        
    def get_information(self):
        return self.numOfFrames, self.FPS, self.numOfJoints, self.listOfJoints


    def get_channelData(self, joint, channelData):
        channels = len(joint.channels)
        joint.frames.append(channelData[0:channels])
        channelData = channelData[channels:]

        for child in joint.children:
            channelData = self.get_channelData(child, channelData)

        return channelData
        
            
