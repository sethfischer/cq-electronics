"""Example usage of CadQuery Electronics pin header."""

from cq_electronics.connectors.headers import PinHeader

result = PinHeader(rows=2, columns=10, simple=False).cq_object

if "show_object" in locals():
    show_object(result, name="pin_header")
