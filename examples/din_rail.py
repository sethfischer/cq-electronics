"""Example usage of CadQuery Electronics din_rail."""

from cq_electronics.mechanical.din_rail import TopHat

result = TopHat().make(100)

if "show_object" in locals():
    show_object(result, name="din_rail")
