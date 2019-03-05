import sys
sys.path.insert(0, '/srv/www/dataview')

activate_this = '/srv/www/dateview/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from dataview import app as application
