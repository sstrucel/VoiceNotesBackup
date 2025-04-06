def sanitize(string):
    """
    Remove all characters not allowed in a filename
    """
    return string.replace(":", "-").replace("/", "-").replace("\\", "-").replace("?", "-").replace("*", "-").replace("<", "-").replace(">", "-").replace("|", "-")