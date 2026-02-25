from enum import Enum


class Options(Enum):
    TRANS = "trans"
    DELETE = "delete"


class Formats(Enum):
    MP3 = ".mp3"
    MP4 = ".mp4"


ALLOWED_CLI_OPTIONS = [option.value for option in Options]
ALLOWED_FORMATS = [format.value for format in Formats]

UPLOADS_FILE_FOLDER = "uploads"
DOWNLOADS_FILE_FOLDER = "downloads"
