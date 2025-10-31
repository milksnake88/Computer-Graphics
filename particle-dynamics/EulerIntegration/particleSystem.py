import numpy as np


class Particle:
    def __init__(self):
        # particle
        self.mass = 1.
        self.pos = np.zeros(3)
        self.vel = np.zeros(3)
        self.force = np.zeros(3)


class ParticleSystem:
    n = 10  # number of particles

    def __init__(self):
        self.particles = [Particle() for i in range(ParticleSystem.n)]


    def get_state(self):
        states = np.zeros(ParticleSystem.n * 6)
        k = 0
        for i in range(ParticleSystem.n):
            states[k] = self.particles[i].pos[0]
            states[k + 1] = self.particles[i].pos[1]
            states[k + 2] = self.particles[i].pos[2]
            states[k + 3] = self.particles[i].vel[0]
            states[k + 4] = self.particles[i].vel[1]
            states[k + 5] = self.particles[i].vel[2]
            k += 6
        return states


    def set_state(self, newStates):
        k = 0
        for i in range(ParticleSystem.n):
            self.particles[i].pos[0] = newStates[k]
            self.particles[i].pos[1] = newStates[k + 1]
            self.particles[i].pos[2] = newStates[k + 2]
            self.particles[i].vel[0] = newStates[k + 3]
            self.particles[i].vel[1] = newStates[k + 4]
            self.particles[i].vel[2] = newStates[k + 5]
            k += 6


    def get_derivative(self):
        self.clear_force()
        self.compute_force()
        derivative = np.zeros(ParticleSystem.n * 6)
        k = 0
        for i in range(ParticleSystem.n):
            derivative[k] = self.particles[i].vel[0]
            derivative[k + 1] = self.particles[i].vel[1]
            derivative[k + 2] = self.particles[i].vel[2]
            derivative[k + 3] = self.particles[i].force[0] / self.particles[i].mass
            derivative[k + 4] = self.particles[i].force[1] / self.particles[i].mass
            derivative[k + 5] = self.particles[i].force[2] / self.particles[i].mass
            k += 6
        return derivative


    def clear_force(self):
        for i in range(ParticleSystem.n):
            self.particles[i].force = np.zeros(3)


    def compute_force(self):
        g = np.array([0., -9.8, 0.])
        
        eps = 0.01
        kr = 0.6
        kf = 0.7
        N = np.array([0., 1., 0.])  # normal vector of the floor
        P = np.array([0., 0., 0.])  # a point on the plane

        for i in range(ParticleSystem.n):
            # gravity
            self.particles[i].force += self.particles[i].mass * g

            V_N = (np.dot(N, self.particles[i].vel)) * N  # normal component of a pos vector
            V_T = self.particles[i].vel - V_N  # tangential component of pos vector
            V_T_norm = np.sqrt(np.dot(V_T, V_T))

            distance_vector_norm = np.sqrt(np.dot(self.particles[i].pos - P, self.particles[i].pos - P))
            distance_vector = (self.particles[i].pos - P)/distance_vector_norm
            distance_angle = np.dot(distance_vector, N)

            collision_vector_norm = np.sqrt(np.dot(self.particles[i].vel, self.particles[i].vel))
            collision_vector = self.particles[i].vel / collision_vector_norm
            collision_angle = np.dot(N, collision_vector)

            if (abs(distance_angle) < eps) and (abs(collision_angle) < eps):
                friction = -kf * (-np.dot(self.particles[i].force, N))*(V_T/V_T_norm)
                normal = -np.dot(self.particles[i].mass*g, N)*N
                self.particles[i].force += friction + normal
                #print('O')
            elif (distance_angle < eps) and (collision_angle < 0):
                self.particles[i].vel = V_T - kr*V_N
                #print('X')
