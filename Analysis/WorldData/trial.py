#! /usr/bin/env python3

import plotly.graph_objects as go
from extractData import * 

# countries = ["Malaysia", "Canada"]
countries = randomCountriesBasedonSize(8, size=["B"])[1]

if "Malaysia" not in countries:
	countries.append("Malaysia")

print(countries)

Countries=[]
for country in countries: 
	Countries.append(combineData(country))


# df1 = combineData("Malaysia")
# df2 = combineData("Canada")

# df = 
# print(df1.head(20))
# print(df2.head(20))

# Countries=[df1,df2]


fig1 = go.Figure(
   #  add_trace = [
   #  	go.Scatter(
			# x=df1.iloc[0:8]["Trailing7DayAccumPrev"], 
			# y=df1.iloc[0:8]["Trailing7DayNewPrev"],
			# name="Malaysia",
			# marker_color='rgba(255, 0, 0, .8)',
			# mode='markers'
			# ),
   #  	go.Scatter(
			# x=df2.iloc[0:8]["Trailing7DayAccumPrev"], 
			# y=df2.iloc[0:8]["Trailing7DayNewPrev"],
			# name="Canada",
   #  		marker_color='rgba(255, 255, 0, .8)',
			# mode='markers'
			# )
   #  	],
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

counter = 0
for country in Countries: 
	fig1.add_trace(go.Scatter(
		x=country.iloc[0:8]["Trailing7DayAccumPrev"], 
		y=country.iloc[0:8]["Trailing7DayNewPrev"],
		name = countries[counter]
		# mode = "lines"
		)
	)
	counter = counter+1



# fig1.add_trace(go.Scatter(
# 	x=df1.iloc[0:8]["Trailing7DayAccumPrev"], 
# 	y=df1.iloc[0:8]["Trailing7DayNewPrev"]))

# fig1.add_trace(go.Scatter(
# 	x=df2.iloc[0:8]["Trailing7DayAccumPrev"], 
# 	y=df2.iloc[0:8]["Trailing7DayNewPrev"]))


# start off data = Day 7 
# fig1.data[7].visible = True

def plotData(day, countryDataList = Countries, countryList = countries):
	scatterList = []
	counter = 0 
	for country in countryDataList:
		countryPlot = go.Scatter(
			x=country.iloc[0:day]["Trailing7DayAccumPrev"],
			y=country.iloc[0:day]["Trailing7DayNewPrev"],
			name= countryList[counter]
			# mode = "lines"
			)
		scatterList.append(countryPlot)
		counter = counter +1

	return scatterList

frames = []

for day in range(8, getDays()):
	frame = go.Frame(
		data=plotData(day),
		layout=go.Layout(
			title_text="Day "+str(day+1)))
		# go.Frame(data=[go.Scatter(x=[1, 2], y=[1, 2])],
		# 	layout=go.Layout(title_text="Day 2")),
		# go.Frame(data=[go.Scatter(x=[1, 4], y=[1, 4])],
		# 	layout=go.Layout(title_text="Day 3")),
		# go.Frame(data=[go.Scatter(x=[3, 4], y=[3, 4])],
		# 	layout=go.Layout(title_text="Day 4"))
	frames.append(frame)

## https://plotly.com/python-api-reference/generated/plotly.graph_objects.Figure.html#plotly.graph_objects.Figure.update_traces 


fig1.frames = frames 

# fig1.update_layout(
#     autosize=True,
#     height=750,
# 	margin={"r":100,"t":80,"l":50,"b":80}, 
#     showlegend=True,
#     xaxis=dict(range=[0, 5], autorange=False),
#     yaxis=dict(range=[0, 5], autorange=False),
#     title="Day 1",
#     updatemenus=[dict(
# 		type="buttons",
# 		buttons=[dict(
# 			label="Play &#9658;",
# 			method="animate",
#             args=[None])])]

    # legend_title='<b> Countries: </b>',
    # legend_orientation="v"
	# title='Countries: '+ ', '.join(map(str, selectedCountriesBySize)),
    # xaxis_type="log", yaxis_type="log",
    # xaxis_title='Accumulated Cases',
    # yaxis_title='Daily New Cases'
	# )

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