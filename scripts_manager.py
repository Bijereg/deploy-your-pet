import scripts.ping
import scripts.clone_repo
from models.base_script import BaseScript


script_list: list[BaseScript] = [
    # Add your scripts here

    scripts.ping.PingScript(),
    scripts.clone_repo.CloneRepoScript()
]


def get_all_scripts() -> list[BaseScript]:
    return script_list


def get_script_by_internal_name(internal_name: str) -> BaseScript | None:
    found_scripts = [s for s in script_list if s.get_internal_name() == internal_name]
    if len(found_scripts) > 1:
        raise RuntimeError(f"Script with name '{internal_name}' has duplicates")
    if len(found_scripts) == 0:
        return None
    return found_scripts[0]


def search_scripts(search_phrase: str) -> list[BaseScript]:
    return [s for s in script_list
            if search_phrase.lower() in s.get_internal_name().lower()
            or search_phrase.lower() in s.description.lower()]

