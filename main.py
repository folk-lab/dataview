#!/usr/bin/python3
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import send_from_directory
import os

import layout
from config import config

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

layout.CreateLayout(app)

if __name__ == '__main__':
	app.run_server(debug=True)


