#!/usr/bin/python3
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import send_from_directory
import os

import layout
from config import config

#class CustomDash(dash.Dash):
#	def interpolate_index(self, **kwargs):
#		return layout.HtmlString(kwargs)	

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

layout.CreateLayout(app)

"""
# Update the list of files
@app.callback(
	Output(component_id='file-list-div', component_property='children'),
	[Input(component_id='tree-root', component_property='value')])
def UpdateFileList(input_value):
	return 'You\'ve entered "{}"'.format(input_value)
"""

if __name__ == '__main__':
	app.run_server(debug=True)


