"""Example usage of CadQuery Electronics DIN clip."""

from cq_electronics.mechanical.din_clip import DinClip

din_clip = DinClip()
result = din_clip.cq_object

if "show_object" in locals():
    show_object(result, name="din_clip")  # noqa: F821
