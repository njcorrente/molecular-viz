import tkinter as tk

class MoleculeCanvas:
    def __init__(self, parent, width, height):
        self.canvas = tk.Canvas(parent, width=width, height=height)
        
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
        """Draw a sphere-like circle with 3D effect"""
        darker = self.adjust_color(base_color, 0.7)
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

        # Main sphere and gradient effects
        self.canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=base_color, outline=darker
        )

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

    def draw_molecules(self, distance, sigma):
        """Draw two molecules with distance indicator"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        scale_factor = canvas_width / 12.0
        center_y = canvas_height / 2
        
        left_x = canvas_width * 0.2
        right_x = left_x + (distance * scale_factor)
        molecule_radius = (sigma * scale_factor) / 2

        self.canvas.delete("all")
        
        # Draw molecules
        self.draw_sphere(left_x, center_y, molecule_radius, '#4169E1')
        self.draw_sphere(right_x, center_y, molecule_radius, '#DC143C')
        
        # Draw distance indicator
        self._draw_distance_indicator(left_x, right_x, center_y, molecule_radius, distance)

    def _draw_distance_indicator(self, left_x, right_x, center_y, molecule_radius, distance):
        """Draw distance line and label"""
        line_offset = molecule_radius + 5
        self.canvas.create_line(
            left_x, center_y + line_offset,
            right_x, center_y + line_offset,
            dash=(4, 2), fill='gray40', width=1.5
        )
        
        mid_x = (left_x + right_x) / 2
        text_y = center_y - molecule_radius - 20
        
        self.canvas.create_rectangle(
            mid_x - 45, text_y - 10,
            mid_x + 45, text_y + 10,
            fill='white', outline='gray80'
        )
        
        self.canvas.create_text(
            mid_x, text_y,
            text=f"r = {distance:.2f} Å",
            font=('Helvetica', 10), fill='black'
        )
