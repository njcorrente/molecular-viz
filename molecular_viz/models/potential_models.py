import numpy as np

class PotentialModel:
    def __init__(self, epsilon_over_kB, sigma):
        self.epsilon_over_kB = epsilon_over_kB
        self.sigma = sigma

class LennardJones(PotentialModel):
    def __init__(self, epsilon_over_kB=120.0, sigma=3.4):
        super().__init__(epsilon_over_kB, sigma)
        self.name = "Lennard-Jones"
        self.description = "Most commonly used for noble gases and simple molecules. Combines short-range repulsion (r⁻¹²) with longer-range attraction (r⁻⁶). The r⁻⁶ term represents van der Waals forces."
        self.equation = r"$V(r) = 4\varepsilon[(\sigma/r)^{12} - (\sigma/r)^6]$"

    def calculate(self, r):
        return 4 * self.epsilon_over_kB * ((self.sigma/r)**12 - (self.sigma/r)**6)

class HardSphere(PotentialModel):
    def __init__(self, epsilon_over_kB=120.0, sigma=3.4):
        super().__init__(epsilon_over_kB, sigma)
        self.name = "Hard Sphere"
        self.description = "Simplest model where particles act as perfect rigid spheres. Used for studying entropy-driven phenomena and as a reference system for more complex fluids."
        self.equation = r"$V(r) = \infty$ for $r < \sigma$, $0$ for $r \geq \sigma$"

    def calculate(self, r):
        mask = r < self.sigma
        potential = np.zeros_like(r)
        potential[mask] = np.inf
        return potential

class SquareWell(PotentialModel):
    def __init__(self, epsilon_over_kB=120.0, sigma=3.4):
        super().__init__(epsilon_over_kB, sigma)
        self.name = "Square Well"
        self.well_width = 1.5  # Fixed value
        self.well_depth = 1.0  # Fixed value
        self.description = "Combines hard sphere repulsion with a constant attractive well. Useful for studying phase transitions and as a simple model for colloidal systems."
        self.equation = r"$V(r) = \infty$ for $r < \sigma$, $-\varepsilon$ for $\sigma \leq r < 1.5\sigma$, $0$ for $r \geq 1.5\sigma$"

    def calculate(self, r):
        well_position = self.sigma * self.well_width
        mask_core = r < self.sigma
        mask_well = (r >= self.sigma) & (r < well_position)
        
        potential = np.zeros_like(r)
        potential[mask_core] = np.inf
        potential[mask_well] = -self.epsilon_over_kB * self.well_depth
        return potential

class Sutherland(PotentialModel):
    def __init__(self, epsilon_over_kB=120.0, sigma=3.4):
        super().__init__(epsilon_over_kB, sigma)
        self.name = "Sutherland"
        self.n = 12  # Fixed value
        self.description = "Historical potential with hard-core repulsion and power-law attraction. Used in theoretical studies and as a simplified model for molecular interactions."
        self.equation = r"$V(r) = \infty$ for $r < \sigma$, $-\varepsilon(\sigma/r)^{12}$ for $r \geq \sigma$"

    def calculate(self, r):
        if isinstance(r, np.ndarray):
            mask = r < self.sigma
            potential = -self.epsilon_over_kB * (self.sigma/r)**self.n
            potential[mask] = np.inf
            return potential
        else:
            if r < self.sigma:
                return np.inf
            else:
                return -self.epsilon_over_kB * (self.sigma/r)**self.n