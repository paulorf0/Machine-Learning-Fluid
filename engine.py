'''
    __init__
        radius : float # Particle radius
        sim_density : int # Amount of particles per cell. Ex: 4 particles

    get_cell
        pos : np.array((x : float, y : float))
'''


from entities.particle import Particle

class Engine:
    def __init__(self, radius, h, width, height):
        self.radius = radius
        self.h = h # Smoothing Radius e tamanho da célula 
        self.width = width
        self.height = height
        
        self.particles = []
        self.space = {}

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