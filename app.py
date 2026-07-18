import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

app = Dash(__name__)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "formatted_data.csv")

if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    df = df.sort_values(by="date")
else:
    raise FileNotFoundError(f"Could not find {DATA_PATH}.")

# The approximate date the price increase went into effect (January 15, 2021)
PRICE_INCREASE_DATE = "2021-01-15"

app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
        "backgroundColor": "#f4f6f9",
        "padding": "30px",
        "minHeight": "100vh"
    },
    children=[
        # Banner Header
        html.Div(
            style={
                "backgroundColor": "#1e3d59",
                "padding": "20px",
                "borderRadius": "8px",
                "textAlign": "center",
                "marginBottom": "25px",
                "color": "#ffffff"
            },
            children=[
                html.H1("Pink Morsel Sales Analysis Dashboard", style={"margin": "0 0 5px 0", "fontSize": "28px"}),
                html.P("Evaluating the business impact of the 2021 product price restructuring", style={"margin": "0", "opacity": "0.8"})
            ]
        ),
        
        # Control Card
        html.Div(
            style={
                "backgroundColor": "#ffffff", 
                "padding": "20px", 
                "borderRadius": "8px",
                "marginBottom": "25px",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"
            },
            children=[
                html.Label(
                    "Select Target Market Region:", 
                    style={"fontWeight": "600", "display": "block", "marginBottom": "10px", "color": "#1e3d59"}
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": " North Region", "value": "north"},
                        {"label": " East Region", "value": "east"},
                        {"label": " South Region", "value": "south"},
                        {"label": " West Region", "value": "west"},
                        {"label": " View All Combined", "value": "all"}
                    ],
                    value="all",
                    inline=True,
                    inputStyle={"marginRight": "5px", "marginLeft": "20px"}
                )
            ]
        ),
        
        # Graph Card
        html.Div(
            style={"backgroundColor": "#ffffff", "padding": "25px", "borderRadius": "8px", "boxShadow": "0 2px 8px rgba(0,0,0,0.05)"},
            children=[
                dcc.Graph(id="sales-line-chart")
            ]
        )
    ]
)

@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value")
)
def update_graph(selected_region):
    if selected_region == "all":
        filtered_df = df
        # Graph multi-color lines for each region to stay readable
        fig = px.line(
            filtered_df, x="date", y="sales", color="region",
            title="Pink Morsel Sales Over Time — All Regions Summary",
            labels={"date": "Timeline", "sales": "Daily Revenue ($)", "region": "Region"}
        )
    else:
        filtered_df = df[df["region"] == selected_region]
        fig = px.line(
            filtered_df, x="date", y="sales",
            title=f"Pink Morsel Sales Over Time — {selected_region.capitalize()} Region Profile",
            labels={"date": "Timeline", "sales": "Daily Revenue ($)"}
        )
    
    # Superimpose a vertical reference line pinpointing the price hike milestone
    fig.add_vline(
        x=PRICE_INCREASE_DATE, 
        line_width=2.5, 
        line_dash="dash", 
        line_color="#e056fd",
        annotation_text="Price Increased ($1.50 → $2.00) ",
        annotation_position="top left"
    )
    
    fig.update_layout(
        template="plotly_white",
        title_x=0.01,
        hovermode="x unified",
        margin=dict(l=40, r=40, t=60, b=40)
    )
    
    return fig

if __name__ == "__main__":
    app.run(debug=True)