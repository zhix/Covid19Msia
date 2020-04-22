#! /usr/bin/env python3

from extractData import * 
import random 

populations = extractCountriesPopulation()
# print(populations.head())

## Ref: https://plotly.com/python/line-charts/
import plotly.express as px

fig = px.histogram(populations, x="Population", nbins=600)


fig.update_layout(
    autosize=True,
    height=750
	# margin={"r":100,"t":80,"l":50,"b":80}, 
 #    showlegend=True,
 #    legend_title='<b> Countries: </b>',
 #    legend_orientation="v",
	# title='Countries: '+ ', '.join(map(str, selectedCountries)),
 #    xaxis_type="log", yaxis_type="log",
 #    xaxis_title='Accumulated Cases',
 #    yaxis_title='Daily New Cases'
	)

## Ref: https://dash.plotly.com/layout

import dash
import dash_core_components as dcc
import dash_html_components as html
# from dash.dependencies import Input, Output


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
        )], style={'textAlign': 'center', 'position':'relative'})

])

if __name__ == '__main__':
    app.run_server(debug=True)