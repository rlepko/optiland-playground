import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from optiland import optic, optimization

# Create a simple two-element lens system
lens = optic.Optic()

# Object at infinity
lens.add_surface(index=0, thickness=np.inf)
# First element
lens.add_surface(index=1, thickness=7, radius=100.0, is_stop=True, material="N-SF11")
lens.add_surface(index=2, thickness=5, radius=-100.0)
# Second element
lens.add_surface(index=3, thickness=5, radius=80.0, is_stop=True, material="N-SF11")
lens.add_surface(index=4, thickness=20, radius=-80.0)
# Image plane
lens.add_surface(index=5)

# Aperture stop
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

lens.update_paraxial()

# Draw starting layout
fig = lens.draw()
plt.savefig("ipopt_before.png")
plt.close(fig)

# Construct optimization problem
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

# Optimization variables
problem.add_variable(lens, "thickness", surface_number=2, min_val=0, max_val=1000)
problem.add_variable(lens, "radius", surface_number=1, min_val=-1000, max_val=1000)
problem.add_variable(lens, "radius", surface_number=2, min_val=-1000, max_val=1000)
problem.add_variable(lens, "thickness", surface_number=1, min_val=5, max_val=10)
problem.add_variable(
    lens,
    "edge_thickness",
    surface_number=1,
    edge_radius=12.5,
    min_val=3,
    max_val=6,
)

# Run IPOPT optimizer (requires cyipopt and the IPOPT library)
optimizer = optimization.IpoptOptimizer(problem)
result = optimizer.optimize(maxiter=256, disp=False)
print("Optimization completed. Final merit:", problem.rss())

# Draw optimized layout
fig = lens.draw()
plt.savefig("ipopt_after.png")
plt.close(fig)
