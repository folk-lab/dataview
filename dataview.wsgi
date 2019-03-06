import sys
import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('/srv/www/dataview/logs/dataview.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.DEBUG)
sys.path.insert(0, '/srv/www/dataview')

activate_this = '/srv/www/dataview/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from dataview import app
app._assets_url_path = 'dataview/assets'
application = app.server
application.logger.addHandler(handler)
