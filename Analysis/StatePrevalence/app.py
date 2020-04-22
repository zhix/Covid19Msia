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
RANGE_NAME = 'StatePrevalenceProgression!A3:T40'


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

dates = [str(i[0]) for i in values]
dates = dates[1:]

states = values[0]
states = states[2:]

data = {
    'State':  states,
    'StateID': ["01", "02", "03", "04", "05", "06", "07", "08", "09", "11", "12", "10", "13", "14", "15", "16", "17", "18"],
    }


for j in range(len(dates)):
    try: 
        data[dates[j]] = values[j+1][2:]  ## taking prevalence values into dates
        data[dates[j]] = [float(i) for i in data[dates[j]]] ## convert strings into floats
    except: 
        pass

df = pd.DataFrame(data)

## make all KL, Selangor & Putrajaya the same prevalence 
for k in range(len(df.columns)):
    if k >= 2:
        df.iat[0,k] = df.iat[16,k]
        df.iat[2,k] = df.iat[16,k]
        df.iat[14,k] = df.iat[16,k]

print(df)
print(len(dates))
print(int(len(dates)))
finalDate = dates[-1]
print(finalDate)

dateDict = {i:dates[i] for i in range(1,len(dates))}
print(dateDict)

## Ref: https://plotly.com/python/mapbox-county-choropleth/
import plotly.express as px

fig = px.choropleth_mapbox(
    data_frame = df, 
    geojson=statesJson, 
    locations='StateID', 
    color=finalDate, 
    color_continuous_scale="RdBu_r",
    range_color=(0, 42),
    mapbox_style="carto-positron",
    zoom=5.3, 
    center = {"lat": 4.5389064, "lon": 110.1190361},
    opacity=0.5,
    labels={'Prevalence':'Prevalence'},
    hover_name='State'
)

fig.update_layout(
    autosize=True,
    height=700,
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

    dcc.Slider(
        id='date-slider',
        min=1,
        max=len(dates),
        value=int(len(dates)/2),
        marks={i:dates[i] for i in range(1,len(dates))},
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
    dateSelected = dateDict[selected_date]
        
    fig = px.choropleth_mapbox(
        data_frame = df, 
        geojson=statesJson, 
        locations='StateID', 
        color=dateSelected, 
        color_continuous_scale="RdBu_r",
        range_color=(0, 42),
        mapbox_style="carto-positron",
        zoom=5.5, 
        center = {"lat": 4.5389064, "lon": 110.1190361},
        opacity=0.5,
        labels={''},
        hover_name='State'
    )

    return fig

@app.callback(
    Output(
        component_id='date-selected', 
        component_property='children'
        ),
    [Input(
        component_id='date-slider', 
        component_property = 'value'
        )]
    )
def update_output(selected_date):
    dateSelected = dateDict[selected_date]
    return 'You have selected {}'.format(dateSelected)

if __name__ == '__main__':
    app.run_server(debug=True)