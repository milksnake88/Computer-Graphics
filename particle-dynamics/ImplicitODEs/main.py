import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from random import uniform
from particleSystem import ParticleSystem

p = ParticleSystem()

def eulerStep(t, h, particles):
    derivative_n0 = p.get_derivative(particles)
    states_n0 = p.get_state(particles)
    y_n0 = states_n0 + h*derivative_n0
    p.set_state(particles, y_n0)
    
    derivative_n1 = p.get_derivative(particles)
    states_n1 = p.get_state(particles)
    y_n1 = states_n1 + h*derivative_n1
    p.set_state(particles, y_n1)
    
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
    
    k = 0
    for i in range(ParticleSystem.n):
        glPointSize(10)
        glBegin(GL_POINTS)
        glColor3ub(255, 255, 255)
        glVertex3fv(np.array([ y_cur[k], y_cur[k+1], y_cur[k+2] ]))
        glEnd()
        k += 6

t = 0.0
h = 0.001

def main():
    if not glfw.init():
        return
    window = glfw.create_window(1200, 1200, "particle_plane_collisions", None, None)
    if not window:
        glfw.terminate()
        return

    for particle in p.particles:
        particle.pos[0] = uniform(-.8, 0.)
        particle.pos[1] = uniform(.5, 1.)
        particle.vel[0] = uniform(0., .5)
        particle.vel[1] = uniform(0., .5)

    particles = p.particles

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        y_cur = eulerStep(t, h, particles)
        render(y_cur)

        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
