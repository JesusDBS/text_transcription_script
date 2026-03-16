from enum import StrEnum, auto
from typing import TypeVar, Type

E = TypeVar('E', bound=StrEnum)


class Options(StrEnum):
    TRANS = auto()
    DELETE = auto()


class Formats(StrEnum):
    MP3 = ".mp3"
    MP4 = ".mp4"


def _get_enum_values(enum: Type[E]) -> list[str]:
    return [member.value for member in enum]


ALLOWED_CLI_OPTIONS = _get_enum_values(Options)
ALLOWED_FORMATS = _get_enum_values(Formats)

UPLOADS_FILE_FOLDER = "uploads"
DOWNLOADS_FILE_FOLDER = "downloads"
TRANSCRIPTION_CHUNK_DURATION = 60
RECOGNIZE_GOOGLE_LANGUAGE = "en-US"
