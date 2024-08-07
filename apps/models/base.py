from exts import db
from datetime import datetime


class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(db.DateTime, default=datetime.now())
    is_delete = db.Column(db.Boolean, default=False)
