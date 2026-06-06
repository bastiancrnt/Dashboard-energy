# la forme
import dash
from dash import html, dcc

# le fond
import pandas as pd
import numpy as np

import plotly.graph_objects as go

dates = pd.date_range("2026-01-01", "2026-06-06", freq = "D")
n = len(dates)

price_da = 60 + 14*np.sin(2*np.pi*dates.hour/24) + np.random.normal(0,5,n)
price_id = price_da + np.random.normal(2, 10, n)

df = pd.DataFrame({
    "time" : dates,
    "price_day_ahead": price_da,
    "price_intraday": price_id
})


app = dash.Dash(__name__)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["time"], y = df["price_day_ahead"], name = "Day-Ahead"))

app.layout = html.Div(children=[
    html.H1("Energy Market Dashboard"),
    html.P("Day-Ahead vs Intraday · Europe"),
    dcc.Graph(id="price-chart", figure=fig) #conteneur du graphe
])


dcc.Graph(id="price-chart", figure=fig) #conteneur du graphe

if __name__ == "__main__":
    app.run(debug=True)