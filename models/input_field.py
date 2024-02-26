from enum import Enum
from typing import Any


class InputType:
    def __init__(self, html_input_type: str, validation_method: callable):
        self.html_input_type = html_input_type
        self.validation_method = validation_method


class InputTypes(Enum):
    STRING = InputType("text",
                       lambda s: True)
    NUMBER = InputType("number",
                       lambda s: s.isnumeric())
    COUNT = InputType("number",
                      lambda s: s.isnumeric() and int(s) >= 0)


class InputField:
    def __init__(self, name: str, description: str, input_type: InputType):
        self.name = name
        self.description = description
        self.input_type = input_type

    def validate(self, value: Any) -> bool:
        return self.input_type.validation_method.__call__(value)
