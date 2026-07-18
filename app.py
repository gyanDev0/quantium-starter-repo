import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Read the data
df = pd.read_csv("formatted_data.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Total sales for each day
df = df.groupby("date", as_index=False)["sales"].sum()

# Create graph
fig = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Over Time"
)

# Create app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)