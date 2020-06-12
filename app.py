import pandas as pd
import numpy as np 
import plotly.express as px
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# load the pickled data frame
df = pd.read_pickle('data/all_data.csv')

# define options for the dropdown menus
state_options = [dict(label=x, value=x) for x in df.state.unique()]
display_options = [{'label': 'Currently Hospitalized', 'value': 'current_hospitals'},
                  {'label': 'Positive Test Rate', 'value': 'positive_test_rate'},
                  {'label': 'Positive Cases', 'value': 'positive'},
                  {'label': 'Recovered Cases', 'value': 'recovered'},
                  {'label': 'Currently in ICU', 'value': 'in_ICU_currently'}] 

# generate dash app with a theme
app = dash.Dash(
    external_stylesheets=[dbc.themes.SKETCHY]
)

# define layout
app.layout = html.Div(
    children = [
        # generate image at top of webpage
        html.Img(src=app.get_asset_url('covid19img.jpg'), id='logo', height=200),
        # define text headers
        html.H1("Prevalance of COVID-19 in the United States"),
        html.H4("This is a simple app to explore COVID-19 Data for states."),
        html.H5("Data is from https://covidtracking.com/api"),
        # define first dropdown and style
        html.Div([
            html.P(['State:',dcc.Dropdown(id='state', options=state_options)]
        )],
            style={'width':'20%', 'display': 'inline-block'}
        ),
        # define second dropdown and style
        html.Div([
            html.P(['Display:',dcc.Dropdown(id='display', options=display_options)]
        )],
            style={'width':'30%', 'display': 'inline-block'}
        ),
        # define empty plot
        dcc.Graph(id='graph', figure=px.line())
])

@app.callback(
    Output('graph', 'figure'), 
    [Input('state', 'value'),
     Input('display', 'value')])

# define function for displaying 'graph'
def cb(state, display):
    if display == 'positive':
        x_ = df[df['state']==state]['date']
        y_ = df[df['state']==state]['positive']
        title_ = 'Total Number of Positives Cases in {}'.format(state)
    elif display == 'current_hospitals':
        x_ = df[df['state']==state]['date']
        y_ = df[df['state']==state]['hospitalizedCurrently']
        title_ = 'Number of Current Hospitalizations in {}'.format(state)
    elif display == 'recovered':
        x_ = df[df['state']==state]['date']
        y_ = df[df['state']==state]['recovered']
        title_ = 'Total Number of Recovered Cases in {}'.format(state)
    elif display == 'positive_test_rate':
        x_ = df[df['state']==state]['date']
        y_ = df[df['state']==state]['positiveTestRate']
        title_ = 'Positive Test Rate in {}'.format(state)
    elif display == 'in_ICU_currently':
        x_ = df[df['state']==state]['date']
        y_ = df[df['state']==state]['inIcuCurrently']
        title_ = 'Positive Test Rate in {}'.format(state)
    else:
        x_ = [0]
        y_ = [0]
        title_ = 'Select Options Above'
    # generate plotly express line graph
    fig = px.line(df, x=x_, y=y_)
    fig.update_layout(
        title=title_,
        xaxis_title="Date",
        yaxis_title="",
        font=dict(
            family="Courier New, monospace",
            size=14,
            color="#7f7f7f"
    ))
    fig.update_traces(mode="markers+lines", hovertemplate=None)
    fig.update_layout(hovermode="x")
    
    return fig

app.run_server()