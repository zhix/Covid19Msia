#! /usr/bin/env python3

from extractData import * 
import random 

# accumData = extractData()[0]
# newcaseData = extractData()[1]

# allCountriesList = extractCountriesPopulation()["World"].tolist()
# selectedCountries = [random.choice(allCountries) for i in range(5)]
selectedCountries = ["Australia",
                    "Italy",
                    "Japan",
                    "Malaysia",  
                    "South Korea",
                    "United Kingdom",
                    "United States"]
selectedCountriesBySize = randomCountriesBasedonSize(5, size=["B"])
# selectedCountries = selectedCountriesBySize[0] ##chose Group A
print (selectedCountriesBySize)


## Ref: https://plotly.com/python/line-charts/
import plotly.graph_objects as go

fig = go.Figure()
fig2 = go.Figure()
fig3 = go.Figure()
fig4 = go.Figure()
fig5 = go.Figure()

grouping=0
for group in selectedCountriesBySize: 
    color = getColor(grouping)
    grouping=grouping+1
    for country in group:
        pop = getPopulation(country)
        
        
        # totalDays = len(accumData[country])

        df = combineData(country)
        
        fig.add_trace(go.Scatter(
            x=df["Accum"], 
            y=df["New"], 
            mode='markers',
            marker=dict(color=color
                        # colorscale="Rainbow"
                        # line = dict(
                        #     color = 'rgb(27, 42, 74)',
                        #     width = 2)
                        ),
            name=country
            ))
        
        fig2.add_trace(go.Scatter(
            x=df["Accum"]/pop, 
            y=df["New"]/pop, 
            mode='markers',
            marker=dict(
                        color=color
                        # colorscale="Viridis"
                        # line = dict(
                        #     color = 'rgb(27, 42, 74)',
                        #     width = 2)
                        ),
            name=country
            ))

        fig3.add_trace(go.Scatter(
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

        fig4.add_trace(go.Scatter(
            x=df["Trailing7DayAccumCases"], 
            y=df["Trailing7DayNewCases"], 
            mode='markers',
            marker=dict(
                        color=color
                        # colorscale="Viridis"
                        # line = dict(
                        #     color = 'rgb(27, 42, 74)',
                        #     width = 2)
                        ),
            name=country
            ))


# fig.update_xaxes(nticks=20)

fig.update_layout(
    autosize=True,
    height=750,
	margin={"r":100,"t":80,"l":50,"b":80}, 
    showlegend=True,
    legend_title='<b> Countries: </b>',
    legend_orientation="v",
	title='Countries: '+ ', '.join(map(str, selectedCountriesBySize)),
    xaxis_type="log", yaxis_type="log",
    xaxis_title='Accumulated Cases',
    yaxis_title='Daily New Cases'
	)

fig2.update_layout(
    autosize=True,
    height=750,
    margin={"r":100,"t":80,"l":50,"b":80}, 
    showlegend=True,
    legend_title='<b> Countries: </b>',
    legend_orientation="v",
    title='Countries: '+ ', '.join(map(str, selectedCountriesBySize)),
    xaxis_type="log", yaxis_type="log",
    xaxis_title='Accumulated Cases/100,000 pax of country\'s population',
    yaxis_title='Daily New Cases/100,000 pax of country\'s population'
    )

fig3.update_layout(
    autosize=True,
    height=750,
    margin={"r":100,"t":80,"l":50,"b":80}, 
    showlegend=True,
    legend_title='<b> Countries: </b>',
    legend_orientation="v",
    title='Countries: '+ ', '.join(map(str, selectedCountriesBySize)),
    xaxis_type="log", yaxis_type="log",
    xaxis_title='7-Day Trailing Accumulated Cases/100,000 pax of country\' population',
    yaxis_title='7-Day Trailing Daily New Cases/100,000 pax of country\'s population'
    )

fig4.update_layout(
    autosize=True,
    height=750,
    margin={"r":100,"t":80,"l":50,"b":80}, 
    showlegend=True,
    legend_title='<b> Countries: </b>',
    legend_orientation="v",
    title='Countries: '+ ', '.join(map(str, selectedCountriesBySize)),
    xaxis_type="log", yaxis_type="log",
    xaxis_title='7-Day Trailing Accumulated Cases',
    yaxis_title='7-Day Trailing Daily New Cases'
    )


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
	            mode='markers',
	            marker=dict(
	                        color=color
	                        # colorscale="Viridis"
	                        # line = dict(
	                        #     color = 'rgb(27, 42, 74)',
	                        #     width = 2)
	                        ),
	            name=country
	            ))


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
    active=10, #currect value
    currentvalue={
    	"font":{"size":20},
    	"xanchor":"right",
    	"prefix": "Day: "},
    pad={"t": 50},
    steps=steps
)]


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
	style={
        'backgroundColor': colors['background']}, 
	children=[
    html.H1(children='#StayHome #StaySafe',
    	style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    # html.Div(children='''
    #     A Chloropleth Map for Covid-19 Prevalence in each state of Malaysia
    #     (Last updated: 29/3/2020)
    # ''', style={
    #     'textAlign': 'center',
    #     'color': colors['text']
    # }),

    html.Div([
        dcc.Graph(
            id='covid19world',
            figure=fig
        )], style={'textAlign': 'center', 'position':'relative'}),

    html.Div([
        dcc.Graph(
            id='covid19worldT7',
            figure=fig4
        )], style={'textAlign': 'center', 'position':'relative'}),

    html.Div([
        dcc.Graph(
            id='covid19worldPrev',
            figure=fig2
        )], style={'textAlign': 'center', 'position':'relative'}),


    html.Div([
        dcc.Graph(
            id='covid19worldPrevT72',
            figure=fig3
        )], style={'textAlign': 'center', 'position':'relative'}),

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