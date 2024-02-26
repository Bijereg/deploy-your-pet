from models.base_script import BaseScript
from models.input_field import InputField, InputTypes
from helpers import os_commands


class PingScript(BaseScript):
    @property
    def description(self) -> str:
        return "Ping"

    @property
    def input_fields(self) -> list[InputField]:
        return [
            InputField("ip_address", "IP address to ping", InputTypes.STRING.value),
            InputField("tries", "Tries count", InputTypes.COUNT.value),
        ]

    def get_stages(self) -> list[callable]:
        return [
            self.start_message,
            self.execute,
            self.end_message
        ]

    @staticmethod
    def start_message(**context) -> str:
        return f"Ping started to {context['ip_address']}"

    @staticmethod
    def execute(**context) -> str:
        return os_commands.shell_command(f"ping -c {context['tries']} {context['ip_address']}")

    @staticmethod
    def end_message(**context) -> str:
        return "Ping ended"
