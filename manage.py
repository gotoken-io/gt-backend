import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import blueprint
from app.main import create_app, db

# 新添加的 model, 需要在此引入, 这样 flask db migrate 才能识别到
from app.main.model import user, blacklist, proposal, comment

from app.fix_db.db_script import DbScript

app = create_app(os.getenv('GT_BACKEND_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def run():
    app.run("0.0.0.0", 5000)


@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def fix_db():
    # DbScript.add_init_create_log()
    # DbScript.set_all_proposal_status_none()
    DbScript.del_logs_update_status_double()


if __name__ == '__main__':
    manager.run()
