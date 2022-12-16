"""DIN rails."""

import cadquery as cq

from cq_electronics.cq_containers import CqWorkplaneContainer


class TopHat(CqWorkplaneContainer):
    """Top hat DIN rail.

    :Standard:
        IEC 60715

    The IEC 60715 standard specifies both a 7.5 mm (default) and a 15 mm deep version,
    which are designated:

    * IEC 60715 – 35 × 7.5
    * IEC 60715 – 35 × 15

    :param length: Rail length.
    :type length: float
    :param depth: Rail height. Typically, 7.5 mm or 15 mm.
    :type depth: float, optional, Defaults to 7.5 mm.
    :param slots: Add mounting slots.
    :type slots: bool, optional, Defaults to True.
    """

    #: Width of rail.
    WIDTH = 35
    #: Material thickness.
    THICKNESS = 1
    CHANNEL_WIDTH = 25
    FILLET_RADIUS = 0.25

    BRIM_WIDTH = (WIDTH - CHANNEL_WIDTH) / 2
    BRIM_CUT_POS_Y = (WIDTH / 2) - (BRIM_WIDTH / 2) + (THICKNESS / 2)

    def __init__(self, length: float, depth: float = 7.5, slots: bool = True) -> None:
        """Initialise DIN rail depth."""
        self.length = length
        self.depth = depth
        self.slots = slots

        self._cq_object = self._make()

    def _make(self) -> cq.Workplane:
        """Make DIN rail and extrude to specified length.

        :return: DIN rail
        :rtype: cadquery.Workplane
        """
        profile = (
            cq.Workplane("ZY")
            .sketch()
            .rect(self.depth, self.WIDTH)
            .push([(self.THICKNESS / 2, 0)])
            .rect(self.depth - self.THICKNESS, self.CHANNEL_WIDTH, mode="s")
            .push(
                [
                    (-self.THICKNESS, -self.BRIM_CUT_POS_Y),
                    (-self.THICKNESS, self.BRIM_CUT_POS_Y),
                ]
            )
            .rect(self.depth, self.BRIM_WIDTH - self.THICKNESS, mode="s")
            .clean()
            .reset()
            .vertices("not(>Y or <Y)")
            .fillet(self.FILLET_RADIUS)
        )

        result: cq.Workplane = profile.finalize().extrude(self.length)

        if self.slots:
            result = self._add_slots(result)

        return result

    def _add_slots(self, extrusion: cq.Workplane) -> cq.Workplane:
        """Add mounting slots."""
        slot_width = 4.5
        slot_length = 25
        between_slots = 10
        between_slot_centers = slot_length + between_slots

        center = -self.length / 2
        slot_locations = [(center, 0)]

        x_coordinate = center + between_slot_centers
        y_coordinate = 0
        while x_coordinate < 0:
            slot_locations.append((x_coordinate, y_coordinate))
            slot_locations.append((center - abs(center - x_coordinate), y_coordinate))

            x_coordinate += between_slot_centers

        result = (
            extrusion.faces(">Z")
            .workplane()
            .pushPoints(slot_locations)
            .slot2D(slot_length, slot_width, 0)
            .cutThruAll()
        )

        return result
