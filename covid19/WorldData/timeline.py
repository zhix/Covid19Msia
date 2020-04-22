#! /usr/bin/env python3

from extractData import * 
# import random 

# accumData = extractData()[0]
# newcaseData = extractData()[1]

# allCountriesList = extractCountriesPopulation()["World"].tolist()
# selectedCountries = [random.choice(allCountries) for i in range(5)]
selectedCountries = [
					# "Italy",
                    # "Japan",
                    "Malaysia",  
                    # "South Korea",
                    # "United Kingdom",
                    "Canada"]
selectedCountriesBySize = randomCountriesBasedonSize(5, 
	randomOrNot=False, 
	listRequired = selectedCountries)
# selectedCountries = selectedCountriesBySize[0] ##chose Group A
print (selectedCountriesBySize)


## Ref: https://plotly.com/python/line-charts/
import plotly.graph_objects as go

fig5 = go.Figure()

for day in range(getDays()):
	grouping = 0
	for group in selectedCountriesBySize: 
	    color = getColor(grouping)
	    grouping=grouping+1
	    for country in group:
	        pop = getPopulation(country)
	        df = combineData(country).iloc[0:day]

	        print(df.head())

	        fig5.add_trace(go.Scatter(
	            visible=False,
	            x=df["Trailing7DayAccumCases"]/pop, 
	            y=df["Trailing7DayNewCases"]/pop, 
	            mode='lines+markers',
	            marker=dict(
	                        color=color,
	                        # colorscale="Viridis"
	                        line = dict(
	                            color = color,
	                            width = 1)
	                        ),
	            name=country
	            ))


##  Steps for the slider

steps = []

for i in range(getDays()):
    step = dict(
        method="restyle",
        # label=i,
        # value=i,
        args=["visible", [False] * getDays()],
    )
    step["args"][1][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

# print(steps)

sliders = [dict(
    active=30, 
    currentvalue={
    	"font":{"size":20},
    	"xanchor":"right",
    	"prefix": "Day: "},
    pad={"t": 50},
    steps=steps
)]

fig5.update_xaxes(range=[-7, 2])
fig5.update_yaxes(range=[-6, -5])

fig5.update_layout(
    autosize=True,
    height=750,
    margin={"r":100,"t":80,"l":50,"b":80}, 
    showlegend=True,
    legend_title='<b> Countries: </b>',
    legend_orientation="v",
    title='Countries: '+ ', '.join(map(str, selectedCountriesBySize)),
    xaxis_type="log", yaxis_type="log",
    xaxis_title='7-Day Trailing Accumulated Cases/100,000 pax of country\' population',
    yaxis_title='7-Day Trailing Daily New Cases/100,000 pax of country\'s population',
    sliders = sliders
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
            id='covid19worldPrevT73',
            figure=fig5
        )], style={'textAlign': 'center', 'position':'relative'})

    # dcc.Slider(
    #     id='day-slider',
    #     min=1,
    #     max=getDays()[0],
    #     value=getDays()[0]/2,
    #     marks={i:i for i in range(1,getDays()[0])},
    #     step=None
    # ) 

])


# @app.callback(
#     Output(
#         component_id='covid19worldPrevT72', 
#         component_property='figure'
#         ),
#     [Input(
#         component_id='day-slider', 
#         component_property = 'value'
#         )]
#     )
# def update_figure(selected_date):
#     # dateSelected = dateDict[selected_date]
        
#     fig4.add_trace(go.Scatter(
#             x=df["Trailing7DayAccumCases"], 
#             y=df["Trailing7DayNewCases"], 
#             mode='markers',
#             marker=dict(
#                         color=color
#                         # colorscale="Viridis"
#                         # line = dict(
#                         #     color = 'rgb(27, 42, 74)',
#                         #     width = 2)
#                         ),
#             name=country
#             ))

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