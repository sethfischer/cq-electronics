"""Pin headers."""

import cadquery as cq

from cq_electronics.colors import black_plastic, gold_plate


class PinHeader:
    """Straight pin header.

    :param rows: Number of pin rows.
    :type rows: int, optional
    :param columns: Number of pin columns.
    :type columns:  int, optional
    :param above: Length of pin above base.
    :type above: float, optional, defaults to 7 mm
    :param below: Length of pin below base.
    :type below: float, optional, defaults to 3 mm
    :param simple: Create shape with reduced detail.
    :type simple: bool, optional, defaults to True
    """

    #: Pin pitch.
    PITCH = 2.54
    PIN_WIDTH = 0.64
    #: Chamfer on ends of pins.
    PIN_CHAMFER = 0.2
    #: Height of insulating base.
    BASE_HEIGHT = 2.4

    def __init__(
        self,
        rows: int = 1,
        columns: int = 1,
        above: float = 7,
        below: float = 3,
        simple: bool = True,
    ):
        """Initialise pin header."""
        self.rows = rows
        self.columns = columns
        self.above = above
        self.below = below
        self.simple = simple
        self._cq_object = self.make()

    @property
    def cq_object(self):
        """Pin header."""
        return self._cq_object

    def make(self) -> cq.Workplane:
        """Make pin header.

        :return: Pin header.
        :rtype: cadquery.Assembly
        """
        pin_length = self.above + self.BASE_HEIGHT + self.below

        base_width = self.PITCH * self.rows
        base_length = self.PITCH * self.columns

        pin_points = []

        for row in range(self.rows):
            loc_y = (self.PITCH / 2) + (row * self.PITCH)
            for column in range(self.columns):
                loc_x = (self.PITCH / 2) + (column * self.PITCH)
                pin_points.append((loc_x, loc_y))

        base = (
            cq.Workplane()
            .box(base_length, base_width, self.BASE_HEIGHT, centered=False)
            .faces(">Z")
            .workplane()
            .pushPoints(pin_points)
            .rect(self.PIN_WIDTH, self.PIN_WIDTH)
            .cutThruAll()
        )

        pin = cq.Workplane().box(self.PIN_WIDTH, self.PIN_WIDTH, pin_length)

        if not self.simple:
            pin = (
                pin.edges("<Z")
                .chamfer(self.PIN_CHAMFER)
                .edges(">Z")
                .chamfer(self.PIN_CHAMFER)
            )

        pin_elevation = (pin_length / 2) - self.below

        header = cq.Assembly(color=cq.Color(*gold_plate))
        header.add(base, name="base", color=cq.Color(*black_plastic))

        for row in range(self.rows):
            loc_y = (self.PITCH / 2) + (row * self.PITCH)
            for column in range(self.columns):
                loc_x = (self.PITCH / 2) + (column * self.PITCH)
                location = cq.Location(cq.Vector(loc_x, loc_y, pin_elevation))
                header.add(pin, name=f"pin_{row}-{column}", loc=location)

        return header
