from shared import db


class DatabaseRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    internal_script_name = db.Column(db.String(255))
    parameters = db.Column(db.String(255))
    start_ts = db.Column(db.DateTime, default=None)
    end_ts = db.Column(db.DateTime, default=None)
    status = db.Column(db.String(255))
    output_text = db.Column(db.Text)

    def __repr__(self):
        return f'<DatabaseRecord {self.internal_script_name | self.start_ts | self.status}>'
