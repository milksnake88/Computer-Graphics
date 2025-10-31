import numpy as np


class Particle:
    def __init__(self):
        # particle
        self.mass = 1.
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.force = np.zeros(3)
        self.contact = False

class ParticleSystem:
    n = 10  # number of particles

    def __init__(self):
        self.particles = [Particle() for i in range(ParticleSystem.n)]

    def get_state(self, particles):
        states = np.zeros(ParticleSystem.n * 6)
        k = 0
        for particle in particles:
            states[k] = particle.pos[0]
            states[k + 1] = particle.pos[1]
            states[k + 2] = particle.pos[2]
            states[k + 3] = particle.vel[0]
            states[k + 4] = particle.vel[1]
            states[k + 5] = particle.vel[2]
            k += 6
        return states

    def set_state(self, particles, newStates):
        k = 0
        for particle in particles:
            particle.pos[0] = newStates[k]
            particle.pos[1] = newStates[k + 1]
            particle.pos[2] = newStates[k + 2]
            particle.vel[0] = newStates[k + 3]
            particle.vel[1] = newStates[k + 4]
            particle.vel[2] = newStates[k + 5]
            k += 6

    def get_derivative(self, particles):
        self.clear_force(particles)
        self.compute_force(particles)
        derivative = np.zeros(ParticleSystem.n * 6)
        k = 0
        for particle in particles:
            derivative[k] = particle.vel[0]
            derivative[k + 1] = particle.vel[1]
            derivative[k + 2] = particle.vel[2]
            derivative[k + 3] = particle.force[0] / particle.mass
            derivative[k + 4] = particle.force[1] / particle.mass
            derivative[k + 5] = particle.force[2] / particle.mass
            k += 6
        return derivative

    def clear_force(self, particles):
        for particle in particles:
            particle.force = np.zeros(3)

    def compute_force(self, particles):
        g = np.array([0., -9.8, 0.])

        eps = 0.01
        kf = 0.5
        N = np.array([0., 1., 0.])  # normal vector of the floor
        P = np.array([0., 0., 0.])  # a point on the plane

        for particle in particles:
            # gravity
            particle.force += particle.mass * g

            # friction
            V_N = (np.dot(N, particle.vel)) * N  # normal component of a pos vector
            V_T = particle.vel - V_N  # tangential component of pos vector
            V_T_norm = np.sqrt(np.dot(V_T, V_T))

            particlePositionInNormalDirection = self.get_particlePositionInNormalDirection(particle)
            particleVelocityInNormalDirection = self.get_particleVelocityInNormalDirection(particle)

            if (abs(particlePositionInNormalDirection) < eps) and (abs(particleVelocityInNormalDirection) < eps):
                particle.contact = True
                friction = -kf * -np.dot(particle.force, N) * (V_T / V_T_norm)
                particle.force = friction

                if np.sqrt(np.dot(V_T, V_T)) < 0.005:
                    particle.vel = np.zeros(3)

                '''                
                if V_T < 0.005:
                    V_T = np.zeros(3)
                '''
                '''
                for i in range(3):
                    if abs(particle.vel[i]) < 0.01:
                        particle.vel[i] = 0.0
                        particle.vel
                '''
            else:
                particle.contact = False

    def collision_response(self, particles):
        kr = 0.7
        eps = 0.01
        N = np.array([0., 1., 0.])  # normal vector of the floor
        P = np.array([0., 0., 0.])  # a point on the plane

        for particle in particles:
            if not particle.contact:
                V_N = (np.dot(N, particle.vel)) * N  # normal component of a pos vector
                V_T = particle.vel - V_N  # tangential component of pos vector

                particlePositionInNormalDirection = self.get_particlePositionInNormalDirection(particle)
                particleVelocityInNormalDirection = self.get_particleVelocityInNormalDirection(particle)

                if (particlePositionInNormalDirection < eps) and (particleVelocityInNormalDirection < 0):
                    particle.vel = V_T - kr * V_N

    def get_particlePositionInNormalDirection(self, particle):
        N = np.array([0., 1., 0.])  # normal vector of the floor
        P = np.array([0., 0., 0.])  # a point on the plane
        return np.dot((particle.pos - P), N)

    def get_particleVelocityInNormalDirection(self, particle):
        N = np.array([0., 1., 0.])  # normal vector of the floor
        return np.dot(N, (particle.vel))

