"""Example usage of CadQuery Electronics RJ45 modular jack."""

from cq_electronics.connectors.rj45 import JackSurfaceMount

result = JackSurfaceMount(simple=False).make()

if "show_object" in locals():
    show_object(result, name="rj45_jack")
