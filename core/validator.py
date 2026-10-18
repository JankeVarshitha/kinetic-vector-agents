import xml.etree.ElementTree as ET

class VectorValidator:
    """Runs automated programmatic compilation checks against Abstract Syntax Trees (AST)."""
    @staticmethod
    def validate_svg_syntax(xml_string: str) -> tuple[bool, str]:
        if not xml_string or "<svg" not in xml_string.lower():
            return False, "Output lacks structural SVG root context signatures."
        try:
            # Executes strict XML structural validation pass
            ET.fromstring(xml_string)
            return True, xml_string
        except ET.ParseError as e:
            return False, f"AST Parsing Exception: {str(e)}"
