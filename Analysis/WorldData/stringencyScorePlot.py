#! /usr/bin/env python3

import json
import urllib.request
import pandas as pd

# download raw json object
url = "https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/2020-02-01/2020-05-07"
data = urllib.request.urlopen(url).read().decode()

# print(data)

# parse json object
obj = json.loads(data)

countryCodes = obj["countries"] ##List of codes
countryCodesWanted = ["CHN","KOR","NZL","AUS","MYS"]

dateData = obj["data"] 

dates = list(dateData.keys()) ##Return list of dates 


df = pd.DataFrame(columns=['date']+countryCodesWanted)

print(df)

row = 0
for date in dates: 
	countryData = []
	for country in countryCodesWanted:
		try: 
			stringency = dateData[date][country]["stringency_actual"]
			# print (stringency)
			countryData = countryData + [stringency] 
		except:
			countryData = countryData + [""]
			pass
	df.loc[row] = [date]+countryData
	row = row + 1

print(df)

	
## Ref: https://plotly.com/python/line-charts/
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = make_subplots(
    rows=3, cols=2,
    specs=[
    	[{}, {}],
    	[{}, {}],
    	[{"colspan": 2}, None],
           ],
    subplot_titles=countryCodesWanted)


fig.add_trace(go.Scatter(
	x=df["date"], 
	y=df[countryCodesWanted[0]]
	),
	row=1, col=1)

fig.add_trace(go.Scatter(
	x=df["date"], 
	y=df[countryCodesWanted[1]]
	),
	row=1, col=2)

fig.add_trace(go.Scatter(
	x=df["date"], 
	y=df[countryCodesWanted[2]]
	),
	row=2, col=1)


fig.add_trace(go.Scatter(
	x=df["date"], 
	y=df[countryCodesWanted[3]]
	),
	row=2, col=2)

fig.add_trace(go.Scatter(
	x=df["date"], 
	y=df[countryCodesWanted[4]]
	),
	row=3, col=1)

fig.update_yaxes(range=[0, 100])

fig.update_layout(
	showlegend=False, 
	autosize=True,
    height=800,
	title_text="Stringency of each country")



import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)

