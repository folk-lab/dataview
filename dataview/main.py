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
	_main_logger.debug(f'ServeLayout {curPath}')
	# List subfolders in the left column
	
	curDirName = fs.GetDirName(curPath)
	subfolderList = MakeSubDirList(curPath)
	subfolderListObj = html.Ul(id='tree-root-ul', className='tree-root', children=subfolderList)

	# List all the files in the selected folder.
	filesArray = fs.ListFiles(curPath)
	fileListHtml = []
	for fn in filesArray:
		filePath = os.path.join(curDirName, fn)
		if filePath == curPath:
			#fileListHtml.append(html.Li(html.A(fn, href=Encode(filePath)), className='selected'))
			fileListHtml.append(html.Li(dcc.Link(fn, href=Encode(filePath)), className='selected'))
		else:
			# fileListHtml.append(html.Li(html.A(fn, href=Encode(filePath))))
			fileListHtml.append(html.Li(dcc.Link(fn, href=Encode(filePath))))
	fileListHtml = html.Ul(id='file-list', className='file-list', children=fileListHtml)

	if fs.IsPlottable(curPath):
		gd = [ds.get_dataset_menus(fullCurPath),
				html.Div(id='plot-area', children=html.P('Select arrays...'))]
	else:
		gd = [html.Div(id='plot-area', children=html.P('Select a dataset...')), ]

	return [html.Div(id='row-container',
			children=[html.Div(id='tree-div', children=subfolderListObj),
					html.Div(id='file-list-div', children=[fileListHtml]),
					html.Div(id='graph-div', children=gd)])]



# List all subfolders (insteda of making a tree), and add an UP button.
def MakeSubDirList(curDir):
	fs = fsys.FileSystem()
	childArr = []
	lst = fs.ListSubDirs(curDir)
	_main_logger.debug(f'MakeSubDirList: {lst}')
	for subDir in lst:
		_main_logger.debug(f'subfolder: {subDir}')
		dirName = os.path.basename(subDir)
		#childArr.append(html.Li(children=[html.A(dirName, href=Encode(subDir))]))
		childArr.append(html.Li(children=[dcc.Link(dirName, href=Encode(subDir))]))
	return childArr
	
'''
# A recusive function that generates a tree structure
# using <ul> and <li> HTML elements.
def MakeDirTree(curDir, selectedDir):
		if selectedDir == '' or selectedDir == os.path.sep:
				selectedDir = ''
		selected = False
		isOpen = False
		if selectedDir == curDir[:-1]:
			selected = True
		if selectedDir.startswith(curDir[:-1]):
			isOpen = True
		fs = fsys.FileSystem()
		dirName = os.path.basename(curDir[:-1])

		childArr = []
		for subDir in fs.ListSubDirs(curDir):
			childArr.append(MakeDirTree(os.path.join(curDir, subDir), selectedDir))

		if curDir == '':
			dirName = os.path.basename(fs.root)

		liClassName = ''
		if selected:
			liClassName += 'selected '
		if isOpen:
			liClassName += 'open '

		if curDir == '':
			curDir = os.path.sep

		if len(childArr) > 0:
			return html.Li(className=liClassName, children=[
							html.A(dirName, href=Encode(curDir)), html.Ul(children=childArr)
							])
		else:
			return html.Li(className=liClassName, children=[
							html.A(dirName, href=Encode(curDir))
							])
'''
# create app layout
app.layout =  html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-contents', children=ServeLayout(''))])

# This function is called every time a folder name or a file name is clicked.
@app.callback(dash.dependencies.Output('page-contents', 'children'),
				[dash.dependencies.Input('url', 'pathname')])
def ProcessUrl(curPath):

		_main_logger.debug(f'got pathname in process url: {curPath}')

		#if (selected_path is None):
		#	_main_logger.debug('Serving root path')
		#	return ServeLayout('')

		try:
			path = Decode(curPath).lstrip('/')
		except:
			return html.Div('Error decoding the path from the URL.')

		if (path=='') or (path==os.path.sep):
			_main_logger.debug('Serving root path')
			return ServeLayout('')
		else:
			_main_logger.debug(f'Serving: {path}')
			return ServeLayout(path)
