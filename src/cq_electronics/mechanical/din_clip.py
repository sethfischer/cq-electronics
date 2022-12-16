"""DIN rail clips."""

import cadquery as cq

from cq_electronics.cq_containers import CqWorkplaneContainer
from cq_electronics.fasteners import (
    M4_CLEARANCE_NORMAL_DIAMETER,
    M4_COUNTERSINK_DIAMETER,
    M_COUNTERSINK_ANGLE,
)
from cq_electronics.mechanical.din_rail import TopHat


class DinClip(CqWorkplaneContainer):
    """Plastic DIN rail clip."""

    LENGTH = 76
    WIDTH = 20
    HEIGHT = 8
    BETWEEN_MOUNT_HOLES = 63
    RAIL_APERTURE_DEPTH = 4
    CORNER_CHAMFER = 3

    def __init__(self) -> None:
        """Initialise DIN rail clip."""
        self.half_length = self.LENGTH / 2
        self.rail_aperture_offset = self.half_length - 30
        self.half_between_mount_holes = self.BETWEEN_MOUNT_HOLES / 2
        self.rail_aperture_center = (-self.rail_aperture_offset, 0)

        self.outer_mount_hole_centers = [
            (self.half_between_mount_holes, 0),
            (-self.half_between_mount_holes, 0),
        ]

        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make DIN rail clip."""
        result = (
            cq.Workplane()
            .box(self.LENGTH, self.WIDTH, self.HEIGHT)
            .faces("<<Z")
            .workplane()
            .tag("workplane__rail_face")
            .pushPoints([self.rail_aperture_center])
            .rect(TopHat.WIDTH, self.WIDTH)
            .cutBlind(-self.RAIL_APERTURE_DEPTH)
            .workplaneFromTagged("workplane__rail_face")
            .pushPoints(self.outer_mount_hole_centers)
            .cskHole(
                M4_CLEARANCE_NORMAL_DIAMETER,
                M4_COUNTERSINK_DIAMETER,
                M_COUNTERSINK_ANGLE,
            )
            .faces(">Z[1]")
            .workplane(centerOption="CenterOfBoundBox")
            .tag("workplane__rail_aperture_face")
            .cskHole(
                M4_CLEARANCE_NORMAL_DIAMETER,
                M4_COUNTERSINK_DIAMETER,
                M_COUNTERSINK_ANGLE,
            )
            .edges("|Z and (>X or <X)")
            .chamfer(self.CORNER_CHAMFER)
        )

        return result
