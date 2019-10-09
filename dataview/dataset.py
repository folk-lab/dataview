import os, re
import logging
_ds_logger = logging.getLogger('dataview.dataset')
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import h5py, json, datetime
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
	#print("Getting dataset menu:", file_path)
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
				[html.Div(id='file-path', children=file_path),  # , style={'display': 'none'}
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
		try:
			js = json.loads(f['/metadata'].attrs['sweep_logs'])
		except:
			js = []
			_ds_logger.debug(f"metadata is empty. Filename = {filename}")

		d = f[dname][:]
		# load x and y data
		if xname!='-':
			x = f[xname][:]
		if yname!='-':
			y = f[yname][:]
		
		
		if d.ndim == 1:
			# Fucking one dimensional!
			try:
				xtitle = json.loads(js['axis_labels'])['x']
			except:
				_ds_logger.debug(f"axis_labels -> x does not exist in metadata. Filename = {filename}")
			_ds_logger.debug(f"XTITLE={xtitle}")
			
			return _plot1d(x, d, xtitle=xtitle)
			
		if d.ndim == 2:
			# Respectfully two dimensional!
			try:
				xtitle=json.loads(js['axis_labels'])['x']
				ytitle=json.loads(js['axis_labels'])['y']
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

def _plot1d(x, d, xtitle='', ytitle=''):
	if not check_data_shapes(x, d):
		return html.P('ShapeError: x and y array shapes not consistent')

	# If the x-axis is time, it needs special treatments.
	print("xtitle", xtitle)
	if xtitle[:4].lower()=='time':
		timediff = x[-1] - x[0]
		
		if timediff < 600:
			tf = '%H:%M:%S'
		elif timediff < 3600*24:
			tf = '%H:%M'
		elif timediff < 3600*24*60:
			tf = '%d/%m %H:%M'
		
		epochcorrection = 2082844800 # This is the number of seconds between 1.1.1904 (Macintosh/Igor time) and 1.1.1970 (UNIX epoch time)
		x = (x - epochcorrection)*1000  # plotly expects epoch time in milliseconds.
		layout = go.Layout(xaxis={ 'title':xtitle, 'type': 'date', 'tickformat': tf}, yaxis={ 'title':ytitle})
	else:
		layout = go.Layout(xaxis={'title':xtitle}, yaxis={ 'title':ytitle})
		#layout = go.Layout(xaxis={})

	data = go.Scatter( x = x, y = d, mode = 'lines')
		
	graph_elem = dcc.Graph(
		figure={
			'data': [data],
			'layout': layout
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
				res.append(html.H2(key))
				js = json.loads(val)
				res.append(html.Pre(json.dumps(js, indent=4).replace('\\"', '').replace('"', '')))
		except Exception as x:
			_ds_logger.debug(f"Probably comments could not be found. Exception: {x}")
			pass
	return res