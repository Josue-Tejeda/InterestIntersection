

def get_file_extension(url):
    """Return the file extension from a URL."""
    return url.rsplit('.', 1)[1].lower()