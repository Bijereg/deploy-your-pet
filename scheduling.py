import datetime

import schedule
from sqlalchemy import and_

from config import config
from models.database_record import DatabaseRecord
from shared import app, db


@schedule.repeat(schedule.every(int(config["Scripts"]["ScriptsCheckSeconds"])).seconds)
def kill_scripts_on_timeout():
    app.app_context().push()
    records: list[DatabaseRecord] = DatabaseRecord.query.filter(
        and_(DatabaseRecord.status != "DONE", DatabaseRecord.status != "KILLED", DatabaseRecord.status != "FAILED")
    ).all()
    for record in records:
        time_diff = (datetime.datetime.now() - record.start_ts).total_seconds()
        if time_diff >= int(config["Scripts"]["ScriptsTimeoutSeconds"]):
            record.status = "KILLED"
            db.session.commit()


def run_scheduled_tasks():
    while True:
        schedule.run_pending()
