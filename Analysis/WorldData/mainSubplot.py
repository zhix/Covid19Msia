#! /usr/bin/env python3

from extractData import * 
# import random 

# selectedCountries = ["Australia",
#                     # "Italy",
#                     "Japan",
#                     "Singapore",
#                     "Norway",  
#                     # "South Korea",
#                     "United Kingdom",
#                     # "United States"
#                     ]
# removedCountries = ["China"]

# selectedCountriesBySize = randomCountriesBasedonSize(10, 
#                                 # size=["A", "B", "C","D"],
#                                 randomOrNot=False
#                                 # listRemoval = removedCountries,
#                                 # listAddition = []
#                                 )
# selectedCountries = selectedCountriesBySize[0] ##chose Group A
# print (selectedCountriesBySize)

countryWanted = ["China","South Korea","New Zealand","Australia","Malaysia"]

## Ref: https://plotly.com/python/line-charts/
import plotly.graph_objects as go
from plotly.subplots import make_subplots

fig = go.Figure()

fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{"secondary_y": True}, {"secondary_y": True}],
        [{"secondary_y": True}, {"secondary_y": True}],
        [{"secondary_y": True, "colspan": 2}, None],
           ],
    subplot_titles=countryWanted)


RowCol = [[1,1],[1,2],[2,1],[2,2],[3,1]]

count = 0
for country in countryWanted:
#     pop = getPopulation(country)
#     df = combineData(country)
#     print(df)

#     lastAvailrow = 0
#     for i in pd.notna(df["Accum"]).tolist():
#     	if i: 
#     		lastAvailrow +=1
#     	else: 
#     		break
#     # print(country, lastAvailrow, len(df["Accum"]))
#     # print(["" for i in range(43)]+[country])

#     # stringency = getStringency(country).tolist() 
#     # markerSize = [i/100*50 for i in stringency] 
#     # print (country, lastAvailrow, len(markerSize))

#     fig.add_trace(go.Scatter(
#         x=df["Trailing7DayAccumCases"]/pop*100000, 
#         y=df["Trailing7DayNewCases"]/pop*100000, 
#         # text = ["" for i in range(lastAvailrow-11)]+[country],
#         textposition="bottom right",
#         mode='lines+markers+text',
#         marker=dict(
#                     color=color,
#                     # size = markerSize,
#                     # colorscale="Viridis"
#                     line = dict(
#                         color = color,
#                         width = 1)
#                     ),
#         name=country
#         ))


    pop = getPopulation(country)
    df = combineData(country)
    print(df)
    rowD=RowCol[count][0]
    colD=RowCol[count][1]

    fig.add_trace(go.Scatter(
        x=df["Trailing7DayAccumCases"]/pop*100000, 
        y=df["Trailing7DayNewCases"]/pop*100000, 
        name = country+"_Newcases",
        marker=dict(
            color="#ed0000",
            line = dict(
                color="#ed0000",
                width = 2)
                ),
        ),
        secondary_y=False,
        row=rowD, col=colD)

    fig.add_trace(go.Scatter(
        x=df["Trailing7DayAccumCases"]/pop*100000, 
        y=df["Stringency"], 
        name = country+"_Stringency",
        marker=dict(
            color="#2600ff",
            line = dict(
                color="#2600ff",
                width = 2)
            ),
        ),
        secondary_y=True,
        row=rowD, col=colD)

    count = count + 1

# fig.add_trace(go.Scatter(
#     x=df["date"], 
#     y=df[countryCodesWanted[1]]
#     ),
#     row=1, col=2)

# fig.add_trace(go.Scatter(
#     x=df["date"], 
#     y=df[countryCodesWanted[2]]
#     ),
#     row=2, col=1)


# fig.add_trace(go.Scatter(
#     x=df["date"], 
#     y=df[countryCodesWanted[3]]
#     ),
#     row=2, col=2)

# fig.add_trace(go.Scatter(
#     x=df["date"], 
#     y=df[countryCodesWanted[4]]
#     ),
#     row=3, col=1)

# fig.update_yaxes(range=[0, 100])

fig.update_layout(
    showlegend=False, 
    autosize=True,
    height=800,
    xaxis=dict(
        title="7-Day Trailing Accumulated Cases",
        type="log"
    ),
    xaxis2=dict(
        title="7-Day Trailing Accumulated Cases",
        type="log"
    ),
    xaxis3=dict(
        title="7-Day Trailing Accumulated Cases",
        type="log"
    ),
    xaxis4=dict(
        title="7-Day Trailing Accumulated Cases",
        type="log"
    ),
    xaxis5=dict(
        title="7-Day Trailing Accumulated Cases",
        type="log"
    ),
    yaxis=dict(
        title="7-Day Trailing Daily New Cases",
        type="log"
        ),
    yaxis2=dict(
        title="Stringency",
        range=[0,100],
        ),
    yaxis3=dict(
        title="7-Day Trailing Daily New Cases",
        type="log"
        ),
    yaxis4=dict(
        title="Stringency",
        range=[0,100]
        ),
    yaxis5=dict(
        title="7-Day Trailing Daily New Cases",
        type="log"
        ),
    yaxis6=dict(
        title="Stringency",
        range=[0,100],
        ),
    yaxis7=dict(
        title="7-Day Trailing Daily New Cases",
        type="log"
        ),
    yaxis8=dict(
        title="Stringency",
        range=[0,100],
        ),
    yaxis9=dict(
        title="7-Day Trailing Daily New Cases",
        type="log"
        ),
    yaxis10=dict(
        title="Stringency",
        range=[0,100],
        ),
    title_text="Stringency of each country")



## Ref: https://dash.plotly.com/layout

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True)