"""Raspberry Pi 3 Model B."""

from typing import List, Tuple

import cadquery as cq

from cq_electronics.connectors.headers import PinHeader
from cq_electronics.connectors.rj45 import JackSurfaceMount
from cq_electronics.materials import COLORS
from cq_electronics.smd.bga import BGA


class RPi3b:
    """Raspberry Pi 3 Model B.

    :Manufacturer:
        `Raspberry Pi Foundation <https://www.raspberrypi.com>`_
    :Model:
        Raspberry Pi 3 Model B

    :param simple: Create with reduced detail.
    :type simple: bool, optional, defaults to True
    """

    HEIGHT = 56
    WIDTH = 85
    THICKNESS = 1.5
    SOLDER_MASK_THICKNESS = 0.05

    CORNER_RADIUS = 3

    HOLE_DIAMETER = 2.7
    HOLE_SOLDER_MASK_DIAMETER = 6
    HOLE_OFFSET_FROM_EDGE = 3.5
    HOLE_CENTERS_LONG = 58

    def __init__(self, simple: bool = True) -> None:
        """Initialise Raspberry Pi 3 Model B."""
        self.simple = simple
        self.hole_points = self._pcb_mounting_hole_points()

        self._cq_object = self._make()

    @property
    def cq_object(self) -> cq.Assembly:
        """Raspberry Pi 3 Model B assembly."""
        return self._cq_object

    def _pcb_mounting_hole_points(self) -> List[Tuple[float, float]]:
        """Calculate PCB mounting hole locations."""
        offset = -self.WIDTH / 2 + self.HOLE_OFFSET_FROM_EDGE + self.HOLE_CENTERS_LONG

        points = [
            (
                self.HEIGHT / 2 - self.HOLE_OFFSET_FROM_EDGE,
                offset,
            ),
            (
                -(self.HEIGHT / 2 - self.HOLE_OFFSET_FROM_EDGE),
                -(self.WIDTH / 2 - self.HOLE_OFFSET_FROM_EDGE),
            ),
            (
                -(self.HEIGHT / 2 - self.HOLE_OFFSET_FROM_EDGE),
                offset,
            ),
            (
                self.HEIGHT / 2 - self.HOLE_OFFSET_FROM_EDGE,
                -(self.WIDTH / 2 - self.HOLE_OFFSET_FROM_EDGE),
            ),
        ]

        return points

    def _substrate(self) -> cq.Workplane:
        """Make PCB substrate."""
        substrate = (
            cq.Workplane("XY")
            .box(self.HEIGHT, self.WIDTH, self.THICKNESS)
            .faces(">Z")
            .workplane(centerOption="CenterOfMass")
            .rect(
                self.HEIGHT - (self.HOLE_OFFSET_FROM_EDGE * 2),
                self.WIDTH - (self.HOLE_OFFSET_FROM_EDGE * 2),
                forConstruction=True,
            )
            .vertices()
            .pushPoints(self.hole_points)
            .hole(self.HOLE_DIAMETER)
            .tag("holes")
            .edges("|Z")
            .fillet(self.CORNER_RADIUS)
        )

        return substrate

    def _solder_mask(self) -> cq.Workplane:
        """Make PCB solder mask."""
        solder_mask = (
            cq.Workplane("XY")
            .box(self.HEIGHT, self.WIDTH, self.SOLDER_MASK_THICKNESS)
            .faces(">Z")
            .workplane(centerOption="CenterOfMass")
            .pushPoints(self.hole_points)
            .hole(self.HOLE_SOLDER_MASK_DIAMETER)
            .tag("holes")
            .edges("|Z")
            .fillet(self.CORNER_RADIUS)
        )

        return solder_mask

    def _make(self) -> cq.Assembly:
        """Make Raspberry Pi 3 Model B.

        :return: Raspberry Pi 3 Model B.
        :rtype: cadquery.Assembly
        """
        substrate = self._substrate()
        substrate.edges("%CIRCLE", tag="holes").edges("<X and <Y and >Z").tag(
            "hole_upper"
        )
        substrate.edges("%CIRCLE", tag="holes").edges("<X and <Y and <Z").tag(
            "hole_lower"
        )

        solder_mask = self._solder_mask()
        solder_mask.edges("%CIRCLE", tag="holes").edges("<X and <Y and >Z").tag(
            "hole_upper"
        )
        solder_mask.edges("%CIRCLE", tag="holes").edges("<X and <Y and <Z").tag(
            "hole_lower"
        )

        ethernet_port = JackSurfaceMount(simple=self.simple).cq_object
        ethernet_port.faces("<Z").tag("board_side")
        ethernet_port.faces(">X").tag("aperture_side")

        gpio = PinHeader(rows=2, columns=20, simple=self.simple).cq_object

        bcm2837 = BGA(14, 14, simple=self.simple).cq_object
        bcm2837.faces("<Z").tag("board_side")

        usb_controller = BGA(9, 9, simple=self.simple).cq_object
        usb_controller.faces("<Z").tag("board_side")

        ram = BGA(9, 9, simple=self.simple).cq_object
        ram.faces("<Z").tag("board_side")

        rpi = (
            cq.Assembly()
            .add(
                substrate,
                name="rpi__pcb_substrate",
                color=cq.Color(*COLORS["pcb_substrate_chiffon"]),
            )
            .add(
                solder_mask,
                name="rpi__pcb_solder_mask_top",
                color=cq.Color(*COLORS["solder_mask_green"]),
            )
            .add(
                solder_mask,
                name="rpi__pcb_solder_mask_bottom",
                color=cq.Color(*COLORS["solder_mask_green"]),
            )
            .add(
                ethernet_port,
                name="rpi__ethernet_port",
                color=cq.Color(*COLORS["tin_plate"]),
            )
            .add(
                bcm2837,
                name="rpi__bcm2837",
                color=cq.Color(*COLORS["package_black"]),
            )
            .add(
                usb_controller,
                name="rpi__usb_controller",
                color=cq.Color(*COLORS["package_black"]),
            )
            .add(ram, name="rpi__ram", color=cq.Color(*COLORS["package_black"]))
            .add(
                gpio,
                name="rpi__gpio",
                loc=cq.Location(
                    cq.Vector(
                        -27, 15.5, (self.THICKNESS + self.SOLDER_MASK_THICKNESS) / 2
                    ),
                    cq.Vector(0, 0, 1),
                    -90,
                ),
            )
        )

        rpi = (
            rpi.constrain("rpi__pcb_substrate", "Fixed")
            .constrain("rpi__pcb_solder_mask_top", "FixedRotation", (0, 0, 0))
            .constrain("rpi__pcb_solder_mask_bottom", "FixedRotation", (0, 0, 0))
            .constrain(
                "rpi__pcb_substrate?hole_upper",
                "rpi__pcb_solder_mask_top?hole_lower",
                "Point",
            )
            .constrain(
                "rpi__pcb_substrate?hole_lower",
                "rpi__pcb_solder_mask_bottom?hole_upper",
                "Point",
            )
            .constrain("rpi__ethernet_port", "FixedRotation", (0, 0, 90))
            .constrain(
                "rpi__ethernet_port?board_side",
                "rpi__pcb_solder_mask_top@faces@>Z",
                "PointInPlane",
            )
            .constrain(
                "rpi__ethernet_port@faces@>X",
                "rpi__pcb_solder_mask_top@faces@>Y",
                "PointInPlane",
                param=2.5,
            )
            .constrain(
                "rpi__ethernet_port@faces@<Y",
                "rpi__pcb_solder_mask_top@faces@>X",
                "PointInPlane",
                param=-2,
            )
            .constrain("rpi__bcm2837", "FixedRotation", (0, 0, 0))
            .constrain(
                "rpi__bcm2837", "rpi__pcb_solder_mask_top@faces@>Z", "PointInPlane"
            )
            .constrain(
                "rpi__bcm2837@faces@<Y",
                "rpi__pcb_solder_mask_top@faces@<Y",
                "PointInPlane",
                param=-20,
            )
            .constrain(
                "rpi__bcm2837@faces@>X",
                "rpi__pcb_solder_mask_top@faces@>X",
                "PointInPlane",
                param=-20,
            )
            .constrain("rpi__usb_controller", "FixedRotation", (0, 0, 0))
            .constrain(
                "rpi__usb_controller",
                "rpi__pcb_solder_mask_top@faces@>Z",
                "PointInPlane",
            )
            .constrain(
                "rpi__usb_controller@faces@<Y",
                "rpi__pcb_solder_mask_top@faces@<Y",
                "PointInPlane",
                param=-53,
            )
            .constrain(
                "rpi__usb_controller@faces@>X",
                "rpi__pcb_solder_mask_top@faces@>X",
                "PointInPlane",
                param=-28,
            )
            .constrain("rpi__ram", "FixedRotation", (0, 180, 0))
            .constrain(
                "rpi__ram", "rpi__pcb_solder_mask_bottom@faces@<Z", "PointInPlane"
            )
            .constrain(
                "rpi__ram@faces@<Y",
                "rpi__pcb_solder_mask_top@faces@<Y",
                "PointInPlane",
                param=-37,
            )
            .constrain(
                "rpi__ram@faces@>X",
                "rpi__pcb_solder_mask_top@faces@<X",
                "PointInPlane",
                param=-17,
            )
        )

        rpi.solve()

        return rpi
