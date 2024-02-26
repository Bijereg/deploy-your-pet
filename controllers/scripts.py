from flask import Blueprint, render_template, request, abort, redirect

from scripts_manager import get_all_scripts, search_scripts, get_script_by_internal_name
from models.base_script import BaseScript
from models.task import Task
from shared import auth, task_queue

scripts_blueprint = Blueprint('scripts', __name__)


@auth.login_required
def get_scripts_view() -> str:
    search_phrase: str | None = request.args.get("search_phrase")
    if search_phrase:
        scripts: list[BaseScript] = search_scripts(search_phrase)
    else:
        scripts: list[BaseScript] = get_all_scripts()

    return render_template(
        "index.html",
        scripts=scripts
    )


@auth.login_required
def run_script_form(internal_script_name: str) -> str:
    script: BaseScript | None = get_script_by_internal_name(internal_script_name)
    if not script:
        abort(404, "Script not found")
    return render_template(
        "run_script_form.html",
        script=script
    )


@auth.login_required
def run_script_action(internal_script_name: str):
    script: BaseScript | None = get_script_by_internal_name(internal_script_name)
    if not script:
        abort(404, "Script not found")

    data: dict[str, str] = dict()
    for field in script.input_fields:
        field_value: str = request.form[field.name]
        if not field.validate(field_value):
            abort(400, f"Incorrect value for field {field.name}: {field_value}")
        data[field.name] = field_value
    task_queue.put(Task(script, data))
    return redirect(f"/records/script/{script.get_internal_name()}")


scripts_blueprint.route("/", methods=["GET"])(get_scripts_view)
scripts_blueprint.route("/script/run/<string:internal_script_name>", methods=["GET"])(run_script_form)
scripts_blueprint.route("/script/run/<string:internal_script_name>", methods=["POST"])(run_script_action)
