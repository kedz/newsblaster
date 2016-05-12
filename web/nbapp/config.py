import os

# Get the current working directory to place sched.db during development.
# In production, use absolute paths or a database management system.
PWD = os.path.abspath(os.curdir)

DEBUG = True

SECRET_KEY = '4840736754news5424579639blaster'  # Create new key. Should not be in repo.
SESSION_PROTECTION = 'strong'
