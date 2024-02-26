import subprocess


def shell_command(command: str, timeout: float = 60) -> str:
    result = subprocess.check_output(
        command,
        shell=True,
        text=True,
        stderr=subprocess.STDOUT,
        timeout=timeout
    )
    return result
