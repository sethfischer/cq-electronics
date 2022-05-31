"""BGA packages."""

import cadquery as cq


class BGA:
    """BGA generic package.

    Ball grid array (BGA) surface-mount packaging.

    :param length: Length of package.
    :type length: float
    :param width: Width of package.
    :type width: float
    :param height: Thickness of package.
    :type height: float, optional, defaults to 1 mm
    :param simple: Create shape with reduced detail.
    :type simple: bool, optional, defaults to True
    """

    def __init__(
        self, length: float, width: float, height: float = 1, simple: bool = True
    ):
        """Initialise BGA generic package."""
        self.length = length
        self.width = width
        self.height = height
        self.simple = simple
        self._cq_object = self.make()

    @property
    def cq_object(self):
        """BGA generic package."""
        return self._cq_object

    def make(self) -> cq.Workplane:
        """Make BGA generic package.

        :return: BGA generic package.
        :rtype: cadquery.Workplane
        """
        result = cq.Workplane("XY").box(self.length, self.width, self.height)

        if not self.simple:
            index_mark_radius = 2
            index_mark_loc_x = -((self.length / 2) - 1)
            index_mark_loc_y = -((self.width / 2) - 1)
            index_mark_elevation = (self.height / 2) + (index_mark_radius * 0.93)

            index_mark = cq.Workplane(
                origin=(
                    index_mark_loc_x,
                    index_mark_loc_y,
                    index_mark_elevation,
                )
            ).sphere(index_mark_radius)

            result = result.cut(index_mark)

        return result
