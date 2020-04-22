#! /usr/bin/env python3

from urllib.request import urlopen
import json

mapURLstate = "https://raw.githubusercontent.com/jnewbery/MapMalaysia/master/public/data/states.geojson"
with urlopen(mapURLstate) as response:
    statesJson = json.load(response)

## Getting Data 

import pandas as pd

df = pd.read_csv('HospitalData12Apr.csv')

stateids = []

for i in df["StateID"]:
    if i < 10:
        i = "0"+str(i)
    else:
        i = str(i)
    stateids = stateids + [i]

df["StateID"] = stateids

## Ref: https://plotly.com/python/mapbox-county-choropleth/
import plotly.express as px

fig = px.choropleth_mapbox(
    data_frame = df, 
    geojson=statesJson, 
    locations="StateID", 
    color="SUM of # ICU beds", 
    color_continuous_scale="Darkmint",
    range_color=(0, 100),
    mapbox_style="carto-positron",
    zoom=5, 
    center = {"lat": 4.5389064, "lon": 110.1190361},
    opacity=0.5,
    hover_name="State"
)

fig.update_layout(
    autosize=True,
    height=750,
    margin={"r":0,"t":0,"l":0,"b":0}
    )


fig2 = px.choropleth_mapbox(
    data_frame = df, 
    geojson=statesJson, 
    locations="StateID", 
    color="#inpatient beds per 100,000 pax", 
    color_continuous_scale="Tealgrn",
    range_color=(0, 200),
    mapbox_style="carto-positron",
    zoom=5, 
    center = {"lat": 4.5389064, "lon": 110.1190361},
    opacity=0.5,
    hover_name="State"
)

fig2.update_layout(
    autosize=True,
    height=750,
    margin={"r":0,"t":0,"l":0,"b":0}
    )

fig3 = px.choropleth_mapbox(
    data_frame = df, 
    geojson=statesJson, 
    locations="StateID", 
    color="Available Capacity of Hospitals", 
    color_continuous_scale="RdBu",
    range_color=(-70, 90),
    mapbox_style="carto-positron",
    zoom=5, 
    center = {"lat": 4.5389064, "lon": 110.1190361},
    opacity=0.5,
    hover_name="State"
)

fig3.update_layout(
    autosize=True,
    height=750,
    margin={"r":0,"t":0,"l":0,"b":0}
    )

## Ref: https://dash.plotly.com/layout

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/kle-pra/pen/xkuEt.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
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

    html.Div(id="date-selected", 
        style={
        'textAlign': 'center',
        'color': colors['text']
    }),


    dcc.Graph(
        id='covid19msia-prevVSstate',
        figure=fig
    ),

    dcc.Graph(
        id='covid19msia-bedper100k',
        figure=fig2
    ),

    dcc.Graph(
        id='covid19msia-hospitalcapacity',
        figure=fig3
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)