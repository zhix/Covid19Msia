#! /usr/bin/env python3

import json
import urllib.request
import pandas as pd


from extractData import * 

selectedCountries = ["China",
					"Malaysia",
					"Australia",
					"New Zealand",
                    # "Italy",
                    # "Japan",
                    # "Singapore",
                    # "Norway",  
                    "South Korea"
                    # "United Kingdom",
                    # "United States"
                    ]

dataPool = []

for country in selectedCountries: 
	countryCode = getCodeDay1Date(country)[0].values[0][0]
	day1Date = getCodeDay1Date(country)[1].values[0][0].split("/")
	DD = day1Date[0]
	MM = day1Date[1]
	YYYY = day1Date[2]

	if len(MM) == 1: 
		MM = "0"+MM 

	if len(DD) == 1: 
		DD = "0"+DD 

	# print(DD, MM, YYYY)
	dateInput = YYYY + "-" + MM + "-" + DD
	print(country, dateInput)

	# download raw json object
	url = "https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/"+dateInput+"/2020-05-07"
	data = urllib.request.urlopen(url).read().decode()

	# parse json object
	obj = json.loads(data)
	print(obj)
	dateData = obj["data"] 
	dates = list(dateData.keys()) ##Return list of dates 
	# print(dates)
	df = pd.DataFrame(columns=['DaySinceCase100', country])

	row = 0
	for date in dates: 
		try: 
			stringency = dateData[date][countryCode]["stringency_actual"]
			# print(stringency)
		except:
			stringency = ""
			pass
		df.loc[row] = [row+1, stringency]
		row = row + 1

	# print(df)
	dataPool =+ [df]

print(dataPool)

df.to_csv ('exportStringencyScore.csv', index = False, header=True)


## Ref: https://plotly.com/python/line-charts/
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots

# fig = make_subplots(
#     rows=3, cols=2,
#     specs=[
#     	[{}, {}],
#     	[{}, {}],
#     	[{"colspan": 2}, None],
#            ],
#     subplot_titles=countryCodesWanted)


# fig.add_trace(go.Scatter(
# 	x=df["date"], 
# 	y=df[countryCodesWanted[0]]
# 	),
# 	row=1, col=1)

# fig.add_trace(go.Scatter(
# 	x=df["date"], 
# 	y=df[countryCodesWanted[1]]
# 	),
# 	row=1, col=2)

# fig.add_trace(go.Scatter(
# 	x=df["date"], 
# 	y=df[countryCodesWanted[2]]
# 	),
# 	row=2, col=1)


# fig.add_trace(go.Scatter(
# 	x=df["date"], 
# 	y=df[countryCodesWanted[3]]
# 	),
# 	row=2, col=2)

# fig.add_trace(go.Scatter(
# 	x=df["date"], 
# 	y=df[countryCodesWanted[4]]
# 	),
# 	row=3, col=1)

# fig.update_yaxes(range=[0, 100])

# fig.update_layout(
# 	showlegend=False, 
# 	autosize=True,
#     height=800,
# 	title_text="Stringency of each country")



# import dash
# import dash_core_components as dcc
# import dash_html_components as html

# app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])

# app.run_server(debug=True)

