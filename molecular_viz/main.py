import tkinter as tk
from tkinter import ttk
import numpy as np

from models.potential_models import LennardJones, HardSphere, SquareWell, Sutherland
from gui.molecule_canvas import MoleculeCanvas
from gui.plot_frame import PlotFrame
from gui.parameter_frame import ParameterFrame
from gui.model_selector import ModelSelector
from gui.model_specific_params import ModelSpecificParams

class PotentialVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Molecular Interaction Potential Visualizer")
        self.geometry("1000x800")

        # Initialize models dictionary
        self.models = {
            "Lennard-Jones": LennardJones,
            "Hard Sphere": HardSphere,
            "Square Well": SquareWell,
            "Sutherland": Sutherland
        }

        # Initialize current model
        self.current_model = LennardJones()
        self.current_distance = 10.0

        self.create_widgets()
        self.update_visualization()

    def create_widgets(self):
        # Create model selector
        self.model_selector = ModelSelector(self, self.models, self.on_model_change)

        # Create parameter frame
        self.param_frame = ParameterFrame(self, self.update_parameters)

        # Create model-specific parameters frame (now just shows description)
        self.model_specific_params = ModelSpecificParams(self, self.update_parameters)

        # Create molecule visualization
        self.molecule_canvas = MoleculeCanvas(self)

        # Distance slider
        slider_frame = ttk.LabelFrame(self, text="Molecule Distance Control")
        slider_frame.pack(fill="x", padx=10, pady=5)

        self.distance_var = tk.DoubleVar(value=self.current_distance)
        self.distance_slider = ttk.Scale(
            slider_frame, 
            from_=0.5,
            to=10.0,
            orient="horizontal",
            variable=self.distance_var,
            command=lambda v: self.after_idle(lambda: self.on_slider_change(v))
        )
        self.distance_slider.pack(fill="x", padx=10, pady=5)

        # Create plot frame
        self.plot_frame = PlotFrame(self)
        self.model_specific_params.update_for_model("Lennard-Jones", self.current_model.description)

    def on_model_change(self, model_name):
        # Get model instance for description
        model_instance = self.models[model_name]()
        
        # Update model description
        self.model_specific_params.update_for_model(model_name, model_instance.description)
        
        # Update current model
        self.update_parameters()

    def update_parameters(self):
        # Get current model name
        model_name = self.model_selector.get_current_model()
        
        # Get basic parameters
        params = self.param_frame.get_parameters()
        
        # Create new model instance
        model_class = self.models[model_name]
        self.current_model = model_class(
            epsilon_over_kB=params['epsilon_over_kB'],
            sigma=params['sigma']
        )
        
        # Update visualization
        self.update_visualization()

    def on_slider_change(self, value):
        """Handle slider value changes with detents at r = sigma and potential minimum (LJ only)"""
        try:
            value = float(value)
            sigma = self.current_model.sigma
            detent_width = 0.05  # Width of the "magnetic" range
            
            # If we're close to sigma, snap to it
            if abs(value - sigma) < detent_width:
                self.current_distance = sigma
                self.distance_var.set(sigma)
            # If Lennard-Jones, add detent at potential minimum
            elif isinstance(self.current_model, LennardJones):
                r_min = 2.0**(1.0/6.0) * sigma  # Position of potential minimum for LJ
                if abs(value - r_min) < detent_width:
                    self.current_distance = r_min
                    self.distance_var.set(r_min)
                else:
                    self.current_distance = value
            else:
                self.current_distance = value
                
            self.update_visualization()
            
        except tk.TclError:
            pass  # Ignore any Tcl errors during slider updates

    def update_visualization(self):
        # Update molecule visualization
        self.molecule_canvas.update_visualization(
            self.current_distance,
            self.current_model.sigma
        )

        # Generate points for the plot
        r = np.linspace(0.5*self.current_model.sigma, 10.0, 1000)
        V = self.current_model.calculate(r)
        current_V = self.current_model.calculate(self.current_distance)

        # Update plot
        self.plot_frame.update_plot(
            self.current_model,
            r,
            V,
            self.current_distance,
            current_V,
            self.current_model.equation
        )

if __name__ == "__main__":
    app = PotentialVisualizer()
    app.mainloop()