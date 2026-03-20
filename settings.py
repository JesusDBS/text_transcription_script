from enum import StrEnum, auto


class Options(StrEnum):
    TRANS = auto()
    DELETE = auto()


class Formats(StrEnum):
    MP3 = auto()
    MP4 = auto()


def _get_options_values(options: Options) -> list[str]:
    return [option.value for option in options]


def _get_formats_values(formats: Formats) -> list[str]:
    return [f'.{format.value}' for format in formats]


ALLOWED_CLI_OPTIONS = _get_options_values(Options)
ALLOWED_FORMATS = _get_formats_values(Formats)

UPLOADS_FILE_FOLDER = "uploads"
DOWNLOADS_FILE_FOLDER = "downloads"
TRANSCRIPTION_CHUNK_DURATION = 60
RECOGNIZE_GOOGLE_LANGUAGE = "en-US"
