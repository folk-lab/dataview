import os
import sys
from config import config

app_root = os.path.join(config['ApplicationDirectory'])
sys.path.insert(0, app_root)

activate_this = os.path.join(app_root,'venv/bin/activate_this.py')
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from dataview import app
app._assets_url_path = 'dataview/assets'
application = app.server
application.logger.addHandler(handler)
