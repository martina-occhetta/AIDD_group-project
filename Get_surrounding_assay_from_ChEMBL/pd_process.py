def str2list(s: str) -> list:
    """
    Convert a string to a list of strings
    """
    return s.replace("'", "").strip('][').split(', ')