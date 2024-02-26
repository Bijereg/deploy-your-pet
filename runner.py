import datetime
import json
import subprocess

from models.base_script import BaseScript
from models.database_record import DatabaseRecord
from models.task import Task
from shared import app, task_queue, db


def runner():
    app.app_context().push()
    while True:
        task: Task = task_queue.get()
        script: BaseScript = task.script
        parameters: dict[str, str] = task.parameters

        record: DatabaseRecord = DatabaseRecord(
            internal_script_name=script.get_internal_name(),
            parameters=json.dumps(parameters),
            start_ts=datetime.datetime.now(),
            end_ts=None,
            status="PREPARED",
            output_text=""
        )

        db.session.add(record)
        db.session.commit()

        stages: list[callable] = script.get_stages()
        success_flag = True
        for stage in stages:
            # Get actual state on each stage
            record: DatabaseRecord = DatabaseRecord.query.filter_by(id=record.id).first()

            # Don't execute killed scripts
            if record.status == "KILLED":
                break

            record.status = stage.__name__
            db.session.commit()
            try:
                output = stage.__call__(**parameters)
                record.output_text += output + "\n"
                db.session.commit()
            except subprocess.CalledProcessError as e:
                record.output_text += "Status code: " + str(e.returncode) + "\n" + "\n"
                record.output_text += e.output + "\n"
                record.end_ts = datetime.datetime.now()
                db.session.commit()
                success_flag = False
                break
            except Exception as e:
                record.output_text += str(e) + "\n"
                record.end_ts = datetime.datetime.now()
                db.session.commit()
                success_flag = False
                break

        if record.status != "KILLED":
            if success_flag:
                record.status = "DONE"
            else:
                record.status = "FAILED"
        record.end_ts = datetime.datetime.now()
        db.session.commit()
