"""RJ45 connectors."""
import cadquery as cq


class JackSurfaceMount:
    """RJ45 modular jack single-port surface-mount.

    :Connector Type:
        RJ45
    :Port Configuration:
        1 x 1

    :param length: Length of body.
    :type length: float, optional
    :param simple: Create shape with reduced detail.
    :type simple: bool, optional, defaults to True
    """

    #: Length of body with magnetics.
    LENGTH_MAGNETIC = 21
    #: Length of body without magnetics.
    LENGTH_NON_MAGNETIC = 16

    def __init__(self, length: float = LENGTH_MAGNETIC, simple: bool = True):
        """Initialise RJ45 modular jack single-port surface-mount."""
        self.length = length
        self.width = 16
        self.height = 14
        self.simple = simple
        self._cq_object = self.make()

    @property
    def cq_object(self):
        """RJ45 modular jack single-port surface-mount."""
        return self._cq_object

    def make(self) -> cq.Workplane:
        """Make RJ45 Jack.

        :return: RJ45 Jack.
        :rtype: cadquery.Workplane
        """
        aperture_width = 11.68
        aperture_height = 7.75
        aperture_depth = -15
        keyway_width = 6
        keyway_height = 1.5
        retainer_width = 3.25
        retainer_height = 1.5
        retainer_depth = 2

        keyway_elevation = -(aperture_height / 2) - (keyway_height / 2)
        retainer_elevation = keyway_elevation - (retainer_height / 2)

        result = cq.Workplane("XY").box(self.length, self.width, self.height)

        if not self.simple:
            result = (
                result.faces(">X")
                .workplane()
                .tag("aperture")
                .rect(aperture_width, aperture_height)
                .cutBlind(aperture_depth)
                .workplaneFromTagged("aperture")
                .move(0, keyway_elevation)
                .rect(keyway_width, keyway_height)
                .cutBlind(aperture_depth)
                .workplaneFromTagged("aperture")
                .move(0, retainer_elevation)
                .rect(retainer_width, retainer_height)
                .cutBlind(aperture_depth)
                .faces(">X")
                .workplane(offset=-retainer_depth)
                .move(0, retainer_elevation)
                .rect(keyway_width, keyway_height)
                .cutBlind(aperture_depth + retainer_depth)
            )

        return result
