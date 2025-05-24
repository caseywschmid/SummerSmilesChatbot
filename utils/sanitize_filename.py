def sanitize_filename(name: str) -> str:
    """
    Sanitize the filename to be filesystem-safe.
    """
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in name)
