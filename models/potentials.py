import numpy as np

class PotentialModel:
    def __init__(self, epsilon_over_kB=120.0, sigma=3.4):
        self.epsilon_over_kB = epsilon_over_kB
        self.sigma = sigma
        
    def lennard_jones(self, r):
        """Lennard-Jones potential in units of epsilon/kB (K)."""
        return 4 * self.epsilon_over_kB * ((self.sigma/r)**12 - (self.sigma/r)**6)

    def hard_sphere(self, r):
        """Hard sphere potential in units of epsilon/kB (K)."""
        mask = r < self.sigma
        potential = np.zeros_like(r)
        potential[mask] = np.inf
        return potential

    def square_well(self, r, well_width=1.5, well_depth=1.0):
        """Square well potential in units of epsilon/kB (K)."""
        well_position = self.sigma * well_width
        mask_core = r < self.sigma
        mask_well = (r >= self.sigma) & (r < well_position)
        
        potential = np.zeros_like(r)
        potential[mask_core] = np.inf
        potential[mask_well] = -self.epsilon_over_kB * well_depth
        return potential

    def sutherland(self, r, n=12):
        """Sutherland potential in units of epsilon/kB (K)."""
        if isinstance(r, np.ndarray):
            mask = r < self.sigma
            potential = -self.epsilon_over_kB * (self.sigma/r)**n
            potential[mask] = np.inf
            return potential
        else:
            if r < self.sigma:
                return np.inf
            else:
                return -self.epsilon_over_kB * (self.sigma/r)**n

POTENTIAL_MODELS = {
    "Lennard-Jones": {
        "description": "Most commonly used for noble gases and simple molecules. Combines short-range repulsion (r−12) with longer-range attraction (r−6).",
        "equation": "V(r) = 4ε[(σ/r)12 - (σ/r)6]"
    },
    "Hard Sphere": {
        "description": "Simplest model where particles act as perfect rigid spheres.",
        "equation": "V(r) = ∞ for r < σ, 0 for r ≥ σ"
    },
    "Square Well": {
        "description": "Combines hard sphere repulsion with a constant attractive well.",
        "equation": "V(r) = ∞ for r < σ, -ε for σ ≤ r < λσ, 0 for r ≥ λσ"
    },
    "Sutherland": {
        "description": "Historical potential with hard-core repulsion and power-law attraction.",
        "equation": "V(r) = ∞ for r < σ, -ε(σ/r)n for r ≥ σ"
    }
}
