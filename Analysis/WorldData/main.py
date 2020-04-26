#! /usr/bin/env python3

from extractData import * 
import random 

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
        df = combineData(country)
        lastAvailrow = 0
        for i in pd.notna(df["Accum"]).tolist():
        	if i: 
        		lastAvailrow +=1
        	else: 
        		break
        # print(country, lastAvailrow, len(df["Accum"]))
        # print(["" for i in range(43)]+[country])
        
        fig.add_trace(go.Scatter(
            x=df["Accum"], 
            y=df["New"], 
            text = ["" for i in range(lastAvailrow-11)]+[country],
            textposition="bottom right",
            mode='markers+text',
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
            text = ["" for i in range(lastAvailrow-11)]+[country],
            textposition="bottom right",
            mode='markers+text',
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
            text = ["" for i in range(lastAvailrow-11)]+[country],
            textposition="bottom right",
            mode='markers+text',
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
            text = ["" for i in range(lastAvailrow-11)]+[country],
            textposition="bottom right",
            mode='markers+text',
            marker=dict(
                        color=color
                        # colorscale="Viridis"
                        # line = dict(
                        #     color = 'rgb(27, 42, 74)',
                        #     width = 2)
                        ),
            name=country
            ))

        fig5.add_trace(go.Scatter(
            x=df["Trailing7DayAccumCases"]/pop, 
            y=df["Trailing7DayNewCases"]/pop, 
            text = ["" for i in range(lastAvailrow-11)]+[country],
            textposition="bottom right",
            mode='lines+markers+text',
            marker=dict(
                        color=color,
                        # colorscale="Viridis"
                        line = dict(
                            color = color,
                            width = 1)
                        ),
            name=country
            ))

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
    xaxis_title='7-Day Trailing Accumulated Cases/100,000 pax of country\'s population',
    yaxis_title='7-Day Trailing Daily New Cases/100,000 pax of country\'s population'
    )

fig5.update_layout(
    autosize=True,
    height=750,
    margin={"r":100,"t":80,"l":50,"b":80}, 
    showlegend=True,
    legend_title='<b> Countries: </b>',
    legend_orientation="v",
    title='Countries: '+ ', '.join(map(str, selectedCountriesBySize)),
    xaxis_type="log", yaxis_type="log",
    xaxis_title='7-Day Trailing Accumulated Cases/100,000 pax of country\'s population',
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

    html.Div([
        dcc.Graph(
            id='covid19world',
            figure=fig
        )], style={'textAlign': 'center', 'position':'relative'}),

    html.Div([
        dcc.Graph(
            id='covid19worldPrev',
            figure=fig2
        )], style={'textAlign': 'center', 'position':'relative'}),

    html.Div([
        dcc.Graph(
            id='covid19worldT7',
            figure=fig4
        )], style={'textAlign': 'center', 'position':'relative'}),

    html.Div([
        dcc.Graph(
            id='covid19worldPrevT7',
            figure=fig3
        )], style={'textAlign': 'center', 'position':'relative'}),

    html.Div([
        dcc.Graph(
            id='covid19worldPrevT7wLines',
            figure=fig5
        )], style={'textAlign': 'center', 'position':'relative'})

])

if __name__ == '__main__':
    app.run_server(debug=True)