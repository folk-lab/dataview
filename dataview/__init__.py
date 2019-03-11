import os
import logging
from config import config
import dash

LOGGING_LEVEL = logging.DEBUG # set log level
LOG_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# define log file path
if 'LoggingDirectory' in config:
    LOG_FILE = os.path.join(config['LoggingDirectory'], 'dataview.log')
else:
    _init_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
    LOG_FILE = os.path.join(_init_dir, 'logs/dataview.log')

# get logger and handlers
_mod_logger = logging.getLogger('dataview')
_mod_logger.setLevel(LOGGING_LEVEL)
fh = logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8')
fh.setLevel(LOGGING_LEVEL)
fh.setFormatter(LOG_FORMATTER)
_mod_logger.addHandler(fh)

app = dash.Dash(
    __name__,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'http-equiv': 'X-UA-Compatible',
            'content': 'IE=edge'
        },
    ])

app.config.update({
     # remove the default of '/'
     'routes_pathname_prefix': '',

     # remove the default of '/'
     'requests_pathname_prefix': ''
     })

app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.title = 'Data Viewer'
server = app.server

from dataview import main
from dataview import filesystem
from dataview import dataset
