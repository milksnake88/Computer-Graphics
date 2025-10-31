import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from random import uniform
from particleSystem import ParticleSystem

p = ParticleSystem()

def Runge_Kutta(t, h, particles):
    initialStates = np.zeros(p.n * 6)
    k = 0
    for particle in p.particles:
        initialStates[k] = particle.pos[0]
        initialStates[k + 1] = particle.pos[1]
        initialStates[k + 2] = particle.pos[2]
        initialStates[k + 3] = particle.vel[0]
        initialStates[k + 4] = particle.vel[1]
        initialStates[k + 5] = particle.vel[2]
        k += 6
        
    k1 = h * p.get_derivative(particles)

    k = 0
    for particle in p.particles:
        particle.pos[0] = initialStates[k] + k1[k]/2
        particle.pos[1] = initialStates[k+1] + k1[k+1]/2
        particle.pos[2] = initialStates[k+2] + k1[k+2]/2
        particle.vel[0] = initialStates[k+3] + k1[k+3]/2
        particle.vel[1] = initialStates[k+4] + k1[k+4]/2
        particle.vel[2] = initialStates[k+5] + k1[k+5]/2
        k += 6
        
    k2 = h * p.get_derivative(particles)

    k = 0
    for particle in p.particles:
        particle.pos[0] = initialStates[k] + k2[k]/2
        particle.pos[1] = initialStates[k+1] + k2[k+1]/2
        particle.pos[2] = initialStates[k+2] + k2[k+2]/2
        particle.vel[0] = initialStates[k+3] + k2[k+3]/2
        particle.vel[1] = initialStates[k+4] + k2[k+4]/2
        particle.vel[2] = initialStates[k+5] + k2[k+5]/2
        k += 6
        
    k3 = h * p.get_derivative(particles)

    k = 0
    for particle in p.particles:
        particle.pos[0] = initialStates[k] + k3[k]
        particle.pos[1] = initialStates[k+1] + k3[k+1]
        particle.pos[2] = initialStates[k+2] + k3[k+2]
        particle.vel[0] = initialStates[k+3] + k3[k+3]
        particle.vel[1] = initialStates[k+4] + k3[k+4]
        particle.vel[2] = initialStates[k+5] + k3[k+5]
        k += 6
        
    k4 = h * p.get_derivative(particles)
    
    newStates = initialStates + k1/6 + k2/3 + k3/3 + k4/6
    p.set_state(particles, newStates)
    p.collision_response(particles)
    y_cur = p.get_state(particles)

    t += h
    return y_cur

    
def render(y_cur):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # floor
    glBegin(GL_LINES)
    glColor3ub(255, 255, 255)
    glVertex3fv(np.array([-1., 0., 0.]))
    glVertex3fv(np.array([1., 0., 0.]))
    glEnd()

    # particles
    k = 0
    for i in range(ParticleSystem.n):
        glPointSize(10)
        glBegin(GL_POINTS)
        glColor3ub(255, 255, 255)
        glVertex3fv(np.array([ y_cur[k], y_cur[k+1], y_cur[k+2] ]))
        glEnd()
        k += 6

    # spring
    k = 0
    for i in range(ParticleSystem.n):
        if (i < ParticleSystem.n -1):
            glBegin(GL_LINES)
            glColor3ub(255, 255, 255)
            glVertex3fv(np.array([ y_cur[k], y_cur[k+1], y_cur[k+2] ]))
            glVertex3fv(np.array([ y_cur[k+6], y_cur[k+7], y_cur[k+8] ]))
            glEnd()
            k += 6
        else:
            glBegin(GL_LINES)
            glColor3ub(255, 255, 255)
            glVertex3fv(np.array([ y_cur[k], y_cur[k+1], y_cur[k+2] ]))
            glVertex3fv(np.array([ y_cur[0], y_cur[1], y_cur[2] ]))
            glEnd()
        
t = 0.0
h = 0.01

def main():
    if not glfw.init():
        return
    window = glfw.create_window(1200, 1200, "particle_plane_collisions", None, None)
    if not window:
        glfw.terminate()
        return

    p.particles[0].pos = np.array([-0.3, 0., 0.])
    p.particles[1].pos = np.array([0.3, 0., 0.])
    p.particles[2].pos = np.array([0.3, 0.6, 0.])
    p.particles[3].pos = np.array([-0.3, 0.6, 0.])
    '''
    for particle in p.particles:
        particle.vel[0] = uniform(0., .5)
        particle.vel[1] = uniform(0., .5)
    '''
    particles = p.particles

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        y_cur = Runge_Kutta(t, h, particles)
        render(y_cur)

        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
