import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

from random import uniform
from particleSystem import ParticleSystem

p = ParticleSystem()

def eulerStep(t, h):
    derivative = p.get_derivative()
    states = p.get_state()
    y_cur = states + h*derivative
    p.set_state(y_cur)
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
h = 0.015

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
        particle.vel[0] = uniform(0., .5)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        y_cur = eulerStep(t, h)
        render(y_cur)

        glfw.swap_buffers(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
