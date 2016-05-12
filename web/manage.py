from flask.ext.script import Manager, Server
from nbapp.app import app

manager = Manager(app)
app.config['DEBUG'] = True  # Ensure debugger will load.
#manager.add_command("runserver", Server(host="0.0.0.0",port=5000))
manager.add_command("runserver", Server())


if __name__ == '__main__':  # pragma: no cover
    manager.run()
