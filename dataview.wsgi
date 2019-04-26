import os
import sys

app_root = '/srv/www/dataview'
sys.path.insert(0, app_root)

activate_this = os.path.join(app_root,'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from dataview import app

app._assets_url_path = 'dataview/assets'
application = app.server
