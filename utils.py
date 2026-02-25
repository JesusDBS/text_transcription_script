import os

import settings


def allowed_file(filename: str) -> bool:
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we can accept only video or audio files.

    Parameters
    ----------
    filename : str
        Filename, it can be a video or audio file.

    Returns
    -------
    bool
        True if the file is a video or audio file, False otherwise.
    """
    filename, file_extension = os.path.splitext(filename)
    if file_extension.lower() in settings.ALLOWED_FORMATS:
        return True

    return False


def get_file_path(filename_path: list[str]) -> str:
    """
    Returns the path of the file.

    Parameters
    ----------
    filename_path : list[str]
        Path components of the filename, it can be a video or audio file.

    Returns
    -------
    str
        Absolute path of the file.
    """
    return os.path.join(*filename_path)
