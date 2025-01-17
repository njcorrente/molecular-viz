import tkinter as tk
from tkinter import ttk

class ParameterFrame(ttk.LabelFrame):
    def __init__(self, parent, callback):
        super().__init__(parent, text="Potential Parameters")
        self.callback = callback
        self.create_widgets()

    def create_widgets(self):
        # Epsilon/kB input
        ttk.Label(self, text="ε/kB (K):").grid(row=0, column=0, padx=5, pady=5)
        self.epsilon_var = tk.StringVar(value="120.0")
        epsilon_entry = ttk.Entry(self, textvariable=self.epsilon_var)
        epsilon_entry.grid(row=0, column=1, padx=5, pady=5)
        epsilon_entry.bind('<Return>', lambda e: self.callback())

        # Sigma input
        ttk.Label(self, text="σ (Å):").grid(row=0, column=2, padx=5, pady=5)
        self.sigma_var = tk.StringVar(value="3.4")
        sigma_entry = ttk.Entry(self, textvariable=self.sigma_var)
        sigma_entry.grid(row=0, column=3, padx=5, pady=5)
        sigma_entry.bind('<Return>', lambda e: self.callback())

        # Update button
        ttk.Button(self, text="Update Parameters", 
                  command=self.callback).grid(row=0, column=4, padx=5, pady=5)

class ModelSpecificFrame(ttk.LabelFrame):
    def __init__(self, parent, model_type, callback):
        super().__init__(parent, text="Model-Specific Parameters")
        self.model_type = model_type
        self.callback = callback
        self.create_widgets()

    def create_widgets(self):
        if self.model_type == "Square Well":
            self._create_square_well_widgets()
        elif self.model_type == "Sutherland":
            self._create_sutherland_widgets()

    def _create_square_well_widgets(self):
        # Well Width
        ttk.Label(self, text="Well Width (λ, in σ units):").grid(
            row=0, column=0, padx=5, pady=5)
        self.well_width_var = tk.DoubleVar(value=1.5)
        well_width_slider = ttk.Scale(
            self, from_=1.0, to=3.0,
            orient="horizontal",
            variable=self.well_width_var,
            command=lambda _: self.callback()
        )
        well_width_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Well Depth
        ttk.Label(self, text="Well Depth (in ε units):").grid(
            row=1, column=0, padx=5, pady=5)
        self.well_depth_var = tk.DoubleVar(value=1.0)
        well_depth_slider = ttk.Scale(
            self, from_=0.1, to=2.0,
            orient="horizontal",
            variable=self.well_depth_var,
            command=lambda _: self.callback()
        )
        well_depth_slider.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    def _create_sutherland_widgets(self):
        ttk.Label(self, text="Power (n):").grid(
            row=0, column=0, padx=5, pady=5)
        self.sutherland_n_var = tk.IntVar(value=12)
        sutherland_n_slider = ttk.Scale(
            self, from_=6, to=18,
            orient="horizontal",
            variable=self.sutherland_n_var,
            command=lambda _: self.callback()
        )
        sutherland_n_slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

class InfoTooltip:
    def __init__(self, widget, models):
        self.widget = widget
        self.models = models
        self.tooltip = None
        self.create_tooltip()

    def create_tooltip(self):
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        
        self.text = tk.Text(self.tooltip, wrap="word", width=50, height=10, 
                           relief="solid", borderwidth=1)
        self.text.pack()

        self.widget.bind('<Enter>', self.show_tooltip)
        self.widget.bind('<Leave>', self.hide_tooltip)

    def show_tooltip(self, event):
        model = self.widget.get()  # Assuming widget is a Combobox or similar
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, f"Model: {model}\n\n")
        self.text.insert(tk.END, f"Equation:\n{self.models[model]['equation']}\n\n")
        self.text.insert(tk.END, f"Description:\n{self.models[model]['description']}")
        
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tooltip.geometry(f"+{x}+{y}")
        self.tooltip.deiconify()

    def hide_tooltip(self, event):
        self.tooltip.withdraw()
