"""Sourcekit® PiTray clip."""

import cadquery as cq

from cq_electronics.colors import COLORS
from cq_electronics.fasteners import M2R5_TAP_HOLE_DIAMETER, M4_TAP_HOLE_DIAMETER
from cq_electronics.mechanical.din_clip import DinClip
from cq_electronics.rpi.rpi3b import RPi3b


class PiTrayClip:
    """Sourcekit PiTray clip.

    :Manufacturer:
        `Sourcekit <https://sourcekit.cc/>`_
    :Model:
        PiTray clip
    """

    LENGTH = 76
    WIDTH = 20
    HEIGHT = 15
    THICKNESS = 1.4

    def __init__(self):
        """Initialise PiTray clip."""
        self.pcb_screw_cylinder_radius = 4.1 / 2
        self.pcb_screw_cylinder_from_edge = 3.7
        self.pcb_screw_cylinder_length = 5.5

        self.clip_screw_cylinder_radius = 7.95 / 2
        self.clip_screw_cylinder_length = 4

        self.corner_fillet_radius = 3

        pcb_screw_center = (
            -RPi3b.HOLE_CENTERS_LONG / 2,
            self.HEIGHT / 2 - self.pcb_screw_cylinder_from_edge,
        )

        self.pcb_mount_hole_centers = [
            pcb_screw_center,
            (-pcb_screw_center[0], pcb_screw_center[1]),
        ]

        clip_mount_hole_center = (-DinClip.BETWEEN_MOUNT_HOLES / 2, 0)
        self.clip_mount_hole_centers = [
            clip_mount_hole_center,
            (-clip_mount_hole_center[0], clip_mount_hole_center[1]),
        ]

        self.cutout_origin = (-self.WIDTH / 2, -self.HEIGHT / 2 + self.THICKNESS)

        self._cq_object = self.make()

    @property
    def cq_object(self):
        """Get PiTray clip."""
        return self._cq_object

    def make(self):
        """Make PiTray clip."""
        angle = (
            cq.Workplane("ZY")
            .box(self.HEIGHT, self.WIDTH, self.LENGTH)
            .faces(">X")
            .workplane()
            .pushPoints([self.cutout_origin])
            .rect(
                self.WIDTH - self.THICKNESS,
                self.HEIGHT - self.THICKNESS,
                centered=False,
            )
            .cutThruAll()
        )

        bracket = (
            angle.faces(">>Y")
            .workplane(centerOption="CenterOfBoundBox")
            .tag("workplane__pcb_face")
            .workplane(offset=-self.pcb_screw_cylinder_length / 2)
            .pushPoints(self.pcb_mount_hole_centers)
            .cylinder(self.pcb_screw_cylinder_length, self.pcb_screw_cylinder_radius)
            .workplaneFromTagged("workplane__pcb_face")
            .pushPoints(self.pcb_mount_hole_centers)
            .hole(M2R5_TAP_HOLE_DIAMETER)
            .faces("<<Z")
            .workplane(centerOption="CenterOfBoundBox")
            .tag("workplane__clip_face")
            .workplane(offset=-self.clip_screw_cylinder_length / 2)
            .pushPoints(self.clip_mount_hole_centers)
            .cylinder(self.clip_screw_cylinder_length, self.clip_screw_cylinder_radius)
            .workplaneFromTagged("workplane__clip_face")
            .pushPoints(self.clip_mount_hole_centers)
            .hole(M4_TAP_HOLE_DIAMETER)
        )

        selector = {
            "edge_1": "(>>X and >>Z)",
            "edge_2": "(>>X and <<Y)",
            "edge_3": "(<<X and >>Z)",
            "edge_4": "(<<X and <<Y)",
        }
        bracket = bracket.edges(" or ".join(selector.values())).fillet(
            self.corner_fillet_radius
        )

        din_clip = DinClip()
        din_clip_elevation = -(self.HEIGHT / 2 + DinClip.HEIGHT / 2)

        assembly = (
            cq.Assembly()
            .add(
                bracket,
                name="bracket",
                color=cq.Color(*COLORS["stainless_steel"]),
            )
            .add(
                din_clip.cq_object,
                name="din_clip",
                color=cq.Color(*COLORS["black_plastic"]),
                loc=cq.Location(cq.Vector(0, 0, din_clip_elevation)),
            )
        )

        return assembly
