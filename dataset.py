import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import h5py
import os

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

# only supports hdf5 files (for now, at least)
class Dataset:

	def __init__(self, file_path):
		self.f = h5py.File(file_path, 'r') # load file object

		# find all datasets in hdf5 tree
		self.names = ['-'] # this array will hold the datasets
		def find_datasets(name, h5obj):
			""" this function is called as visititems walks the filetree """
			if type(self.f[name])==h5py._hl.dataset.Dataset:
				self.names.append(name)

		self.f['/'].visititems(find_datasets) # collect list of datasets
		self.xdefault, self.ydefault = find_default_arrays(self.names)
		self.zdefault = '-'
		print(self.xdefault, self.ydefault, self.zdefault)

	def plot(self, xname, yname, zname, **kwargs):

		x = self.f[xname][:]
		y = self.f[yname][:]
		if zname=='-':
			# 2d plot
			z = self.f[zname][:]
			# self._plot2d(self, x, y, z, **kwargs)
			return html.Div(xname, yname, zname)
		else:
			#1d plot
			self._plot1d(self, x, y, **kwargs)
			return html.Div(xname, yname)

	def _plot1d(self, x, y, **kwargs):
		return html.Div('no 1d plot available yet')

	def _plot2d(self, x, y, z, **kwargs):
		return html.Div('no 1d plot available yet')
