import os

import settings
import utils

from commands import Command, commands
from cli import get_option, get_filename

OPTIONS_MAPPER: dict[str, Command] = {
    settings.Options.TRANS.value: commands.TranscriptFilesCommand(),
    settings.Options.DELETE.value: commands.DeleteFilesCommand()
}


def main():
    option = OPTIONS_MAPPER.get(get_option(), None)
    if option is not None:
        option.execute(get_filename())


if __name__ == "__main__":
    main()
