import tkinter as tk
from tkinter import ttk

class ParameterFrame:
    def __init__(self, parent, update_callback):
        self.frame = ttk.LabelFrame(parent, text="Potential Parameters")
        self.frame.pack(pady=10, padx=10, fill="x")
        self.update_callback = update_callback
        
        # Dictionary to store all parameter variables
        self.param_vars = {}
        
        # Create parameter entries
        self.create_parameter_entries()
        
        # Create additional parameter frames that can be shown/hidden
        self.create_model_specific_parameters()

    def create_parameter_entries(self):
        # Base parameters (always visible)
        ttk.Label(self.frame, text="ε/kB (K):").grid(row=0, column=0, padx=5, pady=5)
        self.param_vars['epsilon_over_kB'] = tk.StringVar(value="120.0")
        epsilon_entry = ttk.Entry(self.frame, textvariable=self.param_vars['epsilon_over_kB'])
        epsilon_entry.grid(row=0, column=1, padx=5, pady=5)
        epsilon_entry.bind('<Return>', lambda e: self.update_callback())

        ttk.Label(self.frame, text="σ (Å):").grid(row=0, column=2, padx=5, pady=5)
        self.param_vars['sigma'] = tk.StringVar(value="3.4")
        sigma_entry = ttk.Entry(self.frame, textvariable=self.param_vars['sigma'])
        sigma_entry.grid(row=0, column=3, padx=5, pady=5)
        sigma_entry.bind('<Return>', lambda e: self.update_callback())

        # Update button
        ttk.Button(self.frame, text="Update Parameters", 
                  command=self.update_callback).grid(row=0, column=4, padx=5, pady=5)

    def create_model_specific_parameters(self):
        # Create frames for model-specific parameters
        self.model_frames = {}
        
        # Morse potential parameters
        morse_frame = ttk.Frame(self.frame)
        ttk.Label(morse_frame, text="a (width):").grid(row=0, column=0, padx=5, pady=5)
        self.param_vars['morse_a'] = tk.StringVar(value="1.0")
        ttk.Entry(morse_frame, textvariable=self.param_vars['morse_a']).grid(row=0, column=1, padx=5, pady=5)
        self.model_frames['Morse'] = morse_frame

        # Buckingham potential parameters
        buckingham_frame = ttk.Frame(self.frame)
        ttk.Label(buckingham_frame, text="A:").grid(row=0, column=0, padx=5, pady=5)
        self.param_vars['buck_A'] = tk.StringVar(value="1000.0")
        ttk.Entry(buckingham_frame, textvariable=self.param_vars['buck_A']).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(buckingham_frame, text="B:").grid(row=0, column=2, padx=5, pady=5)
        self.param_vars['buck_B'] = tk.StringVar(value="2.0")
        ttk.Entry(buckingham_frame, textvariable=self.param_vars['buck_B']).grid(row=0, column=3, padx=5, pady=5)
        self.model_frames['Buckingham'] = buckingham_frame

        # Yukawa potential parameters
        yukawa_frame = ttk.Frame(self.frame)
        ttk.Label(yukawa_frame, text="κ:").grid(row=0, column=0, padx=5, pady=5)
        self.param_vars['yukawa_kappa'] = tk.StringVar(value="1.0")
        ttk.Entry(yukawa_frame, textvariable=self.param_vars['yukawa_kappa']).grid(row=0, column=1, padx=5, pady=5)
        self.model_frames['Yukawa'] = yukawa_frame

        # Mie potential parameters
        mie_frame = ttk.Frame(self.frame)
        ttk.Label(mie_frame, text="n:").grid(row=0, column=0, padx=5, pady=5)
        self.param_vars['mie_n'] = tk.StringVar(value="12")
        ttk.Entry(mie_frame, textvariable=self.param_vars['mie_n']).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(mie_frame, text="m:").grid(row=0, column=2, padx=5, pady=5)
        self.param_vars['mie_m'] = tk.StringVar(value="6")
        ttk.Entry(mie_frame, textvariable=self.param_vars['mie_m']).grid(row=0, column=3, padx=5, pady=5)
        self.model_frames['Mie'] = mie_frame

    def update_visible_parameters(self, model_name):
        # Hide all model-specific frames
        for frame in self.model_frames.values():
            frame.grid_remove()
        
        # Show frame for selected model if it exists
        if model_name in self.model_frames:
            self.model_frames[model_name].grid(row=1, column=0, columnspan=5, padx=5, pady=5)

    def get_parameters(self):
        """Get current parameter values"""
        params = {
            'epsilon_over_kB': float(self.param_vars['epsilon_over_kB'].get()),
            'sigma': float(self.param_vars['sigma'].get())
        }
        
        # Add model-specific parameters
        for key, var in self.param_vars.items():
            if key not in ['epsilon_over_kB', 'sigma']:
                params[key] = float(var.get())
                
        return params