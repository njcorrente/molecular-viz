import numpy as np

def calculate_plot_range(sigma, current_distance):
    """Calculate appropriate plot range based on current parameters"""
    r_min = max(0.8 * sigma, 0.5)
    r_max = max(3.0 * current_distance, 10.0 * sigma)
    return r_min, r_max

def generate_r_values(r_min, r_max, num_points=1000):
    """Generate r values for potential calculation"""
    return np.linspace(r_min, r_max, num_points)

def format_axis_labels(ax):
    """Format plot axis labels"""
    ax.set_xlabel('r (Å)')
    ax.set_ylabel('V(r) (K)')
    ax.grid(True, linestyle='--', alpha=0.7)

def unit_converter():
    """Unit conversion utilities"""
    conversions = {
        'energy': {
            'K_to_kJmol': lambda x: x * 0.008314,
            'K_to_eV': lambda x: x * 8.617e-5,
            'kJmol_to_K': lambda x: x / 0.008314,
            'eV_to_K': lambda x: x / 8.617e-5
        },
        'distance': {
            'A_to_nm': lambda x: x / 10,
            'A_to_pm': lambda x: x * 100,
            'nm_to_A': lambda x: x * 10,
            'pm_to_A': lambda x: x / 100
        }
    }
    return conversions
