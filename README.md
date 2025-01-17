```markdown
# Molecular Potential Viewer

An interactive visualization tool for exploring molecular interaction potentials. This application provides a graphical interface to visualize and understand different molecular potential models commonly used in physics and chemistry.

![Molecular Potential Viewer Screenshot]

## Features

- Interactive visualization of various molecular potential models:
  - Lennard-Jones Potential
  - Hard Sphere Model
  - Square Well Potential 
  - Sutherland Potential
  - Morse Potential
  - Buckingham Potential
  - Yukawa Potential
  - Mie Potential

- Real-time visualization of:
  - Potential energy curves
  - Molecular distance relationships
  - 3D-style molecule representations

- Adjustable parameters for each potential model:
  - Energy parameter (ε/kB)
  - Distance parameter (σ)
  - Model-specific parameters (e.g., width parameter for Morse potential)

- Interactive features:
  - Distance slider with magnetic snap points
  - Dynamic parameter updates
  - Hover tooltips with model information
  - Real-time plot updates

## Installation
```
1. Clone this repository:
```bash
git clone https://github.com/njcorrente/molecular-viz
cd molecular-viz
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python molecular_viz/main.py
```

```markdown
## Requirements

- Python 3.7+
- NumPy 
- Matplotlib
- Tkinter (usually comes with Python)

## Usage

1. Launch the application using the command above
2. Select a potential model from the dropdown menu
3. Adjust the parameters using the input fields
4. Use the slider to change the distance between molecules
5. Observe the potential energy curve and molecular visualization update in real-time

## Potential Models

The application includes several important molecular potential models:

- **Lennard-Jones**: Common for noble gases and simple molecules
- **Hard Sphere**: Simplest model for rigid sphere interactions 
- **Square Well**: Used for studying phase transitions
- **Sutherland**: Historical model with hard-core repulsion
- **Morse**: Suitable for diatomic molecules
- **Buckingham**: Alternative to Lennard-Jones with exponential repulsion
- **Yukawa**: Used in plasma physics and colloidal systems
- **Mie**: Generalized form of Lennard-Jones with adjustable exponents

## Contributing

Contributions are welcome! Please feel free to submit pull requests, create issues, or suggest new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Authors

- Nick Corrente (@njcorrente)

## Acknowledgments

- Thanks to the scientific community for developing and documenting these molecular potential models
- Built using Python's scientific computing stack (NumPy, Matplotlib)
```