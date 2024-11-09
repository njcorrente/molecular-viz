import tkinter as tk
from tkinter import ttk

class ParameterFrame:
    def __init__(self, parent, update_callback):
        self.frame = ttk.LabelFrame(parent, text="Potential Parameters")
        self.frame.pack(pady=10, padx=10, fill="x")
        self.update_callback = update_callback

        # Create parameter entries
        self.create_parameter_entries()

    def create_parameter_entries(self):
        # Epsilon/kB input
        ttk.Label(self.frame, text="ε/kB (K):").grid(row=0, column=0, padx=5, pady=5)
        self.epsilon_over_kB_var = tk.StringVar(value="120.0")
        epsilon_entry = ttk.Entry(self.frame, textvariable=self.epsilon_over_kB_var)
        epsilon_entry.grid(row=0, column=1, padx=5, pady=5)
        epsilon_entry.bind('<Return>', lambda e: self.update_callback())

        # Sigma input
        ttk.Label(self.frame, text="σ (Å):").grid(row=0, column=2, padx=5, pady=5)
        self.sigma_var = tk.StringVar(value="3.4")
        sigma_entry = ttk.Entry(self.frame, textvariable=self.sigma_var)
        sigma_entry.grid(row=0, column=3, padx=5, pady=5)
        sigma_entry.bind('<Return>', lambda e: self.update_callback())

        # Update button
        ttk.Button(self.frame, text="Update Parameters", 
                  command=self.update_callback).grid(row=0, column=4, padx=5, pady=5)

    def get_parameters(self):
        """Get current parameter values"""
        return {
            'epsilon_over_kB': float(self.epsilon_over_kB_var.get()),
            'sigma': float(self.sigma_var.get())
        }
