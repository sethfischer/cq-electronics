"""Example usage of CadQuery Electronics BGA package."""

from cq_electronics.smd.bga import BGA

bga = BGA(20, 20, simple=False)
result = bga.cq_object

if "show_object" in locals():
    show_object(result, name="bga_package")  # noqa: F821
