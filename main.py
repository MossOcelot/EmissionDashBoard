from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

colors = {"background": "#111111", "text": "#7FDBFF"}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pandas.read_excel("data/ghg-emission-of-thailand-edited-july-2021.xlsx")
df.columns = ["BM", "emission", "section_groub", "sub_section", "eng_sub_section", "quantity"]

df['quantity'] = df['quantity'].replace("-",0)

emission_unique = df['emission'].unique()
years_unique = df['BM'].unique()

emission_quantity_years = {'BM': [] ,'emission': [], 'quantity': []}
for y in years_unique:
    bm_y_rows = df[df["BM"] == y]
    for e in emission_unique:
        emission_in_year = bm_y_rows[bm_y_rows["emission"] == e]
        quantity = emission_in_year['quantity'].sum()
        emission_quantity_years['BM'].append(y)
        emission_quantity_years['emission'].append(e)
        emission_quantity_years['quantity'].append(quantity)

df_emission_quantity_years = pandas.DataFrame(emission_quantity_years)




power_emission = df[df['emission'] == 'ภาคพลังงาน']
# 
output = []
value = []

for x in df_emission_quantity_years['emission'].unique():
    for y in df_emission_quantity_years['emission'].unique():
        if x == y:
            continue
        if [y,x] in value:
            continue
        value.append([x,y])

for v in value:
    df2 = df_emission_quantity_years[(df_emission_quantity_years['emission'].str.contains(v[0])) | ( df_emission_quantity_years['emission'].str.contains(v[1]))]
    output.append(dcc.Graph(id=f"{v[0]} {v[1]}",figure=px.bar(df2, x="BM", y="quantity", color="emission", orientation="v", barmode="group")))

fig = px.bar(df_emission_quantity_years, x="BM", y="quantity", color="emission", orientation="v", barmode="group")
fig2 = px.bar(power_emission, x="BM", y="quantity", color="eng_sub_section")

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Hello Dash",
                    style={
                        "textAlign": "center",
                    },
                )
            ],
            className="row",
        ),
        html.Div(
            children=[
                html.Div(
                    children="Dash: A web application framework for your data.",
                    style={
                        "textAlign": "center",
                    },
                ),
            ],
            className="row",
        ),
        html.Div(
            children=[
                html.Div(
                    [dcc.Graph(id="example-graph-1", figure=fig)], className="col"
                ),
                #
            ],
            className="row",
        ),
        html.Div([
            html.Div(
                    [dcc.Graph(id="example-graph-2", figure=fig2)], className="col"
                ),
        ]),
        html.Div(output),
        html.Div([
            html.Button("Hello", className="btn btn-primary")
        ],className="row",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
