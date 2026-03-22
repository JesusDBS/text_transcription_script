import os
import wave
import math
import contextlib
import speech_recognition
import utils
import settings as s

from abc import ABC, abstractmethod
from moviepy import AudioFileClip
from pydub import AudioSegment
from tqdm import tqdm
from enum import StrEnum, auto


class TranscriptionService(ABC):
    @abstractmethod
    def transcript(self, filename: str) -> None:
        pass


class GoogleSpeechRecognitionService(TranscriptionService):
    def __init__(self) -> None:
        super().__init__()
        self.transcripted_audio_file_path: str | None = None

    def _set_transcripted_audio_file_path(self, filename: str) -> None:
        transcripted_audio_file_name = utils.change_filename_extension(
            filename, ".wav")
        self.transcripted_audio_file_path = utils.get_file_path(
            transcripted_audio_file_name, s.DOWNLOADS_FILE_FOLDER)

    def _create_transcripted_audio_file(self, filename: str, file_type: str) -> None:
        file_path = utils.get_file_path(
            filename, s.UPLOADS_FILE_FOLDER)

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
            duration / s.TRANSCRIPTION_CHUNK_DURATION)

        return total_duration

    def _transcript(self, total_duration: int) -> None:
        """Transcribes the audio file in chunks and writes the transcription to a text file.

        Args:
            total_duration (int): Total duration of the audio file in minutes.
        """
        if self.transcripted_audio_file_path is None:
            raise ValueError("Transcripted audio file path is not set.")

        recognizer = speech_recognition.Recognizer()
        transcription_file = utils.change_filename_extension(
            self.transcripted_audio_file_path, ".txt"
        )

        def get_transcription_range() -> tqdm:
            return tqdm(range(0, total_duration), desc="Transcribing audio file")

        def get_audio_file() -> speech_recognition.AudioFile:
            return speech_recognition.AudioFile(self.transcripted_audio_file_path)

        def get_offset(record_chunck: int) -> int:
            return record_chunck * s.TRANSCRIPTION_CHUNK_DURATION

        def save_transcription_in_file(audio: speech_recognition.AudioData) -> None:
            try:
                with open(transcription_file, "a") as f:
                    f.write(recognizer.recognize_google(
                        audio, language=s.RECOGNIZE_GOOGLE_LANGUAGE))
                    f.write(" ")
            except speech_recognition.UnknownValueError:
                pass

        for record_chunck in get_transcription_range():
            with get_audio_file() as source:
                audio = recognizer.record(
                    source, offset=get_offset(record_chunck),
                    duration=s.TRANSCRIPTION_CHUNK_DURATION
                )
            save_transcription_in_file(audio)

    def transcript(self, filename: str) -> None:
        file_type = utils.get_file_type(filename)
        if file_type is not None:
            try:
                print(f"Transcribing file: {filename}")
                self._set_transcripted_audio_file_path(filename)
                self._create_transcripted_audio_file(filename, file_type)
                total_duration = self._compute_total_duration()
                self._transcript(total_duration)
                print("Transcription complete!")
            except Exception as e:
                print(f"Error transcribing {filename}: {e}")
                raise


class TranscriptionServiceBackends(StrEnum):
    GOOGLE_SPEECH_RECOGNITION = auto()


TRANSCRIPTION_SERVICE_BACKENDS_MAPPER: dict[str, type[TranscriptionService]] = {
    TranscriptionServiceBackends.GOOGLE_SPEECH_RECOGNITION.value: GoogleSpeechRecognitionService
}


def set_transcript_service(active_transcript_backend: str) -> TranscriptionService:
    if active_transcript_backend not in TRANSCRIPTION_SERVICE_BACKENDS_MAPPER.keys():
        raise KeyError(
            f"{active_transcript_backend} is not an available backend")

    transcript_service = TRANSCRIPTION_SERVICE_BACKENDS_MAPPER[active_transcript_backend]
    return transcript_service()


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
