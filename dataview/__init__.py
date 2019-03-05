import dash

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
        # needed for iframe resizer
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1'
        },
    ])

app.config.update({
     # remove the default of '/'
     'routes_pathname_prefix': '',

     # remove the default of '/'
     'requests_pathname_prefix': ''
     })

app._assets_url_path = 'dataview/assets'
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

app.title = 'Data Viewer'

from dataview import main
from dataview import filesystem
from dataview import dataset
