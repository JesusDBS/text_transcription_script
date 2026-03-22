from . import Command
from services import services
from settings import ACTIVE_TRANSCRIPT_BACKEND

transcript_service = services.set_transcript_service(
    active_transcript_backend=ACTIVE_TRANSCRIPT_BACKEND)


class TranscriptFilesCommand(Command):
    def execute(self, files_path: list[str]) -> None:
        for file_path in files_path:
            transcript_service.transcript(file_path)


class DeleteFilesCommand(Command):
    def execute(self, files_path: list[str]) -> None:
        for file_path in files_path:
            services.delete_service(file_path)
