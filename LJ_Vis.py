import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from functools import partial

class PotentialVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Molecular Interaction Potential Visualizer")
        self.geometry("1000x800")

        # Default parameters
        self.epsilon_over_kB = 120.0  # K
        self.sigma = 3.4  # Angstrom
        self.current_distance = 4.0  # Angstrom
        
        # Additional parameters for other potentials
        self.well_width = 1.5  # for square well (in units of σ)
        self.well_depth = 1.0  # for square well (in units of ε)
        self.sutherland_n = 12  # Sutherland potential power

        # Define potential models with their descriptions
        self.potential_models = {
            "Lennard-Jones": {
                "description": "Most commonly used for noble gases and simple molecules. Combines short-range repulsion (r⁻¹²) with longer-range attraction (r⁻⁶). The r⁻⁶ term represents van der Waals forces.",
                "equation": "V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]",
                "function": self.lennard_jones
            },
            "Hard Sphere": {
                "description": "Simplest model where particles act as perfect rigid spheres. Used for studying entropy-driven phenomena and as a reference system for more complex fluids.",
                "equation": "V(r) = ∞ for r < σ, 0 for r ≥ σ",
                "function": self.hard_sphere
            },
            "Square Well": {
                "description": "Combines hard sphere repulsion with a constant attractive well. Useful for studying phase transitions and as a simple model for colloidal systems.",
                "equation": "V(r) = ∞ for r < σ, -ε for σ ≤ r < λσ, 0 for r ≥ λσ",
                "function": self.square_well
            },
            "Sutherland": {
                "description": "Historical potential with hard-core repulsion and power-law attraction. Used in theoretical studies and as a simplified model for molecular interactions.",
                "equation": "V(r) = ∞ for r < σ, -ε(σ/r)ⁿ for r ≥ σ",
                "function": self.sutherland
            }
        }
        
        self.create_widgets()
        self.update_plot()

    def create_widgets(self):
        # Top frame for model selection and info
        top_frame = ttk.Frame(self)
        top_frame.pack(pady=10, padx=10, fill="x")

        # Model selection dropdown
        ttk.Label(top_frame, text="Interaction Model:").pack(side="left", padx=5)
        self.model_var = tk.StringVar(value="Lennard-Jones")
        model_dropdown = ttk.Combobox(top_frame, textvariable=self.model_var, 
                                    values=list(self.potential_models.keys()),
                                    state="readonly", width=30)
        model_dropdown.pack(side="left", padx=5)
        model_dropdown.bind('<<ComboboxSelected>>', self.on_model_change)

        # Info button with hover tooltip
        self.info_label = ttk.Label(top_frame, text="ℹ")
        self.info_label.pack(side="left", padx=5)
        self.create_tooltip(self.info_label)

        # Parameter input frame
        param_frame = ttk.LabelFrame(self, text="Potential Parameters")
        param_frame.pack(pady=10, padx=10, fill="x")

        # Epsilon/kB input
        ttk.Label(param_frame, text="ε/kB (K):").grid(row=0, column=0, padx=5, pady=5)
        self.epsilon_var = tk.StringVar(value="120.0")
        epsilon_entry = ttk.Entry(param_frame, textvariable=self.epsilon_var)
        epsilon_entry.grid(row=0, column=1, padx=5, pady=5)
        epsilon_entry.bind('<Return>', lambda e: self.update_parameters())

        # Sigma input
        ttk.Label(param_frame, text="σ (Å):").grid(row=0, column=2, padx=5, pady=5)
        self.sigma_var = tk.StringVar(value="3.4")
        sigma_entry = ttk.Entry(param_frame, textvariable=self.sigma_var)
        sigma_entry.grid(row=0, column=3, padx=5, pady=5)
        sigma_entry.bind('<Return>', lambda e: self.update_parameters())

        # Update button
        ttk.Button(param_frame, text="Update Parameters", 
                  command=self.update_parameters).grid(row=0, column=4, padx=5, pady=5)

        # Create main paned window for resizable sections
        main_paned = ttk.PanedWindow(self, orient=tk.VERTICAL)
        main_paned.pack(pady=10, padx=10, fill="both", expand=True)

        # Upper pane for molecule visualization
        upper_frame = ttk.Frame(main_paned)
        main_paned.add(upper_frame, weight=1)

        # Molecule distance slider frame
        slider_frame = ttk.LabelFrame(upper_frame, text="Molecule Distance Control")
        slider_frame.pack(fill="both", expand=True)

        # Canvas for molecule visualization
        self.molecule_canvas = tk.Canvas(slider_frame, height=200)
        self.molecule_canvas.pack(fill="both", expand=True, padx=10, pady=5)

        # Distance slider
        self.distance_var = tk.DoubleVar(value=4.0)
        self.distance_slider = ttk.Scale(
            slider_frame, 
            from_=2.0, 
            to=10.0,
            orient="horizontal",
            variable=self.distance_var,
            command=self.on_slider_change
        )
        self.distance_slider.pack(fill="x", padx=10, pady=5)

        # Lower pane for plot
        lower_frame = ttk.Frame(main_paned)
        main_paned.add(lower_frame, weight=2)

        # Plot frame
        plot_frame = ttk.Frame(lower_frame)
        plot_frame.pack(fill="both", expand=True)

        # Create matplotlib figure
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Description frame
        self.desc_frame = ttk.LabelFrame(self, text="Model Description")
        self.desc_frame.pack(pady=10, padx=10, fill="x")
        self.desc_label = ttk.Label(self.desc_frame, text="", wraplength=950)
        self.desc_label.pack(pady=5, padx=5)
        
        self.create_model_specific_controls()

    def create_tooltip(self, widget):
        tooltip = tk.Toplevel(self)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        
        text = tk.Text(tooltip, wrap="word", width=50, height=10, 
                      relief="solid", borderwidth=1)
        text.pack()

        def show_tooltip(event):
            model = self.model_var.get()
            text.delete(1.0, tk.END)
            text.insert(tk.END, f"Model: {model}\n\n")
            text.insert(tk.END, f"Equation:\n{self.potential_models[model]['equation']}\n\n")
            text.insert(tk.END, f"Description:\n{self.potential_models[model]['description']}")
            
            x, y, _, _ = widget.bbox("all")
            x = x + widget.winfo_rootx() + 25
            y = y + widget.winfo_rooty() + 25
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def on_model_change(self, event):
        model = self.model_var.get()
        self.desc_label.config(text=self.potential_models[model]['description'])
        self.create_model_specific_controls()
        self.update_plot()
        self.draw_molecules()

    def create_model_specific_controls(self):
        """Create a frame for model-specific parameters"""
        if hasattr(self, 'model_params_frame'):
            self.model_params_frame.destroy()
            
        self.model_params_frame = ttk.LabelFrame(self, text="Model-Specific Parameters")
        self.model_params_frame.pack(after=self.desc_frame, pady=10, padx=10, fill="x")
        
        model = self.model_var.get()
        
        if model == "Square Well":
            ttk.Label(self.model_params_frame, text="Well Width (λ, in σ units):").grid(
                row=0, column=0, padx=5, pady=5)
            self.well_width_var = tk.DoubleVar(value=self.well_width)
            well_width_slider = ttk.Scale(
                self.model_params_frame,
                from_=1.0,
                to=3.0,
                orient="horizontal",
                variable=self.well_width_var,
                command=self.on_model_param_change
            )
            well_width_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            ttk.Label(self.model_params_frame, text=f"{self.well_width:.1f}").grid(
                row=0, column=2, padx=5, pady=5)
            
            ttk.Label(self.model_params_frame, text="Well Depth (in ε units):").grid(
                row=1, column=0, padx=5, pady=5)
            self.well_depth_var = tk.DoubleVar(value=self.well_depth)
            well_depth_slider = ttk.Scale(
                self.model_params_frame,
                from_=0.1,
                to=2.0,
                orient="horizontal",
                variable=self.well_depth_var,
                command=self.on_model_param_change
            )
            well_depth_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
            ttk.Label(self.model_params_frame, text=f"{self.well_depth:.1f}").grid(
                row=1, column=2, padx=5, pady=5)
            
        elif model == "Sutherland":
            ttk.Label(self.model_params_frame, text="Power (n):").grid(
                row=0, column=0, padx=5, pady=5)
            self.sutherland_n_var = tk.IntVar(value=self.sutherland_n)
            sutherland_n_slider = ttk.Scale(
                self.model_params_frame,
                from_=6,
                to=18,
                orient="horizontal",
                variable=self.sutherland_n_var,
                command=self.on_model_param_change
            )
            sutherland_n_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
            ttk.Label(self.model_params_frame, text=f"{self.sutherland_n}").grid(
                row=0, column=2, padx=5, pady=5)
        
        self.model_params_frame.grid_columnconfigure(1, weight=1)

    def on_model_param_change(self, event):
        """Handle changes to model-specific parameters"""
        model = self.model_var.get()
        
        if model == "Square Well":
            self.well_width = self.well_width_var.get()
            self.well_depth = self.well_depth_var.get()
            self.model_params_frame.winfo_children()[2].config(text=f"{self.well_width:.1f}")
            self.model_params_frame.winfo_children()[5].config(text=f"{self.well_depth:.1f}")
            
        elif model == "Sutherland":
            self.sutherland_n = self.sutherland_n_var.get()
            self.model_params_frame.winfo_children()[2].config(text=f"{self.sutherland_n}")
        
        self.update_plot()

    def draw_molecules(self):
        """Draw the molecules on the canvas with 3D sphere-like appearance."""
        canvas_width = self.molecule_canvas.winfo_width()
        canvas_height = self.molecule_canvas.winfo_height()

        self.molecule_canvas.delete("all")

        scale_factor = canvas_width / 12.0
        center_y = canvas_height / 2
        
        left_x = canvas_width * 0.2
        right_x = left_x + (self.current_distance * scale_factor)
        molecule_radius = (self.sigma * scale_factor) / 2

        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
        def rgb_to_hex(rgb):
            return '#{:02x}{:02x}{:02x}'.format(*rgb)
            
        def adjust_color(hex_color, factor):
            r, g, b = hex_to_rgb(hex_color)
            new_r = min(255, int(r * factor))
            new_g = min(255, int(g * factor))
            new_b = min(255, int(b * factor))
            return rgb_to_hex((new_r, new_g, new_b))

        def draw_sphere(x, y, radius, base_color):
            """Helper function to draw a sphere-like circle with improved 3D effect"""
            # Create darker shade for shadow
            darker = adjust_color(base_color, 0.7)
            # Create lighter shade for highlight
            lighter = adjust_color(base_color, 1.3)

            # Draw shadow
            shadow_offset = radius * 0.1
            self.molecule_canvas.create_oval(
                x - radius + shadow_offset,
                y - radius + shadow_offset,
                x + radius + shadow_offset,
                y + radius + shadow_offset,
                fill='gray20', outline=''
            )

            # Main sphere
            self.molecule_canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill=base_color, outline=darker
            )

        # Create gradient effect for 3D appearance
            for i in range(5):
                factor = 0.8 - (i * 0.15)
                inner_radius = radius * factor
                offset = radius * (1 - factor) * 0.5
                self.molecule_canvas.create_oval(
                    x - inner_radius - offset,
                    y - inner_radius - offset,
                    x + inner_radius - offset,
                    y + inner_radius - offset,
                    fill=lighter if i == 0 else '',
                    outline=lighter,
                    stipple='gray50'
                )

            # Add highlight
            highlight_radius = radius * 0.2
            highlight_offset = radius * 0.3
            self.molecule_canvas.create_oval(
                x - highlight_radius - highlight_offset,
                y - highlight_radius - highlight_offset,
                x + highlight_radius - highlight_offset,
                y + highlight_radius - highlight_offset,
                fill='white', outline='white',
                stipple='gray25'
            )

        # Draw molecules with enhanced 3D appearance
        draw_sphere(left_x, center_y, molecule_radius, '#4169E1')  # Left molecule
        draw_sphere(right_x, center_y, molecule_radius, '#DC143C')  # Right molecule

        # Draw distance line below the spheres
        line_offset = molecule_radius + 5
        self.molecule_canvas.create_line(
            left_x, center_y + line_offset,
            right_x, center_y + line_offset,
            dash=(4, 2), fill='gray40', width=1.5
        )
        
        # Display distance value with enhanced styling
        mid_x = (left_x + right_x) / 2
        text_y = center_y - molecule_radius - 20  # Position text above molecules
        
        # Background for text
        self.molecule_canvas.create_rectangle(
            mid_x - 45, text_y - 10,
            mid_x + 45, text_y + 10,
            fill='white', outline='gray80'
        )
        
        # Distance text
        self.molecule_canvas.create_text(
            mid_x, text_y,
            text=f"r = {self.current_distance:.2f} Å",
            font=('Helvetica', 10), fill='black'
        )

    def lennard_jones(self, r):
        """Lennard-Jones potential in units of epsilon/kB (K)."""
        return 4 * self.epsilon_over_kB * ((self.sigma/r)**12 - (self.sigma/r)**6)

    def hard_sphere(self, r):
        """Hard sphere potential in units of epsilon/kB (K)."""
        mask = r < self.sigma
        potential = np.zeros_like(r)
        potential[mask] = np.inf
        return potential

    def square_well(self, r):
        """Square well potential in units of epsilon/kB (K)."""
        well_position = self.sigma * self.well_width
        mask_core = r < self.sigma
        mask_well = (r >= self.sigma) & (r < well_position)
        
        potential = np.zeros_like(r)
        potential[mask_core] = np.inf
        potential[mask_well] = -self.epsilon_over_kB * self.well_depth
        return potential

    def sutherland(self, r):
        """Sutherland potential in units of epsilon/kB (K)."""
        if isinstance(r, np.ndarray):
            mask = r < self.sigma
            potential = -self.epsilon_over_kB * (self.sigma/r)**self.sutherland_n
            potential[mask] = np.inf
            return potential
        else:
            if r < self.sigma:
                return np.inf
            else:
                return -self.epsilon_over_kB * (self.sigma/r)**self.sutherland_n

    def update_parameters(self):
        try:
            self.epsilon_over_kB = float(self.epsilon_var.get())
            self.sigma = float(self.sigma_var.get())
            self.update_plot()
            self.draw_molecules()
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numbers for parameters")

    def on_slider_change(self, event):
        self.current_distance = self.distance_var.get()
        self.update_plot()
        self.draw_molecules()

    def configure_plot_style(self):
        """Configure the plot style settings"""
        # Set the style
        plt.style.use('seaborn-v0_8-darkgrid')
        
        # Configure figure and axes appearance
        self.fig.set_facecolor('#f8f9fa')
        self.ax.set_facecolor('#ffffff')
        
        # Custom color scheme
        self.plot_colors = {
            'Lennard-Jones': '#2E86C1',
            'Hard Sphere': '#28B463',
            'Square Well': '#E67E22',
            'Sutherland': '#8E44AD'
        }
        
        # Spine and grid styling
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_linewidth(1.5)
        self.ax.spines['bottom'].set_linewidth(1.5)
        
        # Tick styling
        self.ax.tick_params(axis='both', which='major', labelsize=10, width=1.5, length=6)
        self.ax.tick_params(axis='both', which='minor', width=1, length=4)
        
        # Grid styling
        self.ax.grid(True, linestyle='--', alpha=0.7, color='gray', linewidth=0.5)

    def update_plot(self):
        """Update the potential plot."""
        self.ax.clear()
        
        # Apply style configuration
        self.configure_plot_style()
        
        # Generate points for the plot - extend range to show repulsive region
        r = np.linspace(0.5*self.sigma, 10.0, 1000)
        V = self.potential_models[self.model_var.get()]['function'](r)
        model = self.model_var.get()
        
        # Add bold zero line with better styling
        self.ax.axhline(y=0, color='gray', linewidth=1.5, linestyle='-', alpha=0.5)
        
        # Dictionary of equation strings with LaTeX formatting
        equations = {
            "Lennard-Jones": r"$V(r) = 4\epsilon\left[\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6\right]$",
            "Hard Sphere": r"$V(r) = \infty \,(r < \sigma), \,\, 0\,(r \geq \sigma)$",
            "Square Well": r"$V(r) = \infty \,(r < \sigma), \,\, -\epsilon\,(\sigma \leq r < \lambda\sigma), \,\, 0\,(r \geq \lambda\sigma)$",
            "Sutherland": r"$V(r) = \infty \,(r < \sigma), \,\, -\epsilon(\sigma/r)^n\,(r \geq \sigma)$"
        }
        
        if model == "Hard Sphere":
            # Add repulsive region
            r_repulsive = r[r < self.sigma]
            V_repulsive = np.full_like(r_repulsive, self.epsilon_over_kB * 10)
            self.ax.plot(r_repulsive, V_repulsive, '--', color='#e74c3c', 
                        linewidth=2, alpha=0.5)
            
            self.ax.axvline(x=self.sigma, color='#e74c3c', linestyle='--', 
                          label='V = ∞', linewidth=2, alpha=0.7)
            r_plot = r[r >= self.sigma]
            V_plot = np.zeros_like(r_plot)
            self.ax.plot(r_plot, V_plot, '-', color=self.plot_colors[model], 
                        linewidth=2.5, alpha=0.8)
            
        elif model == "Square Well":
            # Add repulsive region
            r_repulsive = r[r < self.sigma]
            V_repulsive = np.full_like(r_repulsive, self.epsilon_over_kB * 10)
            self.ax.plot(r_repulsive, V_repulsive, '--', color='#e74c3c', 
                        linewidth=2, alpha=0.5)
            
            self.ax.axvline(x=self.sigma, color='#e74c3c', linestyle='--', 
                          label='V = ∞', linewidth=2, alpha=0.7)
            
            well_position = self.sigma * self.well_width
            r_well = r[(r >= self.sigma) & (r < well_position)]
            V_well = np.full_like(r_well, -self.epsilon_over_kB * self.well_depth)
            r_outer = r[r >= well_position]
            V_outer = np.zeros_like(r_outer)
            
            self.ax.plot(r_well, V_well, '-', color=self.plot_colors[model], 
                        linewidth=2.5, alpha=0.8)
            self.ax.plot(r_outer, V_outer, '-', color=self.plot_colors[model], 
                        linewidth=2.5, alpha=0.8)
            self.ax.plot([well_position, well_position], 
                        [-self.epsilon_over_kB * self.well_depth, 0], 
                        '-', color=self.plot_colors[model], linewidth=2.5, alpha=0.8)
            
        elif model == "Sutherland":
            # Add repulsive region
            r_repulsive = r[r < self.sigma]
            V_repulsive = np.full_like(r_repulsive, self.epsilon_over_kB * 10)
            self.ax.plot(r_repulsive, V_repulsive, '--', color='#e74c3c', 
                        linewidth=2, alpha=0.5)
            
            self.ax.axvline(x=self.sigma, color='#e74c3c', linestyle='--', 
                          label='V = ∞', linewidth=2, alpha=0.7)
            
            r_plot = r[r >= self.sigma]
            V_plot = -self.epsilon_over_kB * (self.sigma/r_plot)**self.sutherland_n
            self.ax.plot(r_plot, V_plot, '-', color=self.plot_colors[model], 
                        linewidth=2.5, alpha=0.8)
            equations["Sutherland"] = equations["Sutherland"].replace("^n", f"^{{{self.sutherland_n}}}")
            
        else:  # Lennard-Jones
            # For Lennard-Jones, we can plot all points but limit the y-axis
            self.ax.plot(r, V, '-', color=self.plot_colors[model], 
                        linewidth=2.5, alpha=0.8)
        
        # Plot current point if not in infinite region
        current_V = self.potential_models[model]['function'](self.current_distance)
        if not np.isinf(current_V) and current_V < self.epsilon_over_kB * 10:
            self.ax.plot(self.current_distance, current_V, 'o', 
                        color='#e74c3c', markersize=8, 
                        markeredgecolor='white', markeredgewidth=1.5)
        
        # Enhanced labels and title
        self.ax.set_xlabel('Distance (Å)', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('Potential Energy (ε/kB, K)', fontsize=12, fontweight='bold')
        self.ax.set_title(f'{model} Potential', fontsize=14, fontweight='bold', pad=15)
        
        # Enhanced equation display
        bbox_props = dict(boxstyle="round,pad=0.5", fc="#f8f9fa", ec="gray", 
                         alpha=0.9, linewidth=1.5)
        self.ax.text(0.98, 0.95, equations[model], 
                    transform=self.ax.transAxes, 
                    fontsize=11,
                    bbox=bbox_props,
                    horizontalalignment='right',
                    verticalalignment='top')
        
        # Set y-axis limits to show repulsion but prevent extreme values
        if model == "Hard Sphere":
            self.ax.set_ylim(-0.5*self.epsilon_over_kB, self.epsilon_over_kB * 10)
        elif model == "Square Well":
            self.ax.set_ylim(-1.5*self.epsilon_over_kB * self.well_depth, 
                            self.epsilon_over_kB * 10)
        else:
            self.ax.set_ylim(-2*self.epsilon_over_kB, self.epsilon_over_kB * 10)
        
        # Set x-axis limits to show the full range including repulsive region
        self.ax.set_xlim(0.5*self.sigma, 10.0)
        
        # Add grid behind the plot
        self.ax.grid(True, linestyle='--', alpha=0.7)
        
        # Enhanced legend
        if model in ["Hard Sphere", "Square Well", "Sutherland"]:
            self.ax.legend(fontsize=10, framealpha=0.9, loc='upper right')
        
        # Adjust layout and draw
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = PotentialVisualizer()
    app.mainloop()