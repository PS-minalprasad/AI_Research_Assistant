import os


def ensure_directory(path):
    """
    Create directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)


def count_files(folder):
    """
    Count files in a folder.
    """
    if not os.path.exists(folder):
        return 0

    return len(os.listdir(folder))


def get_file_extension(filename):
    """
    Return file extension.
    """
    return os.path.splitext(filename)[1].lower()