import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import filesystem
import base64

from config import config

def CreateLayout(app):	
	app.layout =  html.Div([
		dcc.Location(id='url', refresh=False),
		html.Div(id='page-contents', children=ServeLayout(''))])
	
	@app.callback(dash.dependencies.Output('page-contents', 'children'),
		[dash.dependencies.Input('url', 'pathname')])
	def ProcessUrl(selectedPath):
		if selectedPath is None:
			return ServeLayout('')
		else:
			return ServeLayout(Decode(selectedPath[1:]))

def ServeLayout(selectedPath):
	selectedDir = os.path.dirname(selectedPath) + os.path.sep
	tree = MakeDirTree('', selectedDir)
	treeObj = html.Ul(id='tree-root-ul', className='tree-root', children=tree)
	
	fs = filesystem.FileSystem()
	print("SELECTED PATH", selectedPath)
	filesArray = fs.ListFiles(selectedDir)
	fileListHtml = []
	for fn in filesArray:
		filePath = os.path.join(selectedDir, fn)
		if filePath == selectedPath:
			fileListHtml.append(html.Li(html.A(fn, href=Encode(filePath)), className='selected'))
		else:
			fileListHtml.append(html.Li(html.A(fn, href=Encode(filePath))))
	fileListHtml = html.Ul(id='file-list', className='file-list-ul', children=fileListHtml)
	
	return [html.Div(id='row-container',
			children=[html.Div(id='tree-div', children=treeObj),
			html.Div(id='file-list-div', children=[fileListHtml]),
			html.Div(id='graph-div')])]


# A recusive function that generates a tree structure
# using <ul> and <li> HTML elements.
def MakeDirTree(curDir, selectedDir):
	selected = False
	print(selectedDir, " == ", curDir)
	if selectedDir == curDir:
		selected = True
	fs = filesystem.FileSystem()
	dirName = os.path.basename(curDir[:-1])
	childArr = []
	for subDir in fs.ListSubDirs(curDir):
		childArr.append(MakeDirTree(os.path.join(curDir, subDir), selectedDir))
	if curDir == "":
		dirName = os.path.basename(fs.root)
	if len(childArr) > 0:
		if selected:
			return html.Li(className='selected', children=[
				html.A(dirName, href=Encode(curDir)), html.Ul(children=childArr)
			])		
		else:
			return html.Li(children=[
				html.A(dirName, href=Encode(curDir)), html.Ul(children=childArr)
			])
	else:
		if selected:
			return html.Li(className='selected', children=[
				html.A(dirName, href=Encode(curDir))
			])		
		else:
			return html.Li(children=[
				html.A(dirName, href=Encode(curDir))
			])

# Encode the folder and file names into something that
# can safely be included in a URL.
def Encode(s):
	return base64.b64encode(bytes(s, 'utf-8')).decode('UTF-8','ignore')
	
def Decode(n):
	return base64.b64decode(n).decode('UTF-8','ignore')

