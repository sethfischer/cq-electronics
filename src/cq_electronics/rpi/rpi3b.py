"""Raspberry Pi 3 Model B."""

import cadquery as cq

from cq_electronics.colors import (
    package_black,
    pcb_substrate_chiffon,
    solder_mask_green,
    tin_plate,
)
from cq_electronics.connectors.headers import PinHeader
from cq_electronics.connectors.rj45 import JackSurfaceMount
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

    def __init__(self, simple: bool = True):
        """Initialise Raspberry Pi 3 Model B."""
        self.simple = simple
        self.hole_points = self._pcb_mounting_hole_points()
        self._cq_object = self.make()

    @property
    def cq_object(self):
        """Raspberry Pi 3 Model B assembly."""
        return self._cq_object

    def _pcb_mounting_hole_points(self):
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

    def make(self) -> cq.Assembly:
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

        bcm2837 = BGA(14, 14, simple=self.simple).make()
        bcm2837.faces("<Z").tag("board_side")

        usb_controller = BGA(9, 9, simple=self.simple).make()
        usb_controller.faces("<Z").tag("board_side")

        ram = BGA(9, 9, simple=self.simple).make()
        ram.faces("<Z").tag("board_side")

        rpi = (
            cq.Assembly()
            .add(
                substrate, name="pcb_substrate", color=cq.Color(*pcb_substrate_chiffon)
            )
            .add(
                solder_mask,
                name="pcb_solder_mask_top",
                color=cq.Color(*solder_mask_green),
            )
            .add(
                solder_mask,
                name="pcb_solder_mask_bottom",
                color=cq.Color(*solder_mask_green),
            )
            .add(ethernet_port, name="ethernet_port", color=cq.Color(*tin_plate))
            .add(
                bcm2837,
                name="bcm2837",
                color=cq.Color(*package_black),
            )
            .add(usb_controller, name="usb_controller", color=cq.Color(*package_black))
            .add(ram, name="ram", color=cq.Color(*package_black))
            .add(
                gpio,
                name="gpio",
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
            rpi.constrain("pcb_substrate", "Fixed")
            .constrain("pcb_solder_mask_top", "FixedRotation", (0, 0, 0))
            .constrain("pcb_solder_mask_bottom", "FixedRotation", (0, 0, 0))
            .constrain(
                "pcb_substrate?hole_upper", "pcb_solder_mask_top?hole_lower", "Point"
            )
            .constrain(
                "pcb_substrate?hole_lower", "pcb_solder_mask_bottom?hole_upper", "Point"
            )
            .constrain("ethernet_port", "FixedRotation", (0, 0, 90))
            .constrain(
                "ethernet_port?board_side",
                "pcb_solder_mask_top@faces@>Z",
                "PointInPlane",
            )
            .constrain(
                "ethernet_port@faces@>X",
                "pcb_solder_mask_top@faces@>Y",
                "PointInPlane",
                param=2.5,
            )
            .constrain(
                "ethernet_port@faces@<Y",
                "pcb_solder_mask_top@faces@>X",
                "PointInPlane",
                param=-2,
            )
            .constrain("bcm2837", "FixedRotation", (0, 0, 0))
            .constrain("bcm2837", "pcb_solder_mask_top@faces@>Z", "PointInPlane")
            .constrain(
                "bcm2837@faces@<Y",
                "pcb_solder_mask_top@faces@<Y",
                "PointInPlane",
                param=-20,
            )
            .constrain(
                "bcm2837@faces@>X",
                "pcb_solder_mask_top@faces@>X",
                "PointInPlane",
                param=-20,
            )
            .constrain("usb_controller", "FixedRotation", (0, 0, 0))
            .constrain("usb_controller", "pcb_solder_mask_top@faces@>Z", "PointInPlane")
            .constrain(
                "usb_controller@faces@<Y",
                "pcb_solder_mask_top@faces@<Y",
                "PointInPlane",
                param=-53,
            )
            .constrain(
                "usb_controller@faces@>X",
                "pcb_solder_mask_top@faces@>X",
                "PointInPlane",
                param=-28,
            )
            .constrain("ram", "FixedRotation", (0, 180, 0))
            .constrain("ram", "pcb_solder_mask_bottom@faces@<Z", "PointInPlane")
            .constrain(
                "ram@faces@<Y",
                "pcb_solder_mask_top@faces@<Y",
                "PointInPlane",
                param=-37,
            )
            .constrain(
                "ram@faces@>X",
                "pcb_solder_mask_top@faces@<X",
                "PointInPlane",
                param=-17,
            )
        )

        rpi.solve()

        return rpi
