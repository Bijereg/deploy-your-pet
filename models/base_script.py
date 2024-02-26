from abc import ABC, abstractmethod

from models.input_field import InputField


class BaseScript(ABC):

    def get_internal_name(self) -> str:
        return self.__class__.__name__

    @property
    @abstractmethod
    def description(self) -> str:
        raise NotImplementedError("Script must have a description")

    @property
    @abstractmethod
    def input_fields(self) -> list[InputField]:
        raise NotImplementedError("Script must have input fields")

    @abstractmethod
    def get_stages(self) -> list[callable]:
        raise NotImplementedError("Script must implement stages")
