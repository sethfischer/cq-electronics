"""Example usage of CadQuery Electronics Raspberry Pi 3 Model B."""

from cq_electronics.rpi.rpi3b import RPi3b

rpi = RPi3b(simple=False)
result = rpi.cq_object

if "show_object" in locals():
    show_object(result, name="rpi_3b")
