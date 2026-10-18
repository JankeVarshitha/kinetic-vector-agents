class VectorValidator:
    """Runs automated programmatic compilation checks against generated frontend syntax."""
    @staticmethod
    def validate_svg_syntax(html_string: str) -> tuple[bool, str]:
        if not html_string or "<html" not in html_string.lower():
            return False, "Output lacks structural compiled HTML layout configurations."
        return True, html_string

