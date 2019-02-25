import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import filesystem
import base64

from config import config
from plot import Plot

def CreateLayout(app):	
	app.layout =  html.Div([
		dcc.Location(id='url', refresh=False),
		html.Div(id='page-contents', children=ServeLayout(''))])
	
	# This function is called every time a folder name or a file name is clicked.
	@app.callback(dash.dependencies.Output('page-contents', 'children'),
		[dash.dependencies.Input('url', 'pathname')])
	def ProcessUrl(selectedPath):
		if selectedPath is None:
			return ServeLayout('')
		else:
			return ServeLayout(Decode(selectedPath[1:]))

def ServeLayout(selectedPath):
	# Create a folder tree
	selectedDir = os.path.dirname(selectedPath)
	tree = MakeDirTree('', selectedDir)
	treeObj = html.Ul(id='tree-root-ul', className='tree-root', children=tree)

	# List all the files in the selected folder.	
	fs = filesystem.FileSystem()
	filesArray = fs.ListFiles(selectedDir)
	fileListHtml = []
	for fn in filesArray:
		filePath = os.path.join(selectedDir, fn)
		if filePath == selectedPath:
			fileListHtml.append(html.Li(html.A(fn, href=Encode(filePath)), className='selected'))
		else:
			fileListHtml.append(html.Li(html.A(fn, href=Encode(filePath))))
	fileListHtml = html.Ul(id='file-list', className='file-list', children=fileListHtml)

	# If a file is selected, plot it.
	if fs.IsFile(selectedPath):
		plot = Plot(fs.FullPath(selectedPath))
	else:
		plot = html.Div('')

	return [html.Div(id='row-container',
			children=[html.Div(id='tree-div', children=treeObj),
			html.Div(id='file-list-div', children=[fileListHtml]),
			html.Div(id='graph-div', children=[plot])])]


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
	fs = filesystem.FileSystem()
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

# Encode the folder and file names into something that
# can safely be included in a URL.
def Encode(s):
	return base64.b64encode(bytes(s, 'utf-8')).decode('UTF-8','ignore')
	
def Decode(n):
	return base64.b64decode(n).decode('UTF-8','ignore')

