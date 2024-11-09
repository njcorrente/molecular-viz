import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PlotFrame:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # Set up matplotlib with LaTeX support
        plt.rcParams.update({
            "text.usetex": False,  
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "mathtext.fontset": "dejavuserif"
        })

        # Create matplotlib figure
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Define plot colors
        self.plot_colors = {
            'Lennard-Jones': '#2E86C1',
            'Hard Sphere': '#28B463',
            'Square Well': '#E67E22',
            'Sutherland': '#8E44AD'
        }

    def configure_plot_style(self):
        """Configure the plot style settings"""
        plt.style.use('seaborn-v0_8-darkgrid')
        
        self.fig.set_facecolor('#f8f9fa')
        self.ax.set_facecolor('#ffffff')
        
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_linewidth(1.5)
        self.ax.spines['bottom'].set_linewidth(1.5)
        
        self.ax.tick_params(axis='both', which='major', labelsize=10, width=1.5, length=6)
        self.ax.tick_params(axis='both', which='minor', width=1, length=4)
        
        self.ax.grid(True, linestyle='--', alpha=0.7, color='gray', linewidth=0.5)

    def update_plot(self, model, r, V, current_distance, current_V, equation):
        """Update the potential plot"""
        self.ax.clear()
        self.configure_plot_style()

        model_color = self.plot_colors[model.name]
        y_max = model.epsilon_over_kB * 10
        y_min = -2 * model.epsilon_over_kB
        # Add horizontal line at V = 0
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)

        # Plot the potential based on model type
        if model.name == 'Square Well':
            well_position = model.sigma * model.well_width
            well_depth = -model.epsilon_over_kB * model.well_depth
            
            # Add high-value line segment for r < sigma
            r_repulsive = r[r < model.sigma]
            if len(r_repulsive) > 0:
                V_repulsive = np.full_like(r_repulsive, y_max)
                self.ax.plot(r_repulsive, V_repulsive, '-', 
                           color=model_color, linewidth=2, alpha=0.5)
                
                # Add vertical connection line from well depth to y_max at r = sigma
                self.ax.plot([model.sigma, model.sigma], [well_depth, y_max], '-',
                           color=model_color, linewidth=2, alpha=0.8)
            
            # Plot well region
            r_well = r[(r >= model.sigma) & (r < well_position)]
            V_well = np.full_like(r_well, well_depth)
            self.ax.plot(r_well, V_well, '-', color=model_color, 
                        linewidth=2.5, alpha=0.8)
            
            # Plot outer region
            r_outer = r[r >= well_position]
            V_outer = np.zeros_like(r_outer)
            self.ax.plot(r_outer, V_outer, '-', color=model_color, 
                        linewidth=2.5, alpha=0.8)
            
            # Add vertical connection at well edge
            self.ax.plot([well_position, well_position], [well_depth, 0], '-',
                        color=model_color, linewidth=2.5, alpha=0.8)

        elif model.name in ['Hard Sphere', 'Sutherland']:
            # Plot the main potential curve
            valid_mask = ~np.isinf(V)
            self.ax.plot(r[valid_mask], V[valid_mask], '-', 
                        color=model_color, linewidth=2.5, alpha=0.8)

            # Add high-value line segment for r < sigma
            r_repulsive = r[r < model.sigma]
            if len(r_repulsive) > 0:
                V_repulsive = np.full_like(r_repulsive, y_max)
                self.ax.plot(r_repulsive, V_repulsive, '-', 
                           color=model_color, linewidth=2, alpha=0.5)

            # Find the value of the potential just after sigma
            r_after_sigma = r[r >= model.sigma][0]
            V_after_sigma = V[r >= model.sigma][0]
            
            # Add vertical connection line
            self.ax.plot([model.sigma, model.sigma], [V_after_sigma, y_max], '-',
                        color=model_color, linewidth=2, alpha=0.8)

        else:  # Lennard-Jones
            self.ax.plot(r, V, '-', color=model_color, linewidth=2.5, alpha=0.8)

        # Plot current point if not in infinite region
        if not np.isinf(current_V):
            self.ax.plot(current_distance, current_V, 'o', 
                        color='#e74c3c', markersize=8, 
                        markeredgecolor='white', markeredgewidth=1.5)

        # Labels and title
        self.ax.set_xlabel('Distance (Å)', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('Potential Energy (ε/kB, K)', fontsize=12, fontweight='bold')
        self.ax.set_title(f'{model.name} Potential', fontsize=14, fontweight='bold', pad=15)

        # Equation display
        bbox_props = dict(boxstyle="round,pad=0.5", fc="#f8f9fa", ec="gray", 
                         alpha=0.9, linewidth=1.5)
        
        # Split equation into multiple lines if needed
        equation_parts = equation.split(', ')
        equation_text = '\n'.join(equation_parts)
        
        self.ax.text(0.98, 0.95, equation_text, 
                    transform=self.ax.transAxes, 
                    fontsize=11,
                    bbox=bbox_props,
                    horizontalalignment='right',
                    verticalalignment='top',
                    math_fontfamily='dejavuserif')

        # Set axis limits
        y_min = -model.epsilon_over_kB * 1.5
        self.ax.set_ylim([y_min, 1000])
        self.ax.set_xlim(0.5*model.sigma, 10.0)

        # Update canvas
        self.canvas.draw()