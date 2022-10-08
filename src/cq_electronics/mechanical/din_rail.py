"""DIN rails."""

import cadquery as cq


class TopHat:
    """Top hat DIN rail.

    :Standard:
        IEC 60715

    The IEC 60715 standard specifies both a 7.5 mm (default) and a 15 mm deep version,
    which are designated:

    * IEC 60715 – 35 × 7.5
    * IEC 60715 – 35 × 15

    :param depth: Rail height. Typically, 7.5 mm or 15 mm. Defaults to 7.5 mm
    :type depth: float, optional
    """

    #: Width of rail.
    WIDTH = 35
    #: Material thickness.
    THICKNESS = 1
    CHANNEL_WIDTH = 25
    FILLET_RADIUS = 0.25

    BRIM_WIDTH = (WIDTH - CHANNEL_WIDTH) / 2
    BRIM_CUT_POS_Y = (WIDTH / 2) - (BRIM_WIDTH / 2) + (THICKNESS / 2)

    def __init__(self, length: float, depth: float = 7.5):
        """Initialise DIN rail depth."""
        self.length = length
        self.depth = depth

        self._cq_object = self._make(self.length)

    @property
    def cq_object(self):
        """DIN rail."""
        return self._cq_object

    def _make(self, length: float) -> cq.Workplane:
        """Make DIN rail and extrude to specified length.

        :param length: Rail length.
        :type length: float

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

        return profile.finalize().extrude(length)
