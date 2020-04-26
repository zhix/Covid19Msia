#! /usr/bin/env python3

import plotly.graph_objects as go
from extractData import * 

selectedCountries = ["Australia",
                    # "Italy",
                    "Japan",
                    "Singapore",
                    "Norway",  
                    # "South Korea",
                    "United Kingdom",
                    # "United States"
                    ]
removedCountries = ["China"]

selectedCountriesBySize = randomCountriesBasedonSize(5, 
								size=["A", "B", "C"],
								listRemoval = removedCountries,
								listAddition = []
								)



# countries = ["Malaysia", "Canada"]
countries = randomCountriesBasedonSize(3, size=["B"])[1]

if "Malaysia" not in countries:
	countries.append("Malaysia")

print(countries)

Countries=[]
for country in countries: 
	Countries.append(combineData(country))

fig1 = go.Figure(
    layout=go.Layout(
    	autosize=True,
    	height=750,
		margin={"r":100,"t":80,"l":50,"b":80}, 
		showlegend=True,
		xaxis_type="log", yaxis_type="log",
        xaxis=dict(range=[-7, 2], autorange=False),
        yaxis=dict(range=[-6, -3], autorange=False),
        title="Day 7",
        updatemenus=[dict(
            type="buttons",
            buttons=[dict(label="Play &#9658;",
                          method="animate",
                          args=[None]
                          )])]
    	)
	)

## Setting up the Day 7 stage 
counter = 0
for country in Countries: 
	# lastAvailrow = 0
 #    for i in pd.notna(df["Accum"]).tolist():
 #    	if i: 
	# 		lastAvailrow +=1
	# 	else: 
	# 		break

	fig1.add_trace(go.Scatter(
		x=country.iloc[0:8]["Trailing7DayAccumPrev"], 
		y=country.iloc[0:8]["Trailing7DayNewPrev"],
		name = countries[counter],
		mode = "lines+text",
		text = ["" for i in range(7)]+[countries[counter]],
        textposition="bottom right"
		)
	)
	counter = counter+1


def plotData(day, countryDataList = Countries, countryList = countries):
	scatterList = []
	counter = 0 
	for country in countryDataList:
		countryPlot = go.Scatter(
			x=country.iloc[0:day]["Trailing7DayAccumPrev"],
			y=country.iloc[0:day]["Trailing7DayNewPrev"],
			name= countryList[counter],
			mode = "lines+text",
			text = ["" for i in range(day-1)]+[countries[counter]],
        	textposition="bottom right"
			)
		scatterList.append(countryPlot)
		counter = counter +1

	return scatterList


## Creating frames for Days onward 
frames = []

for day in range(8, getDays()):
	frame = go.Frame(
		data=plotData(day),
		layout=go.Layout(
			title_text="Day "+str(day+1)))
		
	frames.append(frame)

fig1.frames = frames 

import dash
import dash_core_components as dcc
import dash_html_components as html


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = ['https://codepen.io/kle-pra/pen/xkuEt.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(
	style={'backgroundColor': colors['background']}, 
	children=[
    html.H1(children='#StayHome #StaySafe',
    	style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div([
        dcc.Graph(
            id='covid19worldPrevT7',
            figure=fig1
        )], style={'textAlign': 'center', 'position':'relative'})
])

if __name__ == '__main__':
    app.run_server(debug=True)