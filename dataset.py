import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import h5py
import os, re
from app import app

def find_default_arrays(name_list):
	endings = ['','data','array','arr','_data', '_array','_arr']

	xname = None
	yname = None
	for n in name_list:
		for end in endings:
			seq = re.compile(f'(\w+/)*([xy]){end}$')
			m = re.match(seq, n)
			if m:
				if m.group(2)=='x' and not xname:
					xname = n
					break
				if  m.group(2)=='y' and not yname:
					yname = n
					break
			if xname and yname:
				return xname, yname

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

def check_data_shapes(x, y, z=None):

	# now check the shape of everything
	if z is None:
		if len(x)==len(y):
			return True
	else:
		if z.shape==(len(y),len(x)):
			return True
	return False

@app.callback(dash.dependencies.Output('plot-area', 'children'),
	[dash.dependencies.Input('file-path', 'children'),
	 dash.dependencies.Input('x-dropdown', 'value'),
	 dash.dependencies.Input('y-dropdown', 'value'),
	 dash.dependencies.Input('z-dropdown', 'value')])
def update_plot(fname, xname, yname, zname):
	with h5py.File(fname, 'r') as f: # load file object

		# load x and y data
		if xname!='-' and yname!='-':
			x = f[xname][:]
			y = f[yname][:]

			# check if these arrays are 1d
			if (x.ndim==1 or x.shape[0]==1) and (y.ndim==1 or y.shape[0]==1):
				x = np.ravel(x)
				y = np.ravel(y)
			else:
				return html.P('ShapeError: x and y should be 1d arrays')
		else:
			return html.P('MissingDataError: Need both x and y arrays')

		# load z data
		if zname=='-':
			z = None
			return _plot1d(x, y)
		else:
			z = f[zname][:]
			if (z.ndim==1 or z.shape[0]==1):
				return _plot1d(x, np.ravel(z))
			elif z.shape[1]==0:
				return _plot1d(y, np.ravel(z))
			else:
				return _plot2d(x,y,z)


def _plot1d(x, y, **kwargs):

	if check_data_shapes(x, y, z=None):

		data = go.Scatter(
			x = x,
			y = y,
			mode = 'lines',
		)

		graph_elem = dcc.Graph(
	        figure={
	            'data': [data],
	            'layout': go.Layout(
	            #     xaxis={'type': 'log', 'title': 'GDP Per Capita'},
	            #     yaxis={'title': 'Life Expectancy'},
	            #     margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
	            #     legend={'x': 0, 'y': 1},
	                hovermode='closest'
	            )
	        }
	    )

		return graph_elem
	else:
		return html.P('ShapeError: x and y array shapes not consistent')

def _plot2d(x, y, z, **kwargs):

	if check_data_shapes(x, y, z=z):

		data = go.Heatmap(
			z = z,
			x = x,
			y = y,
			colorscale='Viridis',
		)

		graph_elem = dcc.Graph(
	        figure={
	            'data': [data],
	            'layout': go.Layout(
	            #     xaxis={'type': 'log', 'title': 'GDP Per Capita'},
	            #     yaxis={'title': 'Life Expectancy'},
	            #     margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
	            #     legend={'x': 0, 'y': 1},
	                hovermode='closest'
	            )
	        }
	    )
		
		return graph_elem
	else:
		return html.P('ShapeError: x, y, and z array shapes not consistent')
