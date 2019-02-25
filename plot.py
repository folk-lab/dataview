import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import h5py

# This function should return a dash component, probably a dcc.Graph object!
def Plot(fileName):
	f = h5py.File(fileName, 'r')
	print("PLOT", f.keys())
	ds = f['DS1']
	print(ds.shape)
	if len(ds.shape) == 1:
		return Plot1d(ds)
	elif len(ds.shape) == 2:
		return Plot2d(ds)
	else:
		return html.Div('I don\'t know!')

def Plot1d(ds):
	return ''

def Plot2d(ds):
	return dcc.Graph(
        id='plot2d',
        figure={
            'data': [go.Heatmap(z=ds)],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )

