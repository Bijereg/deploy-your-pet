import os

from helpers import os_commands


def clone(git_url: str, directory: str) -> str:
    os.rmdir(directory)
    os.mkdir(directory)
    os.chdir(directory)
    return os_commands.shell_command(f"git clone {git_url}")
