from . import Command


class TranscriptFilesCommand(Command):
    def execute(self, files_path: list[str]) -> None:
        for file_path in files_path:
            print(f"Transcribing file: {file_path}")


class DeleteFilesCommand(Command):
    def execute(self, files_path: list[str]) -> None:
        for file_path in files_path:
            print(f"Deleting file: {file_path}")
