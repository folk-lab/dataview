#!/usr/bin/python3
import dash

app = dash.Dash(__name__)
app.title='Data Viewer'

app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
