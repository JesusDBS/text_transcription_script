from enum import StrEnum, auto
from typing import TypeVar


class Options(StrEnum):
    TRANS = auto()
    DELETE = auto()


class Formats(StrEnum):
    MP3 = auto()
    MP4 = auto()


E = TypeVar('E', bound=StrEnum)


def _get_options_values(options: type[E]) -> list[str]:
    return [option.value for option in options]


def _get_formats_values(formats: type[E]) -> list[str]:
    return [f'.{format.value}' for format in formats]


ALLOWED_CLI_OPTIONS = _get_options_values(Options)
ALLOWED_FORMATS = _get_formats_values(Formats)

UPLOADS_FILE_FOLDER = "uploads"
DOWNLOADS_FILE_FOLDER = "downloads"
TRANSCRIPTION_CHUNK_DURATION = 60
RECOGNIZE_GOOGLE_LANGUAGE = "en-US"

# NOTE
# The available backends include:
# - google_speech_recognition
# - whisper_speech_recognition
ACTIVE_TRANSCRIPT_BACKEND = "whisper_speech_recognition"
