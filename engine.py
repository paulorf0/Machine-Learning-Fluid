'''
    __init__
        radius : float # Particle radius
        sim_density : int # Amount of particles per cell. Ex: 4 particles

    get_cell
        pos : np.array((x : float, y : float))
'''

import numpy as np

from entities.particle import Particle

from kernel.poly6 import Poly6
from kernel.spiky_gradient import Spiky_Gradient
from kernel.viscosity_laplacian import Viscosity_Lapaclian

REST_DENS = 1000.0  # Densidade da água (kg/m^3)
STIFFNESS = 2000.0  # Constante do Gás (k) - Pressão
VISC      = 200.0   # Viscosidade (mu)
GRAVITY = 9.84
DT        = 0.005   # Passo de Tempo (0.005s = 200 passos/segundo)


class Engine:
    def __init__(self, radius, h, width, height):
        self.radius = radius
        self.h = h # Smoothing Radius e tamanho da célula 
        self.width = width
        self.height = height
        
        self.particles = []
        self.space = {}

    def loop(self):
        self.update_grid()

        # Calc density and pressure
        for p in self.particles:
            p.rho = 0.0
            p.force = np.array([0.0, 0.0]) 
            
            neighbors = self.get_neighbors(p)
            
            for n in neighbors:
                diff_pos = p.pos - n.pos
                r2 = np.dot(diff_pos, diff_pos) # r**2
                
                if r2 < self.h * self.h:
                    r = np.sqrt(r2)
                    p.rho += n.mass * Poly6(r, self.h)
            
            p.rho = max(p.rho, REST_DENS) 
            
            p.p = STIFFNESS * (p.rho - REST_DENS)

        # Calc intern pressure and viscosity
        for p in self.particles:
            f_pressure = np.array([0.0, 0.0])
            f_viscosity = np.array([0.0, 0.0])
            
            neighbors = self.get_neighbors(p)
            
            for n in neighbors:
                if p == n:
                    continue 
                
                diff_pos = p.pos - n.pos
                r2 = np.dot(diff_pos, diff_pos)
                
                if r2 < self.h * self.h:
                    r = np.sqrt(r2)
                    grad_w = Spiky_Gradient(diff_pos, r, self.h) 
                    
                    term_press = (p.p + n.p) / (2 * n.rho) 
                    f_pressure -= n.mass * term_press * grad_w # F = -m * term * grad

                    lap_w = Viscosity_Lapaclian(r, self.h) 
                    vel_diff = n.vel - p.vel
                    
                    term_visc = (vel_diff / n.rho) * lap_w
                    f_viscosity += VISC * n.mass * term_visc
            
            f_gravity = p.rho * GRAVITY 

            p.force = f_pressure + f_viscosity + f_gravity

        # Temporal integration
        for p in self.particles:
            if p.rho > 0:
                acc = p.force / p.rho
            else:
                acc = np.array([0.0, 0.0])

            # Euler Semi-Implicito / Leap Frog Simplificado
            p.vel += acc * DT
            p.pos += p.vel * DT
            
            # wall collision
            self.handle_boundary(p)

    def handle_boundary(self, p):
        damping = 0.5 
        
        # Left
        if p.pos[0] < self.radius:
            p.pos[0] = self.radius
            p.vel[0] *= -damping
            
        # Right
        elif p.pos[0] > self.width - self.radius:
            p.pos[0] = self.width - self.radius
            p.vel[0] *= -damping

        # Up
        if p.pos[1] < self.radius:
            p.pos[1] = self.radius
            p.vel[1] *= -damping
            
        # bottom
        elif p.pos[1] > self.height - self.radius:
            p.pos[1] = self.height - self.radius
            p.vel[1] *= -damping

    def init_particles(self, rows, cols, start_x, start_y):
        spacing = self.radius * 2 
        
        for i in range(rows):
            for j in range(cols):
                x = start_x + i * spacing
                y = start_y + j * spacing
                p = Particle(x, y, self.radius, mass=1.0)
                self.particles.append(p)

        self.update_grid()


    def update_grid(self):
        self.space = {} 
        for p in self.particles:
            cell_x = int(p.pos[0] / self.h)
            cell_y = int(p.pos[1] / self.h)
            
            cell_key = (cell_x, cell_y)

            if cell_key not in self.space:
                self.space[cell_key] = []
            
            self.space[cell_key].append(p)

    def get_neighbors(self, particle):
        neighbors = []
        cx = int(particle.pos[0] / self.h)
        cy = int(particle.pos[1] / self.h)

        for i in range(cx - 1, cx + 2):
            for j in range(cy - 1, cy + 2):
                key = (i, j)
                if key in self.space:
                    # Adiciona todas as partículas dessa célula à lista de potenciais vizinhos
                    neighbors.extend(self.space[key])
        
        return neighbors