from models.base_script import BaseScript
from models.input_field import InputField, InputTypes
from helpers import git


class CloneRepoScript(BaseScript):
    @property
    def description(self) -> str:
        return "Clone a repository"

    @property
    def input_fields(self) -> list[InputField]:
        return [
            InputField("repo", "Repository url", InputTypes.STRING.value),
            InputField("dir", "Where to clone", InputTypes.STRING.value),
        ]

    def get_stages(self) -> list[callable]:
        return [
            self.prepare,
            self.clone
        ]

    @staticmethod
    def prepare(**context) -> str:
        return f"Start cloning repo {context['repo']} into {context['dir']}"

    @staticmethod
    def clone(**context) -> str:
        return git.clone(context["repo"], context["dir"])
