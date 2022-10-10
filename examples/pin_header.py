"""Example usage of CadQuery Electronics pin header."""

from cq_electronics.connectors.headers import PinHeader

pin_header = PinHeader(rows=2, columns=10, simple=False)
result = pin_header.cq_object

if "show_object" in locals():
    show_object(result, name="pin_header")  # noqa: F821
