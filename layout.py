import os
import dash_core_components as dcc
import dash_html_components as html

from config import config

def CreateLayout(app):
	graph = dcc.Graph(
				id='graph',
				figure={
					'data': [
						{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'line', 'name': 'SF'},
						{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'line', 'name': u'Montréal'},
					],
					'layout': {
						'title': 'Dash Data Visualization'
					}
				}
			)
	treeObj = html.Ul(id='tree-root-ul', className='tree-root',  children=MakeDirTree(config['RootDirectory']))
	app.layout = html.Div(
		children=[
			html.Div(id='row-container', children=[
				html.Div(id='tree-div', children=treeObj),
				html.Div(id='file-list-div', children=[]),
				html.Div(id='graph-div', children=[graph])])
		]
	)

def MakeDirTree(curDir):
	dirName = os.path.basename(curDir)
	childArr = []
	for subDir in os.listdir(curDir):
		if os.path.isdir(os.path.join(curDir, subDir)) and not subDir.startswith('.'):
			childArr.append(MakeDirTree(os.path.join(curDir, subDir)))
	if len(childArr) > 0:
		return html.Li(children=[html.Link(children=[dirName, html.Ul(children=childArr)]) ])
	else:
		return html.Li(children=[dirName])

