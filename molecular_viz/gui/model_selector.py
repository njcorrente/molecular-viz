import tkinter as tk
from tkinter import ttk

class ModelSelector:
    def __init__(self, parent, models, on_model_change):
        self.frame = ttk.Frame(parent)
        self.frame.pack(pady=10, padx=10, fill="x")

        # Create model instances with default parameters
        self.model_instances = {
            name: model_class() for name, model_class in models.items()
        }

        # Model selection dropdown (simplified - remove categories)
        ttk.Label(self.frame, text="Interaction Model:").pack(side="left", padx=5)
        self.model_var = tk.StringVar(value="Lennard-Jones")
        
        # Organize models into categories but keep dropdown simple
        model_list = list(models.keys())
        
        self.model_dropdown = ttk.Combobox(
            self.frame, 
            textvariable=self.model_var,
            values=model_list,  # Just use the plain list of models
            state="readonly", 
            width=30
        )
        self.model_dropdown.pack(side="left", padx=5)
        
        # Store callback
        self.on_model_change = on_model_change
        
        # Bind the callback
        self.model_dropdown.bind('<<ComboboxSelected>>', self.on_selection_change)

        # Info button with hover tooltip
        self.info_label = ttk.Label(self.frame, text="ℹ")
        self.info_label.pack(side="left", padx=5)
        
        # Create tooltip for model information
        self.create_tooltip()

    def on_selection_change(self, event):
        model_name = self.model_var.get()
#         print(f"ModelSelector: Selected model: {model_name}")  # Debug print
        self.on_model_change(model_name)

    def create_tooltip(self):
        tooltip = tk.Toplevel(self.frame)
        tooltip.withdraw()
        tooltip.overrideredirect(True)
        
        text = tk.Text(tooltip, wrap="word", width=50, height=10, 
                      relief="solid", borderwidth=1)
        text.pack()

        def show_tooltip(event):
            model_name = self.get_current_model()
            model = self.model_instances[model_name]
            text.delete(1.0, tk.END)
            text.insert(tk.END, f"Model: {model_name}\n\n")
            text.insert(tk.END, f"Equation:\n{model.equation}\n\n")
            text.insert(tk.END, f"Description:\n{model.description}")
            
            x, y, _, _ = self.info_label.bbox("all")
            x = x + self.info_label.winfo_rootx() + 25
            y = y + self.info_label.winfo_rooty() + 25
            tooltip.geometry(f"+{x}+{y}")
            tooltip.deiconify()

        def hide_tooltip(event):
            tooltip.withdraw()

        self.info_label.bind('<Enter>', show_tooltip)
        self.info_label.bind('<Leave>', hide_tooltip)

    def get_current_model(self):
        return self.model_var.get()