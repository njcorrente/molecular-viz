import tkinter as tk
from tkinter import ttk

class ModelSpecificParams:
    def __init__(self, parent, update_callback):
        self.frame = ttk.LabelFrame(parent, text="Model Information")
        self.frame.pack(pady=10, padx=10, fill="x")
        self.update_callback = update_callback
        
        # Create description label
        self.desc_label = ttk.Label(self.frame, text="", wraplength=950)
        self.desc_label.pack(pady=5, padx=5)

    def update_for_model(self, model_name, description):
        # Update the description text
        self.desc_label.config(text=description)

    def get_parameters(self):
        """Get current model-specific parameters"""
        return {}  # No additional parameters needed