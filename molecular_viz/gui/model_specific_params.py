# gui/model_specific_params.py
import tkinter as tk
from tkinter import ttk

class ModelSpecificParams:
    def __init__(self, parent, update_callback):
        self.frame = ttk.LabelFrame(parent, text="Model Information and Parameters")
        self.frame.pack(pady=10, padx=10, fill="x")
        self.update_callback = update_callback
        
        # Create description label
        self.desc_label = ttk.Label(self.frame, text="", wraplength=950)
        self.desc_label.pack(pady=5, padx=5)

        # Create frame for additional parameters
        self.param_frame = ttk.Frame(self.frame)
        self.param_frame.pack(fill="x", pady=5, padx=5)
        
        # Dictionary to store parameter variables
        self.param_vars = {}
        
        # Store current model name
        self.current_model = None

    def create_parameter_widgets(self, model_name):
        # Clear existing parameter widgets
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.param_vars.clear()

        # Create specific parameter inputs based on model
        if model_name == "Morse":
            self.create_parameter("morse_a", "Width parameter (a):", "1.0")
        elif model_name == "Buckingham":
            self.create_parameter("buck_A", "Repulsive strength (A):", "1000.0")
            self.create_parameter("buck_B", "Repulsive range (B):", "2.0")
        elif model_name == "Yukawa":
            self.create_parameter("yukawa_kappa", "Screening length (κ):", "1.0")
        elif model_name == "Mie":
            self.create_parameter("mie_n", "Repulsive exponent (n):", "12")
            self.create_parameter("mie_m", "Attractive exponent (m):", "6")

    def create_parameter(self, name, label, default):
        """Create a labeled entry for a parameter"""
        frame = ttk.Frame(self.param_frame)
        frame.pack(side="left", padx=5)
        
        ttk.Label(frame, text=label).pack(side="left", padx=2)
        var = tk.StringVar(value=default)
        entry = ttk.Entry(frame, textvariable=var, width=10)
        entry.pack(side="left")
        entry.bind('<Return>', lambda e: self.update_callback())
        
        self.param_vars[name] = var

    def update_for_model(self, model_name, description):
        """Update the display for a new model"""
        self.current_model = model_name
        self.desc_label.config(text=description)
        self.create_parameter_widgets(model_name)

    def get_parameters(self):
        """Get current model-specific parameters"""
        params = {}
        for name, var in self.param_vars.items():
            try:
                params[name] = float(var.get())
            except ValueError:
                # If conversion fails, use default values
                defaults = {
                    "morse_a": 1.0,
                    "buck_A": 1000.0,
                    "buck_B": 2.0,
                    "yukawa_kappa": 1.0,
                    "mie_n": 12,
                    "mie_m": 6
                }
                params[name] = defaults[name]
        return params