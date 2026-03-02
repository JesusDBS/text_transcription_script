import os
from argparse import ArgumentParser

from settings import ALLOWED_CLI_OPTIONS, UPLOADS_FILE_FOLDER, DOWNLOADS_FILE_FOLDER
from utils import allowed_file, get_file_path


parser = ArgumentParser(
    prog='Text Trsanscription Script',
    description='Converts audio and video files to text using the Google Speech Recognition API.')

parser.add_argument('-o', '--option', type=str, choices=ALLOWED_CLI_OPTIONS, required=True,
                    help="Option to execute, it can be 'trans' to transcribe a single file or 'delete' to delete a file from the uploads folder")
parser.add_argument('-f', '--filename', type=str, action="extend", nargs="+",
                    help="Filename, it can be a video or audio file stored in the uploads folder.")
parser.add_argument('-d', '--directory', type=str, choices=[
                    UPLOADS_FILE_FOLDER, DOWNLOADS_FILE_FOLDER], help="Directory to delete files from, it can be 'uploads' or 'downloads'.")
# TODO add a parser for the language of the transcription, for example with the option -l or --language


def get_option(parser: ArgumentParser = parser) -> str:
    """
    Parses the command line arguments and returns the option to execute.

    Parameters
    ----------
    parser : ArgumentParser
        ArgumentParser object to parse the command line arguments.

    Returns
    -------
    str
        Option to execute.
    """
    args = parser.parse_args()
    return args.option


def _get_files_from_directory(directory: str) -> list[str]:
    """
    Returns a list of files in the specified directory.

    Parameters
    ----------
    directory : str
        Directory to get files from.

    Returns
    -------
    list[str]
        List of files path in the specified directory.
    """
    files = os.listdir(directory)
    if ".gitignore" in files:
        files.remove(".gitignore")

    files = list(map(lambda file: get_file_path(file, directory), files))
    return files


def get_filename(parser: ArgumentParser = parser) -> list[str] | None:
    """
    Parses the command line arguments and returns the list of filenames to process.

    Parameters
    ----------
    parser : ArgumentParser
        ArgumentParser object to parse the command line arguments.

    Returns
    -------
    list[str] | None
        Filenames to process, or None if no filename was provided.
    """

    filenames = parser.parse_args().filename
    if filenames is not None:
        for filename in filenames:
            if not allowed_file(filename):
                raise ValueError(f"File format not allowed: {filename}")

        return filenames

    directory = parser.parse_args().directory
    if directory is not None:
        filenames = _get_files_from_directory(directory)

    return filenames
