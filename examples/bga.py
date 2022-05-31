"""Example usage of CadQuery Electronics BGA package."""

from cq_electronics.smd.bga import BGA

result = BGA(20, 20, simple=False).make()

if "show_object" in locals():
    show_object(result, name="bga_package")
