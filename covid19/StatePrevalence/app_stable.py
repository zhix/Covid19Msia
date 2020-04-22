#! /usr/bin/env python3

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd

from urllib.request import urlopen
import json

mapURLstate = "https://raw.githubusercontent.com/jnewbery/MapMalaysia/master/public/data/states.geojson"
with urlopen(mapURLstate) as response:
    statesJson = json.load(response)

# with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#     counties = json.load(response)

# import pandas as pd
# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
#                    dtype={"fips": str})


## Getting Data 

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1Qew2IsSQtkQbF78zJ_FQZqAd3psR1rDtj4bXLaGb0z4'
RANGE_NAME = 'StatePrevalenceProgression!C3:T12'


def loginWithCredentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)


def extractDataFromSheet(Service, SheetID, RangeName): 
    # Call the Sheets API
    sheet = Service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SheetID,
                                range=RangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found. Try again.')

    else:
        return values

service = loginWithCredentials()
values = extractDataFromSheet(service, SPREADSHEET_ID, RANGE_NAME)

states = values[0]
prev = [float(i) for i in values[-1]]


data = {
        'State':  states,
        'Prevalence': prev,
        'StateID': ["01", "02", "03", "04", "05", "06", "07", "08", "09", "11", "12", "10", "13", "14", "15", "16", "17", "18"]
        }

df = pd.DataFrame(data)

df.iat[0,1] = df.iat[16,1]
df.iat[2,1] = df.iat[16,1]
df.iat[14,1] = df.iat[16,1]

print(df)
    

## Ref: https://plotly.com/python/mapbox-county-choropleth/
import plotly.express as px

fig = px.choropleth_mapbox(
    data_frame = df, 
    geojson=statesJson, ## states 
    locations='StateID', 
    color='Prevalence', ## " Today"
    color_continuous_scale="Viridis",
    range_color=(0, 10),
    mapbox_style="carto-positron",
    zoom=5, 
    center = {"lat": 4.5389064, "lon": 110.1190361},
    opacity=0.5,
    labels={'Prevalence':'Prevalence'},
    hover_name='State'
)

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

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
        A Chloropleth Map for Covid-19 Prevalence in each state of Malaysia (Today 29/3/2020)
    ''', style={
        'textAlign': 'center',
        'color': colors['text']
    }),


    dcc.Graph(
        id='covid19msia-prevVSstate',
        figure=fig
    ), 

    dcc.Slider(
        id='date-slider',
        min=1,
        max=10,
        value=10,
        marks={i:str(i) for i in range(1,11)},
        step=None
    )

])


@app.callback(
    Output(
        component_id='covid19msia-prevVSstate', 
        component_property='figure'
        ),
    [Input(
        component_id='date-slider', 
        component_property = 'value'
        )]
    )

def update_figure(selected_date):
    filtered_df = df[date == selected_date]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(dict(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'type': 'log', 'title': 'GDP Per Capita',
                   'range':[2.3, 4.8]},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            transition = {'duration': 500},
        )
    }



if __name__ == '__main__':
    app.run_server(debug=True)