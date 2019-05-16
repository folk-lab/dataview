import os, re
import logging
_ds_logger = logging.getLogger('dataview.dataset')
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import h5py, json
from dataview import app

dropdown_callback_items = []

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
		names = [] # this array will hold the datasets
		def find_datasets(name, h5obj):
			""" this function is called as visititems walks the filetree """
			if type(f[name])==h5py._hl.dataset.Dataset:
				names.append(name)

		f['/'].visititems(find_datasets) # collect list of datasets
		xdefault, ydefault = find_default_arrays(names)
		
		displaynames = []
		for i,n in enumerate(names):
			if not n == xdefault and not n == ydefault:
				displaynames.append(n)
		
		return html.Div(
				[html.Div(id='file-path', children=file_path, style={'display': 'none'}),
				html.Div(id='x-data', children=xdefault, style={'display': 'none'}),
				html.Div(id='y-data', children=ydefault, style={'display': 'none'}),
				html.Div([
					dcc.Dropdown(
						id='data-dropdown',
						options=[{'label':name, 'value':name} for name in displaynames],
						value = displaynames[0],
						clearable=False,),
						],
					className='data-dropdown-div'
				)]
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
	dash.dependencies.Input('x-data', 'children'),
	dash.dependencies.Input('y-data', 'children'),
	dash.dependencies.Input('data-dropdown', 'value')])
def update_plot(fname, xname, yname, dname):
	_ds_logger.debug(f'updating plot: {fname} {xname} {yname} {dname}')
	xtitle = ''
	ytitle = ''

	with h5py.File(fname, 'r') as f: # load file object
		js = json.loads(f['/metadata'].attrs['sweep_logs'])
		# load x and y data
		if xname!='-':
			x = f[xname][:]
			_ds_logger.debug('x.ndim={0} shape={1}'.format(x.ndim, x.shape))
		if yname!='-':
			y = f[yname][:]
			_ds_logger.debug('y.ndim={0} shape={1}'.format(y.ndim, y.shape))

		d = f[dname][:]
		_ds_logger.debug('Data dimensions: {0} shape: {1}'.format(d.ndim, d.shape))
		if d.ndim == 1:
			# Fucking one dimensional!
			try:
				xtitle = js['axis_labels']['x']
			except:
				pass
			return _plot1d(x, d, xtitle=xtitle)
		if d.ndim == 2:
			# Respectfully two dimensional!
			try:
				xtitle=js['axis_labels']['x']
				ytitle=js['axis_labels']['y']
			except:
				pass
			return _plot2d(x, y, d, xtitle=xtitle, ytitle=ytitle)
		
			# # check if these arrays are 1d
			# if (x.ndim==1 or x.shape[0]==1) and (y.ndim==1 or y.shape[0]==1):
				# x = np.ravel(x)
				# y = np.ravel(y)
			# else:
				# return html.P('ShapeError: x and y should be 1d arrays')
		# else:
			# return html.P('MissingDataError: Need both x and y arrays')

		# # load z data
		# if zname=='-':
			# z = None
			# return _plot1d(x, y)
		# else:
			# z = f[zname][:]
			# if (z.ndim==1 or z.shape[0]==1):
				# return _plot1d(x, y, np.ravel(z))
			# elif z.shape[1]==0:
				# return _plot1d(y, np.ravel(z))
			# else:
				# return _plot2d(x,y,z)

def _plot1d(x, d, xtitle=''):
	if not check_data_shapes(x, d):
		return html.P('ShapeError: x and y array shapes not consistent')
	
	data = go.Scatter( x = x, y = d, mode = 'lines')
	graph_elem = dcc.Graph(
		figure={
			'data': [data],
			'layout': go.Layout(
				xaxis={'title': xtitle},
				# yaxis={'title': 'Life Expectancy'},
				# margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
				# legend={'x': 0, 'y': 1},
				hovermode='closest'
			)
		}
	)

	return graph_elem		

def _plot2d(x, y, d, xtitle='', ytitle=''):
	if not check_data_shapes(x, y, z=d):
		return html.P('ShapeError: x, y, and z array shapes not consistent')
		
	data = go.Heatmap(
		x = x,
		y = y,
		z = d,
		colorscale='Viridis',
	)
	graph_elem = dcc.Graph(
		figure={
			'data': [data],
			'layout': go.Layout(
				xaxis={'title': xtitle},
				yaxis={'title': ytitle},
				# margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
				# legend={'x': 0, 'y': 1},
				hovermode='closest'
			)
		}
	)
	return graph_elem

def get_comments(file_path):
	res = []
	with h5py.File(file_path, 'r') as f: # load file object
		try:
			for key, val in dict(f['/metadata'].attrs).items():
				js = json.loads(f['/metadata'].attrs[key])
				for k in js:
					if type(js[k]) == str:
						res.append(html.Tr(children=[html.Td(k), html.Td(js[k])]))
					elif type(js[k]) == dict:
						res.append(html.Tr(children=[html.Td(k), html.Td(json.dumps(js[k]))]))
		except:
			pass
		
	return res