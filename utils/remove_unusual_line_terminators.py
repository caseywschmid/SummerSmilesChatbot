def remove_unusual_line_terminators(s: str) -> str:
    """
    Remove Unicode Line Separator (U+2028) and Paragraph Separator (U+2029) from a string.
    """
    return s.replace("\u2028", "").replace("\u2029", "")
