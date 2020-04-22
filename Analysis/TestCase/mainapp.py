#! /usr/bin/env python3

import pandas as pd

df = pd.read_csv('TestCase.csv')
print(df)

## Ref: https://plotly.com/python/line-and-scatter/
# import plotly.express as px

# fig = px.scatter(
# 	x=df["Daily Tests #"], 
# 	y=df["% Positive"], 
#     color = df["dates"],
#     size=[5 for i in range(len(df["dates"]))] ,
#     color_continuous_scale="Blugrn"
# 	)


## Ref: https://plotly.com/python/line-charts/
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df["Daily Tests #"], 
    y=df["% Positive"], 
    mode='markers',
    marker=dict(size=[20 for i in range(len(df["dates"]))],
                color=df["dates"],
                line = dict(
                    color = 'rgb(27, 42, 74)',
                    width = 2
                )
                # color_continuous_scale="Blugrn"
                ),
    name='real points'
    ))
fig.add_trace(go.Scatter(
    x=df["Daily Tests #"], 
    y=df["MovingAverage"], 
    mode='lines',
    name='4-day moving average'))

fig.update_xaxes(nticks=20)

fig.update_layout(
    legend_orientation="h",
    autosize=True,
    height=750,
	margin={"r":100,"t":80,"l":50,"b":80}, 
	title='Covid-19 Testing: How many do we need to test to cover all?',
    xaxis_title='Total Tests Conducted',
    yaxis_title='% of Cases tested positive'
	)


## Ref: https://dash.plotly.com/layout

import dash
import dash_core_components as dcc
import dash_html_components as html
# from dash.dependencies import Input, Output


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/kle-pra/pen/xkuEt.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(
	style={
        'backgroundColor': colors['background']}, 
	children=[
    html.H1(children='#StayHome #StaySafe',
    	style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(children='''
        A Chloropleth Map for Covid-19 Prevalence in each state of Malaysia
        (Last updated: 29/3/2020)
    ''', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    html.Div([
        dcc.Graph(
            id='covid19msia-PUItests',
            figure=fig
        )], style={'textAlign': 'center', 'position':'relative'}) 

])


# @app.callback(
#     Output(
#         component_id='covid19msia-prevVSstate', 
#         component_property='figure'
#         ),
#     [Input(
#         component_id='date-slider', 
#         component_property = 'value'
#         )]
#     )
# def update_figure(selected_date):
#     dateSelected = dateDict[selected_date]
        
#     fig = px.choropleth_mapbox(
#         data_frame = df, 
#         geojson=statesJson, 
#         locations='StateID', 
#         color=dateSelected, 
#         color_continuous_scale="Reds",
#         range_color=(0, 35),
#         mapbox_style="carto-positron",
#         zoom=5, 
#         center = {"lat": 4.5389064, "lon": 110.1190361},
#         opacity=0.5,
#         labels={''},
#         hover_name='State'
#     )

#     return fig

# @app.callback(
#     Output(
#         component_id='date-selected', 
#         component_property='children'
#         ),
#     [Input(
#         component_id='date-slider', 
#         component_property = 'value'
#         )]
#     )
# def update_output(selected_date):
#     dateSelected = dateDict[selected_date]
#     return 'You have selected {}'.format(dateSelected)

if __name__ == '__main__':
    app.run_server(debug=True)