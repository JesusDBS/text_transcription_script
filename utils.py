import os
import mimetypes
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


def get_file_path(filename_path: str, file_folder: str) -> str:
    """
    Returns the absolute path of the file.

    Parameters
    ----------
    filename_path : str
        Path components of the filename, it can be a video or audio file.

    Returns
    -------
    str
        Absolute path of the file.
    """
    filename_path = os.path.join(file_folder, filename_path)
    return os.path.abspath(filename_path)


def get_file_name(filename_path: str) -> str:
    """
    Returns the name of the file.

    Parameters
    ----------
    filename_path : str
        Path components of the filename, it can be a video or audio file.

    Returns
    -------
    str
        Name of the file.
    """
    return os.path.basename(filename_path)


def get_file_type(file_path: str) -> str | None:
    """Returns the MIME type of the file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str | None: MIME type of the file, or None if unknown.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type


def change_filename_extension(filename: str, new_extension: str) -> str:
    """
    Changes the file extension of the given filename to the new extension.

    Parameters
    ----------
    filename : str
        File whose extension is to be changed.
    new_extension : str
        New file extension (e.g., '.wav').

    Returns
    -------
    str
        The file path with the new extension.
    """
    base = os.path.splitext(filename)[0]
    return f"{base}{new_extension}"
