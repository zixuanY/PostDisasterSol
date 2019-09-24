"""
Connection Platform package initializer.

"""
import flask

app = flask.Flask(__name__)  # pylint: disable=invalid-name
app.app_context().push()

# Read settings from config module (PDPlatform/config.py)
app.config.from_object('PDPlatform.config')

# Overlay settings read from file specified by environment variable. This is
# useful for using different on development and production machines.
# Reference: http://flask.pocoo.org/docs/config/
app.config.from_envvar('PDPLATFORM_SETTINGS', silent=True)  # TODO: where is it?

# Tell our app about views and model.  This is dangerously close to a
# circular import, which is naughty, but Flask was designed that way.
# (Reference http://flask.pocoo.org/docs/patterns/packages/)  We're
# going to tell pylint and pycodestyle to ignore this coding style violation.
import PDPlatform.views  # noqa: E402  pylint: disable=wrong-import-position
import PDPlatform.model  # noqa: E402  pylint: disable=wrong-import-position
