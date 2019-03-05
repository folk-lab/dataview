import dash

app_prefix = ''

#app = dash.Dash(__name__)
app = dash.Dash(
    __name__,
    url_base_pathname=app_prefix + '/',
    assets_url_path=app_prefix + '/assets',
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
app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

title = 'Data Viewer'

app.title = title

# app.config.update({
#     # remove the default of '/'
#     'routes_pathname_prefix': '',
#
#     # remove the default of '/'
#     'requests_pathname_prefix': ''
# })

from dataview import main
from dataview import filesystem
from dataview import dataset
