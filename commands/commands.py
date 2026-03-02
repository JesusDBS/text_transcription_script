from . import Command
from services import services

transcript_service = services.GoogleSpeechRecognitionService()


class TranscriptFilesCommand(Command):
    def execute(self, files_path: list[str]) -> None:
        for file_path in files_path:
            transcript_service.transcript(file_path)


class DeleteFilesCommand(Command):
    def execute(self, files_path: list[str]) -> None:
        for file_path in files_path:
            services.delete_service(file_path)
