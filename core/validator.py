import xml.etree.ElementTree as ET

class VectorValidator:
    """Runs automated programmatic compilation checks against Abstract Syntax Trees (AST)."""
    @staticmethod
    def validate_svg_syntax(xml_string: str) -> tuple[bool, str]:
        print("\n[VALIDATOR START] Evaluating code generation syntax trees...")
        if not xml_string or "<svg" not in xml_string.lower():
            print("[VALIDATOR FAILED] Data lack root structural <svg Context Signature.")
            return False, "Output lacks structural SVG root context signatures."
            
        try:
            # Executes strict XML structural validation pass
            ET.fromstring(xml_string)
            print("[VALIDATOR SUCCESS] XML validated flawlessly through structural compilation validation gates.")
            return True, xml_string
        except ET.ParseError as e:
            print(f"[VALIDATOR FAILED] AST Parsing Exception: {str(e)}")
            print("==== FAILED VECTOR PAYLOAD FOR INSPECTION ====")
            print(xml_string)
            print("==============================================")
            return False, f"AST Parsing Exception: {str(e)}"
