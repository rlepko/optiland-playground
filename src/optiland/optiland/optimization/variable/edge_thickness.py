"""Edge Thickness Variable Module

This module defines the :class:`EdgeThicknessVariable` which represents
thickness measured at a chosen radial distance from the optical axis. It
allows constraining the edge thickness between two surfaces during
optimization.
"""

import optiland.backend as be
from optiland.optimization.variable.base import VariableBehavior


class EdgeThicknessVariable(VariableBehavior):
    """Represents a variable for the edge thickness between two surfaces."""

    def __init__(self, optic, surface_number, edge_radius, apply_scaling=True, **kwargs):
        super().__init__(optic, surface_number, apply_scaling, **kwargs)
        self.edge_radius = edge_radius

    def _get_sag(self):
        surf_before = self._surfaces.surfaces[self.surface_number]
        surf_after = self._surfaces.surfaces[self.surface_number + 1]
        sag_before = surf_before.geometry.sag(0.0, self.edge_radius)
        sag_after = surf_after.geometry.sag(0.0, self.edge_radius)
        return sag_before, sag_after

    def get_value(self):
        """Return the current edge thickness value."""
        center_t = self._surfaces.get_thickness(self.surface_number)[0]
        sag_before, sag_after = self._get_sag()
        value = center_t + sag_after - sag_before
        if self.apply_scaling:
            return self.scale(value)
        return value

    def update_value(self, new_value):
        """Update the edge thickness to ``new_value``."""
        if self.apply_scaling:
            new_value = self.inverse_scale(new_value)
        sag_before, sag_after = self._get_sag()
        center_t = new_value - sag_after + sag_before
        self.optic.set_thickness(center_t, self.surface_number)

    def scale(self, value):
        return value / 10.0 - 1.0

    def inverse_scale(self, scaled_value):
        return (scaled_value + 1.0) * 10.0

    def __str__(self):
        return f"Edge Thickness, Surface {self.surface_number}"
