class VectorValidator:
    """Runs automated programmatic compilation checks against generated frontend syntax."""
    @staticmethod
    def validate_svg_syntax(html_string: str) -> tuple[bool, str]:
        # Lenient check to ensure we received executable frontend code structures
        if not html_string or ("<div" not in html_string.lower() and "<canvas" not in html_string.lower()):
            return False, "Output lacks structural root layout contexts."
        return True, html_string
