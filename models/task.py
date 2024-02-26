from models.base_script import BaseScript


class Task:
    def __init__(self, script: BaseScript, parameters: dict[str, str]):
        self.script = script
        self.parameters = parameters
