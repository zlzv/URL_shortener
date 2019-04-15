from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.models import User


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    db.create_all()


@manager.command
def drop_db():
    db.drop_all()


@manager.command
def create_admin():
    db.session.add(User(username='admin', password='admin'))
    db.session.commit()


if __name__ == '__main__':
    manager.run()