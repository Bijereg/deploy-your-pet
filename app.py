import os
from threading import Thread

from controllers.records import records_blueprint
from controllers.scripts import scripts_blueprint
from runner import runner
from scheduling import run_scheduled_tasks
from shared import db, app

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
db.init_app(app)
app.register_blueprint(scripts_blueprint)
app.register_blueprint(records_blueprint)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    runner_thread = Thread(target=runner)
    runner_thread.start()
    scheduler_thread = Thread(target=run_scheduled_tasks)
    scheduler_thread.start()
    app.run()
