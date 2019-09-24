"""
PDPlatform development configuration.

Adapted from EECS 485, Andrew DeOrio <awdeorio@umich.edu>
"""
import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\xae\x87|E\xe7\xce!\x16x"\xec|\xe1O\xba6cS \x11\xc9\x999\x11'
SESSION_COOKIE_NAME = 'info'

# File Upload to var/uploads/
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'uploads'
)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/PDPlatform.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'main.db'
)