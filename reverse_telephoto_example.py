import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend

import matplotlib.pyplot as plt
from optiland.samples.objectives import ReverseTelephoto
import numpy as np

lens = ReverseTelephoto()
lens.draw() # This will not display in a non-GUI environment
plt.savefig("lens_plot.png")  # Save instead of show
