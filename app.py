# la forme
import dash
from dash import html, dcc
from dash import Input, Output #relie filtre au graphe

# le fond
import pandas as pd
import numpy as np

import plotly.graph_objects as go

dates = pd.date_range("2026-01-01", "2026-06-06", freq = "D")
n = len(dates)

price_da = 60 + 14*np.sin(2*np.pi*dates.dayofyear/365) + np.random.normal(0,5,n)
price_id = price_da + np.random.normal(2, 10, n)

df = pd.DataFrame({
    "time" : dates,
    "price_day_ahead": price_da,
    "price_intraday": price_id
})


app = dash.Dash(__name__)

'''fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df["time"], y = df["price_day_ahead"], name = "Day-Ahead"))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["time"], y = df["price_intraday"], name = "Intraday"))
 '''
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=df["time"], y = df["price_day_ahead"], name = "Day-Ahead"))
fig3.add_trace(go.Scatter(x=df["time"], y = df["price_intraday"], name = "Intraday"))


app.layout = html.Div(children=[
    html.H1("Energy Market Dashboard"),
    html.P("Day-Ahead vs Intraday · Europe"),
    dcc.DatePickerRange(
        id="date-filter",
        min_date_allowed="2026-01-01",
        max_date_allowed="2026-06-06",
        start_date="2026-01-01",
        end_date="2026-06-06",
    ),
    #dcc.Graph(id="price-chart1", figure=fig1), #conteneur du graphe
    #dcc.Graph(id="price-chart2", figure=fig2),
    dcc.Graph(id="price-chart3", figure=fig3)    
])

@app.callback(
    Output("price-chart3", "figure"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def update_chart(start_date, end_date):
    filtered_df = df[(df["time"] >= start_date) & (df["time"] <= end_date)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df["time"], y=filtered_df["price_day_ahead"], name="Day-Ahead"))
    fig.add_trace(go.Scatter(x=filtered_df["time"], y=filtered_df["price_intraday"], name="Intraday"))
    
    return fig




if __name__ == "__main__":
    app.run(debug=True)