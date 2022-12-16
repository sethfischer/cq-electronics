"""Example usage of CadQuery Electronics top hat DIN rail."""

from cq_electronics.mechanical.din_rail import TopHat

top_hat = TopHat(100, slots=True)
result = top_hat.cq_object

if "show_object" in locals():
    show_object(result, name="din_rail")  # type: ignore[name-defined] # noqa: F821
