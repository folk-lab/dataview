import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import h5py
import os
from app import app

def find_default_arrays(name_list):
	endings = ['','data','array','arr','_data', '_array','_arr']
	x_choices = ['x'+end for end in endings]
	y_choices = ['y'+end for end in endings]

	xname = None
	yname = None
	for n in name_list:
		if not xname and (n in x_choices):
			xname = n
		elif not yname and (n in y_choices):
			yname = n

	if not xname:
		xname = '-'
	if not yname:
		yname = '-'
	return xname, yname

def get_dataset_menus(file_path):

	with h5py.File(file_path, 'r') as f: # load file object

		# find all datasets in hdf5 tree
		names = ['-'] # this array will hold the datasets
		def find_datasets(name, h5obj):
			""" this function is called as visititems walks the filetree """
			if type(f[name])==h5py._hl.dataset.Dataset:
				names.append(name)

		f['/'].visititems(find_datasets) # collect list of datasets
		xdefault, ydefault = find_default_arrays(names)
		zdefault = '-'

		return html.Div(
		       [html.Div(id='file-path', children=file_path, style={'display': 'none'}),
		        html.Div([
		        dcc.Dropdown(
		            id='x-dropdown',
		            options=[{'label':name, 'value':name} for name in names],
		            value = xdefault,
					clearable=False,),
		            ],
				style={'width': '19%', 'margin-left': '0', 'margin-right': '0.5%', 'display': 'inline-block'}
				),
		        html.Div([
		        dcc.Dropdown(
		            id='y-dropdown',
					options=[{'label':name, 'value':name} for name in names],
		            value = ydefault,
					clearable=False,),
		            ],
				style={'width': '19%', 'margin-left': '0.5%', 'margin-right': '0.5%', 'display': 'inline-block'}
				),
				html.Div([
		        dcc.Dropdown(
		            id='z-dropdown',
					options=[{'label':name, 'value':name} for name in names],
		            value = zdefault,
					clearable=False,),
		            ],
				style={'width': '19%', 'margin-left': '0.5%', 'margin-right': '0', 'display': 'inline-block'}
				),
		    ],
		)

@app.callback(dash.dependencies.Output('plot-area', 'children'),
	[dash.dependencies.Input('file-path', 'children'),
	 dash.dependencies.Input('x-dropdown', 'value'),
	 dash.dependencies.Input('y-dropdown', 'value'),
	 dash.dependencies.Input('z-dropdown', 'value')])
def update_plot(fname, xname, yname, zname):
	return html.P(f'{fname}: {xname}, {yname}, {zname}')

def _plot1d(x, y, **kwargs):
	return html.Div('no 1d plot available yet')

def _plot2d(x, y, z, **kwargs):
	return html.Div('no 1d plot available yet')

	# with h5py.File(file_path, 'r') as f: # load file object
		# return f'array(s) changed! {xname}, {yname}, {zname}'
