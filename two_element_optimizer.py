import numpy as np
import matplotlib.pyplot as plt

from optiland import optic, optimization

# Create an empty optical system
lens = optic.Optic()

# -------------------------
# Setup initial geometry
# -------------------------
# Surface 0 : Object at infinity
lens.add_surface(index=0, thickness=np.inf)
# First lens element surfaces
# Use finite starting radii so the variables begin within bounds
lens.add_surface(index=1, thickness=7, radius=100.0, is_stop=True, material="N-SF11")
lens.add_surface(index=2, thickness=5, radius=-100.0)
# Second lens element surfaces
# Second lens element surfaces with finite radii
lens.add_surface(index=3, thickness=5, radius=80.0, is_stop=False, material="N-SF11")
lens.add_surface(index=4, thickness=20, radius=-80.0)
# Image plane
lens.add_surface(index=5)

# Aperture stop (Effective pupil diameter = 25 mm)
lens.set_aperture(aperture_type="EPD", value=25)

# Fields in degrees
lens.set_field_type(field_type="angle")
lens.add_field(y=0.0)
lens.add_field(y=0.7)
lens.add_field(y=1.0)

# Wavelengths in microns
lens.add_wavelength(value=0.4861)
lens.add_wavelength(value=0.5876, is_primary=True)
lens.add_wavelength(value=0.6563)

lens.draw()
plt.show()


# Update the paraxial model before optimization
lens.update_paraxial()

# -------------------------
# Construct optimization problem
# -------------------------
problem = optimization.OptimizationProblem()

for wave in lens.wavelengths.get_wavelengths():
    for Hx, Hy in lens.fields.get_field_coords():
        input_data = {
            "optic": lens,
            "Hx": Hx,
            "Hy": Hy,
            "num_rays": 3,
            "wavelength": wave,
            "distribution": "gaussian_quad",
        }
        problem.add_operand(
            operand_type="OPD_difference",
            target=0,
            weight=1,
            input_data=input_data,
        )

# Target a back focal length of 100 mm
problem.add_operand(
    operand_type="f2",
    target=100,
    weight=10,
    input_data={"optic": lens},
)

# -------------------------
# Define optimization variables
# -------------------------
# Separation between the two lenses
problem.add_variable(lens, "thickness", surface_number=2, min_val=0, max_val=1000)
# Radii of the first element
problem.add_variable(lens, "radius", surface_number=1, min_val=-1000, max_val=1000)
problem.add_variable(lens, "radius", surface_number=2, min_val=-1000, max_val=1000)

# Constraint on the first element's center thickness (surface 1 -> 2)
problem.add_variable(lens, "thickness", surface_number=1, min_val=5, max_val=10)
# Constraint on the first element's edge thickness at semi-diameter 12.5 mm
problem.add_variable(
    lens,
    "edge_thickness",
    surface_number=1,
    edge_radius=12.5,
    min_val=3,
    max_val=6,
)

# Display the problem summary
problem.info()

# -------------------------
# Run optimization
# -------------------------
optimizer = optimization.DifferentialEvolution(problem)
res = optimizer.optimize(maxiter=256, disp=False, workers=-1)

# Print final merit function value
print("Optimization completed. Final merit:", problem.rss())

lens.draw()