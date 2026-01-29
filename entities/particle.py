import numpy as np

'''
    __init__
        radius : float
        pos : (x1,x2)
   collision
       ball : Class ball
    apply_force
        force : np.array([x : float, y : float])

        return
            old force at ball
'''

TOL = 0.2

import numpy as np

class Particle:
    def __init__(self, x, y, radius, mass):
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([0.0, 0.0]) # Velocidade inicial
        self.force = np.array([0.0, 0.0])
        self.radius = radius
        self.mass = mass
        self.rho = 0.0
        self.p = 0.0
        
    def collision(self, ball):
        b1_pos = ball.get_pos_np()
        b2_pos = self.get_pos_np()

        dist = np.linalg.norm(b1_pos - b2_pos)
        if dist + TOL < self.radius:
            return 0
        else:
            return dist

    def apply_force(self, force):
        self.force += force
        return self.force
        

    def set_pos(self, pos):
        self.pos = pos

    def get_pos_np(self):
        return np.array([self.pos[0], self.pos[1]])
