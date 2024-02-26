import datetime
import json
from flask import Blueprint, render_template, redirect, Response

from models.base_script import BaseScript
from models.database_record import DatabaseRecord
from models.task import Task
from scripts_manager import get_script_by_internal_name
from shared import auth, task_queue, db

records_blueprint = Blueprint('records', __name__)


@auth.login_required
def all_records():
    records: list[DatabaseRecord] = (DatabaseRecord.query
                                     .order_by(DatabaseRecord.start_ts.desc())
                                     .limit(100))
    return render_template(
        "records_list.html",
        records=records,
        now=datetime.datetime.now()
    )


@auth.login_required
def records_by_script(internal_script_name: str) -> str:
    records: list[DatabaseRecord] = (DatabaseRecord.query
                                     .filter_by(internal_script_name=internal_script_name)
                                     .order_by(DatabaseRecord.start_ts.desc())
                                     .limit(100)
                                     .all())
    return render_template(
        "records_list.html",
        records=records,
        now=datetime.datetime.now()
    )


@auth.login_required
def record_detail_view(record_id: int) -> str:
    record: DatabaseRecord = (DatabaseRecord.query
                              .filter_by(id=record_id)
                              .first_or_404())
    return render_template(
        "record_detail_view.html",
        record=record
    )


@auth.login_required
def restart_record(record_id: int) -> Response:
    record: DatabaseRecord = (DatabaseRecord.query
                              .filter_by(id=record_id)
                              .first_or_404())
    script: BaseScript = get_script_by_internal_name(record.internal_script_name)
    task_queue.put(Task(script, json.loads(record.parameters)))
    return redirect(f"/records/script/{script.get_internal_name()}")


@auth.login_required
def kill_record(record_id: int) -> Response:
    record: DatabaseRecord = (DatabaseRecord.query
                              .filter_by(id=record_id)
                              .first_or_404())
    if not (record.status == "DONE" or record.status == "FAILED" or record.status == "KILLED"):
        record.status = "KILLED"
        db.session.commit()
    return redirect(f"/records/details/{record.id}")


records_blueprint.route("/records", methods=["GET"])(all_records)
records_blueprint.route("/records/script/<string:internal_script_name>", methods=["GET"])(records_by_script)
records_blueprint.route("/records/details/<int:record_id>", methods=["GET"])(record_detail_view)
records_blueprint.route("/records/restart/<int:record_id>", methods=["POST"])(restart_record)
records_blueprint.route("/records/kill/<int:record_id>", methods=["POST"])(kill_record)
