import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import filesystem
import base64

from config import config

def CreateLayout(app):	
	app.layout =  html.Div(id='page-contents', children=ServeLayout(''))
	
	@app.callback(dash.dependencies.Output('page-contents', 'children'),
		[dash.dependencies.Input('url', 'pathname')])
	def ProcessUrl(pathname):
		if pathname is None:
			print("NONE")
			return ServeLayout('')
		else:
			return ServeLayout(pathname)

def ServeLayout(curUrlString):
	fs = filesystem.FileSystem()
	tree = MakeDirTree('', fs=fs)
	treeObj = html.Ul(id='tree-root-ul', className='tree-root', children=tree)
	if curUrlString == '':
		print("Nothing detected")
		# Return an empty page with only a list of directory names
		return [dcc.Location(id='url', refresh=False),
				html.Div(id='row-container',
				children=[html.Div(id='tree-div', children=treeObj),
				html.Div(id='file-list-div'),
				html.Div(id='graph-div')])]
	else:
		print(curUrlString)
		curItem = Decode(curUrlString[1:])
		curDir = os.path.dirname(os.path.realpath(curItem))
		print(curDir)
	return None

# A recusive function that generates a tree structure
# using <ul> and <li> HTML elements.
def MakeDirTree(curDir, fs):
	dirName = os.path.basename(curDir)
	childArr = []
	for subDir in fs.ListSubDirs(curDir):
		childArr.append(MakeDirTree(os.path.join(curDir, subDir)))
	if len(childArr) > 0:
		return html.Li(children=[
			html.A(dirName, href=Encode(curDir)), html.Ul(children=childArr)
		])
	else:
		return html.Li(children=[
			html.A(dirName, href=Encode(curDir))
		])
'''	elif protocol == 'samba':
		dirName = os.path.basename(curDir) if len(curDir) > 0 else "Root"
		childArr = []
		for subDir in smb.ListSubDirs(curDir):
			childArr.append(MakeDirTree(os.path.join(curDir, subDir), smb=smb))
		if len(childArr) > 0:
			print("Return Children", dirName)
			return html.Li(children=[dirName, html.Ul(children=childArr) ])
		else:
			print("Return Childless", dirName)
			return html.Li(children=[dirName])
'''
# Encode the folder and file names into something that
# can safely be included in a URL.
def Encode(s):
	return base64.b64encode(bytes(s, 'utf-8')).decode('UTF-8','ignore')
	
def Decode(n):
	return base64.b64decode(n).decode('UTF-8','ignore')

