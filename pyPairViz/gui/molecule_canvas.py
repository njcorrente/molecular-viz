import tkinter as tk

class MoleculeCanvas:
    def __init__(self, parent, height=200):
        self.canvas = tk.Canvas(parent, height=height)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=5)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
    def rgb_to_hex(self, rgb):
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
        
    def adjust_color(self, hex_color, factor):
        r, g, b = self.hex_to_rgb(hex_color)
        new_r = min(255, int(r * factor))
        new_g = min(255, int(g * factor))
        new_b = min(255, int(b * factor))
        return self.rgb_to_hex((new_r, new_g, new_b))

    def draw_sphere(self, x, y, radius, base_color):
        """Helper function to draw a sphere-like circle with improved 3D effect"""
        # Create darker shade for shadow
        darker = self.adjust_color(base_color, 0.7)
        # Create lighter shade for highlight
        lighter = self.adjust_color(base_color, 1.3)

        # Draw shadow
        shadow_offset = radius * 0.1
        self.canvas.create_oval(
            x - radius + shadow_offset,
            y - radius + shadow_offset,
            x + radius + shadow_offset,
            y + radius + shadow_offset,
            fill='gray20', outline=''
        )

        # Main sphere
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=base_color, outline=darker
        )

        # Create gradient effect for 3D appearance
        for i in range(5):
            factor = 0.8 - (i * 0.15)
            inner_radius = radius * factor
            offset = radius * (1 - factor) * 0.5
            self.canvas.create_oval(
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
        self.canvas.create_oval(
            x - highlight_radius - highlight_offset,
            y - highlight_radius - highlight_offset,
            x + highlight_radius - highlight_offset,
            y + highlight_radius - highlight_offset,
            fill='white', outline='white',
            stipple='gray25'
        )

        # Draw center point (small dot)
        dot_radius = 2
        self.canvas.create_oval(
            x - dot_radius, y - dot_radius,
            x + dot_radius, y + dot_radius,
            fill='black', outline='black'
        )

    def update_visualization(self, current_distance, sigma):
        """Update the molecule visualization"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        self.canvas.delete("all")

        # Calculate margins and usable space
        margin = 40
        usable_width = canvas_width - 2 * margin
        usable_height = canvas_height - 2 * margin

        # Calculate scale factors
        max_distance = 10.0  # Maximum distance in Angstroms
        distance_scale = (usable_width * 0.6) / max_distance

        # Calculate molecule radius in canvas units
        molecule_radius = sigma * distance_scale / 2

        # Ensure radius isn't too large for the canvas height
        max_allowed_radius = usable_height / 4
        if molecule_radius > max_allowed_radius:
            scale_factor = max_allowed_radius / molecule_radius
            molecule_radius = max_allowed_radius
            distance_scale *= scale_factor

        # Calculate positions
        center_y = canvas_height / 2
        left_x = margin + usable_width * 0.2
        right_x = left_x + (current_distance * distance_scale)

        # Draw molecules (which will now appear on top of the line)
        self.draw_sphere(left_x, center_y, molecule_radius, '#4169E1')  # Left molecule
        self.draw_sphere(right_x, center_y, molecule_radius, '#DC143C')  # Right molecule
        
        
        # Draw the dashed line after spheres (so it appears on top)
        self.canvas.create_line(
            left_x, center_y,
            right_x, center_y,
            dash=(4, 2), fill='gray40', width=1.5
        )
        
        # Display distance value
        mid_x = (left_x + right_x) / 2
        text_y = center_y - molecule_radius - 20
        
        # Background for text
        self.canvas.create_rectangle(
            mid_x - 45, text_y - 10,
            mid_x + 45, text_y + 10,
            fill='white', outline='gray80'
        )
        
        # Distance text
        self.canvas.create_text(
            mid_x, text_y,
            text=f"r = {current_distance:.2f} Å",
            font=('Helvetica', 10), fill='black'
        )