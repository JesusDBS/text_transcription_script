import wave
import math
import contextlib
import speech_recognition

import utils
import settings

from abc import ABC, abstractmethod
from moviepy import AudioFileClip
from pydub import AudioSegment
from tqdm import tqdm


class TranscriptionService(ABC):
    @abstractmethod
    def transcript(self, filename: str) -> None:
        pass


class GoogleSpeechRecognitionService(TranscriptionService):
    def __init__(self) -> None:
        super().__init__()
        self.transcripted_audio_file_path: str | None = None

    def _set_transcripted_audio_file(self, filename: str) -> None:
        transcripted_audio_file_name = utils.change_filename_extension(
            filename, ".wav")
        self.transcripted_audio_file_path = utils.get_file_path(
            transcripted_audio_file_name, settings.DOWNLOADS_FILE_FOLDER)

    def _write_transcripted_audio_file(self, filename: str, file_type: str) -> None:
        file_path = utils.get_file_path(
            filename, settings.UPLOADS_FILE_FOLDER)

        if file_type.startswith("video"):
            audioclip = AudioFileClip(file_path)
            audioclip.write_audiofile(self.transcripted_audio_file_path)

        elif file_type.startswith("audio") and filename.endswith(".mp3"):
            audioclip = AudioSegment.from_mp3(file_path)
            audioclip.export(self.transcripted_audio_file_path, format="wav")

    def _compute_total_duration(self) -> int:
        if self.transcripted_audio_file_path is None:
            raise ValueError("Transcripted audio file path is not set.")

        with contextlib.closing(wave.open(self.transcripted_audio_file_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        total_duration = math.ceil(
            duration / settings.TRANSCRIPTION_CHUNK_DURATION)

        return total_duration

    def _transcript(self, total_duration: int) -> None:
        """Transcribes the audio file in chunks and writes the transcription to a text file.

        Args:
            total_duration (int): Total duration of the audio file in minutes.
        """
        if self.transcripted_audio_file_path is None:
            raise ValueError("Transcripted audio file path is not set.")

        recognizer = speech_recognition.Recognizer()
        for record_chunck in tqdm(range(0, total_duration), desc="Transcribing audio file"):
            with speech_recognition.AudioFile(self.transcripted_audio_file_path) as source:
                audio = recognizer.record(
                    source, offset=record_chunck*settings.TRANSCRIPTION_CHUNK_DURATION,
                    duration=settings.TRANSCRIPTION_CHUNK_DURATION
                )

            transcription_file = utils.change_filename_extension(
                self.transcripted_audio_file_path, ".txt"
            )
            with open(transcription_file, "a") as f:
                f.write(recognizer.recognize_google(audio))
                f.write(" ")

    def transcript(self, filename: str) -> None:
        file_type = utils.get_file_type(filename)
        if file_type is not None:
            print(f"Transcribing file: {filename}")
            self._set_transcripted_audio_file(filename)
            self._write_transcripted_audio_file(filename, file_type)
            total_duration = self._compute_total_duration()
            self._transcript(total_duration)
            print("Transcription complete!")


def delete_service(filename: str) -> None:
    # TODO: Implement delete service
    pass
