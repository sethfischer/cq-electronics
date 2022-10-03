"""Example usage of CadQuery Electronics din_rail."""

from cq_electronics.mechanical.din_rail import TopHat

top_hat = TopHat(100)
result = top_hat.cq_object

if "show_object" in locals():
    show_object(result, name="din_rail")
