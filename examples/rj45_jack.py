"""Example usage of CadQuery Electronics RJ45 modular jack."""

from cq_electronics.connectors.rj45 import JackSurfaceMount

jack = JackSurfaceMount(simple=False)
result = jack.cq_object

if "show_object" in locals():
    show_object(result, name="rj45_jack")  # type: ignore[name-defined] # noqa: F821
