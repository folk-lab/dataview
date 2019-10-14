import os
import logging
_main_logger = logging.getLogger('dataview.main')
from urllib.parse import quote_plus, unquote_plus
import dash
import dash_core_components as dcc
import dash_html_components as html

from dataview import config
from dataview import filesystem as fsys
from dataview import dataset as ds
from dataview import app

# Encode the folder and file names into something that
# can safely be included in a URL.
def Encode(s):
	return quote_plus(s)

def Decode(n):
	return unquote_plus(n)

def ServeLayout(curPath):
	fs = fsys.FileSystem()
	fullCurPath = fs.FullPath(curPath)
	# List subfolders in the left column
	
	curDirName = fs.GetDirName(curPath)
	subfolderList = MakeSubDirList(curPath)
	subfolderListObj = html.Ul(id='dir-root-ul', className='dir-root', children=subfolderList)

	# List all the files in the selected folder.
	filesArray = fs.ListFiles(curPath)
	fileListHtml = []
	for fn in filesArray:
		filePath = os.path.join(curDirName, fn)
		if filePath == curPath:
			fileListHtml.append(html.Li(dcc.Link(fn, href=Encode(filePath)), className='selected'))
		else:
			fileListHtml.append(html.Li(dcc.Link(fn, href=Encode(filePath))))
	fileListHtml = html.Ul(id='file-list', className='file-list', children=fileListHtml)
	
	gd = ""
	
	if fs.IsPlottable(curPath):
		_, item_type = os.path.splitext(curPath)
		
		print("Item Type:", item_type)
		if item_type == ".h5" or item_type == ".hdf5":
			gd = display_h5(fullCurPath)

	else:
		gd = [html.Div(id='plot-area', children=html.P('Select a dataset...'))]

	return [html.Div(id='row-container',
			children=[
					html.Div(id='dir-list-div', children=subfolderListObj),
					html.Div(id='file-list-div', children=[fileListHtml]),
					html.Div(id='graph-div', children=gd)])]

def display_h5(fullCurPath):
	gd = [ds.get_dataset_menus(fullCurPath),
		html.Div(id='plot-area', children=html.P('Select arrays...')),
		html.Div(id='display-file-path', children="File name: " + fullCurPath[len(config['LocalRootDirectory']):]),
		html.Div(className='comments', children=ds.get_comments(fullCurPath))]
	return gd
	

# List all subfolders (insteda of making a tree), and add an UP button.
def MakeSubDirList(d):
	fs = fsys.FileSystem()
	
	childArr = []
	dirName = fs.GetDirName(d)
	parentDir = fs.GetParentDir(d)
	if d != '' and dirName != '':
		childArr.append(html.Li(className='up', children=dcc.Link('..', parentDir)))
	
	lst = fs.ListSubDirs(d)
	for subDir in lst:
		dirName = os.path.basename(subDir)
		#childArr.append(html.Li(children=[html.A(dirName, href=Encode(subDir))]))
		childArr.append(html.Li(children=[dcc.Link(dirName, href=Encode(subDir))]))
	return childArr
	
	
# create app layout
app.layout =  html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-contents', children=ServeLayout(''))])

# This function is called every time a folder name or a file name is clicked.
@app.callback(dash.dependencies.Output('page-contents', 'children'),
				[dash.dependencies.Input('url', 'pathname')])
def ProcessUrl(curPath):
	try:
		path = Decode(curPath).lstrip('/')
	except:
		return html.Div('Error decoding the path from the URL.')

	if (path=='') or (path==os.path.sep):
		return ServeLayout('')
	else:
		return ServeLayout(path)
