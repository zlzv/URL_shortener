import datetime
from app import db, bcrypt
from sqlalchemy import event, DDL


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    registered_at = db.Column(db.DateTime, nullable=False)
    urls = db.relationship('Url')

    def __init__(self, password, username):
        self.password = bcrypt.generate_password_hash(password)
        self.username = username
        self.registered_at = datetime.datetime.now()

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    views = db.Column(db.Integer, default=0)

    def __init__(self, user_id, url):
        self.url = url
        self.user_id = user_id
        self.created_at = datetime.datetime.now()

    def __repr__(self):
        return '<Url {0}>'.format(self.url)


#
# Required for setting initial value of auto_increment
#
event.listen(
    User.__table__,
    "after_create",
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10000;")
)


event.listen(
    Url.__table__,
    "after_create",
    DDL("ALTER TABLE %(table)s AUTO_INCREMENT = 10000;")
)