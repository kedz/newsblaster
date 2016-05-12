import os

# Get the current working directory to place sched.db during development.
# In production, use absolute paths or a database management system.
PWD = os.path.abspath(os.curdir)

DEBUG = True

SECRET_KEY = 'secret222'  # Create your own.
SESSION_PROTECTION = 'strong'
