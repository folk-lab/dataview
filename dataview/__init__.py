import dash

app = dash.Dash(__name__)
app.title='Data Viewer'

app.config.requests_pathname_prefix = ''
app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

from dataview import main
from dataview import filesystem
from dataview import dataset
