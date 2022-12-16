"""Example usage of CadQuery Electronics Sourcekit® PiTray clip."""

from cq_electronics.sourcekit.pitray_clip import PiTrayClip

pitray_clip = PiTrayClip()
result = pitray_clip.cq_object

if "show_object" in locals():
    show_object(result, name="pitray_clip")  # type: ignore[name-defined] # noqa: F821
