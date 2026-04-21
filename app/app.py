# app/app.py

import os
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update

# =========================
# LOAD DATA
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "synthetic_data.csv")

df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])

FREQ = 10


# =========================
# AGGREGATION
# =========================
def compute_car_stats(df):
    stats = []

    for car_id, dff in df.groupby("car_id"):
        dff = dff.sort_values("timestamp")

        active = dff["is_active"]

        total_runtime = active.sum() / FREQ
        uptime_ratio = active.mean()

        avg_reliability = dff["reliability"].mean()
        dropout_rate = dff["dropout"].mean()
        motion_rate = dff["motion_artifact"].mean()

        stats.append({
            "car_id": car_id,
            "is_active": active.iloc[-1],
            "total_runtime": total_runtime,
            "uptime_ratio": uptime_ratio,
            "avg_reliability": avg_reliability,
            "dropout_rate": dropout_rate,
            "motion_rate": motion_rate
        })

    return pd.DataFrame(stats)


# =========================
# APP INIT
# =========================
app = Dash(__name__, suppress_callback_exceptions=True)


# =========================
# NAVBAR (ALWAYS VISIBLE)
# =========================
def navbar():
    return html.Div([
        dcc.Link("🏠 Home", href="/", style={"margin-right": "20px"}),
        dcc.Link("🚗 Fleet", href="/fleet", style={"margin-right": "20px"}),
        dcc.Link("🌍 Map", href="/map"),
    ], style={
        "padding": "12px",
        "background": "#eee",
        "font-size": "18px"
    })


# =========================
# PAGES
# =========================

def home_page():
    stats = compute_car_stats(df)
    active = stats[stats["is_active"]]

    rows = []
    for _, row in active.iterrows():
        rows.append(
            html.Div([
                dcc.Link(row["car_id"], href=f"/car/{row['car_id']}"),
                html.Span(" 🟢 ACTIVE"),
                html.Span(f" | Reliability: {row['avg_reliability']:.2f}")
            ], style={"padding": "5px"})
        )

    return html.Div([
        html.H1("Active Vehicles"),
        html.Div(rows)
    ])


def fleet_page():
    stats = compute_car_stats(df)

    rows = []
    for _, row in stats.iterrows():
        status = "🟢" if row["is_active"] else "⚫"

        rows.append(
            html.Div([
                dcc.Link(row["car_id"], href=f"/car/{row['car_id']}"),
                html.Span(f" {status}"),
                html.Span(f" | Runtime: {row['total_runtime']:.1f}s"),
                html.Span(f" | Uptime: {row['uptime_ratio']:.2f}"),
                html.Span(f" | Rel: {row['avg_reliability']:.2f}"),
                html.Span(f" | Dropout: {row['dropout_rate']:.3f}"),
                html.Span(f" | Motion: {row['motion_rate']:.3f}")
            ], style={"padding": "5px"})
        )

    return html.Div([
        html.H1("Fleet Overview"),
        html.Div(rows)
    ])


def map_page():
    latest = df.sort_values("timestamp").groupby("car_id").tail(1)

    fig = px.scatter_geo(
        latest,
        locations="country",
        locationmode="country names",
        hover_name="car_id",
        size="reliability",
        projection="natural earth",
        title="Car Locations"
    )

    return html.Div([
        html.H1("Global Map"),
        dcc.Graph(figure=fig)
    ])


def car_page(car_id):
    dff = df[df["car_id"] == car_id]
    stats = compute_car_stats(df)
    row = stats[stats["car_id"] == car_id].iloc[0]

    status = "🟢 LIVE (updating)" if row["is_active"] else "⚫ Inactive"

    fig_hr = px.line(dff, x="timestamp", y="heart_rate", title="Heart Rate")
    fig_rel = px.line(dff, x="timestamp", y="reliability", title="Reliability")

    return html.Div([
        html.H2(f"Car: {car_id}"),
        html.H4(status),

        html.Div([
            html.Div(f"Total runtime: {row['total_runtime']:.1f}s"),
            html.Div(f"Uptime ratio: {row['uptime_ratio']:.2f}"),
            html.Div(f"Avg reliability: {row['avg_reliability']:.2f}"),
            html.Div(f"Dropout rate: {row['dropout_rate']:.3f}"),
            html.Div(f"Motion rate: {row['motion_rate']:.3f}")
        ], style={"margin-bottom": "20px"}),

        dcc.Graph(id="hr-graph", figure=fig_hr),
        dcc.Graph(id="rel-graph", figure=fig_rel),

        dcc.Interval(id="interval", interval=2000)
    ])


# =========================
# MAIN LAYOUT
# =========================
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar(),
    html.Hr(),
    html.Div(id="page-content")
])


# =========================
# ROUTING
# =========================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def route(path):
    if path.startswith("/car/"):
        return car_page(path.split("/")[-1])
    elif path == "/fleet":
        return fleet_page()
    elif path == "/map":
        return map_page()
    else:
        return home_page()


# =========================
# LIVE UPDATE
# =========================
@app.callback(
    Output("hr-graph", "figure"),
    Input("interval", "n_intervals"),
    Input("url", "pathname"),
    prevent_initial_call=True
)
def live_update(n, path):
    if not path.startswith("/car/"):
        return no_update

    car_id = path.split("/")[-1]
    dff = df[df["car_id"] == car_id]

    if not dff["is_active"].iloc[-1]:
        return px.line(dff, x="timestamp", y="heart_rate")

    dff = dff.copy()
    dff["heart_rate"] += np.random.normal(0, 0.5, len(dff))

    return px.line(dff, x="timestamp", y="heart_rate")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port)