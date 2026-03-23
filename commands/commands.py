import os
from . import Command
from services.services import set_transcript_service
from settings import ACTIVE_TRANSCRIPT_BACKEND

transcript_service = set_transcript_service(
    active_transcript_backend=ACTIVE_TRANSCRIPT_BACKEND)


class TranscriptFilesCommand(Command):
    def execute(self, files_path: list[str]) -> None:
        for file_path in files_path:
            transcript_service.transcript(file_path)


def delete_service(filepath: str) -> None:
    try:
        if os.path.isfile(filepath):
            os.remove(filepath)
            print(f'....{filepath} has been deleted....', '\n')

    except FileExistsError as error:
        raise error
    except FileNotFoundError as error:
        raise error
    except Exception as error:
        raise error


class DeleteFilesCommand(Command):
    def execute(self, files_path: list[str]) -> None:
        for file_path in files_path:
            delete_service(file_path)
