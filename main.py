from dash import Dash, dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

colors = {"background": "#111111", "text": "#7FDBFF"}

df = pandas.read_excel("data/ghg-emission-of-thailand-edited-july-2021.xlsx")
df.columns = ["BE", "emission", "section_groub", "sub_section", "eng_sub_section", "quantity"]

df['quantity'] = df['quantity'].replace("-",0)

emission_unique = df['emission'].unique()
years_unique = df['BE'].unique()

emission_quantity_years = {'BE': [] ,'emission': [], 'quantity': []}
for y in years_unique:
    bm_y_rows = df[df["BE"] == y]
    for e in emission_unique:
        emission_in_year = bm_y_rows[bm_y_rows["emission"] == e]
        quantity = emission_in_year['quantity'].sum()
        emission_quantity_years['BE'].append(y)
        emission_quantity_years['emission'].append(e)
        emission_quantity_years['quantity'].append(quantity)

df_emission_quantity_years = pandas.DataFrame(emission_quantity_years)

power_emission = df[df['emission'] == 'ภาคพลังงาน']
#
value = []

for x in df_emission_quantity_years['emission'].unique():
    for y in df_emission_quantity_years['emission'].unique():
        if x == y:
            continue
        if [y,x] in value:
            continue
        value.append([x,y])

fig = px.bar(df_emission_quantity_years, x="BE", y="quantity", color="emission", orientation="v", barmode="group")
fig2 = px.bar(power_emission, x="BE", y="quantity", color="eng_sub_section")

@app.callback(
    Output("bar-graph", "figure"),
    Input("emission_type1", "value"),
    Input("emission_type2", "value"),
)
def show_data(emission_type1, emission_type2):
    print(emission_type1, emission_type2)
    filtered_df = df_emission_quantity_years[(df_emission_quantity_years['emission'].str.contains(emission_type1)) | 
    ( df_emission_quantity_years['emission'].str.contains(emission_type2))]
    # print(filtered_df)
    fig = px.bar(filtered_df, 
    x="BE", y="quantity", 
    color="emission", orientation="v", 
    barmode="group")
    # fig.update_layout(transition_duration=500)

    return fig

# 
df2 = pandas.read_excel("data/ghg-emission-of-thailand-edited-july-2021.xlsx", "Emission ประเทศ (ตารางปกติ)")
df2.columns = ['BE', 'gas_type', 'net_quantity', 'quantity']
df2 = df2[:-2]
df2['LULUCF'] = df2['quantity'] - df2['net_quantity']

df2_1 = df2.iloc[:,[0,1,2]]
df2_1['quantity_type'] = "net_quantity"
df2_1.columns.values[2] = 'quantity'
df2_2 = df2.iloc[:,[0,1,3]]
df2_2['quantity_type'] = "quantity"
df2_2.columns.values[2] = 'quantity'
df2_3 = df2.iloc[:,[0,1,4]]
df2_3['quantity_type'] = "LULUCF"
df2_3.columns.values[2] = 'quantity'

df3 = pandas.concat([df2_1,df2_2,df2_3])

fig3 = px.area(df3, x="BE", y="quantity", color="quantity_type")

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
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(id="bar-graph"),
                    ],
                    className="col-8",
                ),
                html.Div(
                    [
                        # dbc.Dropdown(df["BE"].unique(), df["BE"].min(), id="year"),
                        # dbc.Dropdown(
                        #     df["emission_type"].unique(),
                        #     df["emission_type"][0],
                        #     id="emission_type",
                        # ),
                        dbc.Select(
                            options=[
                                dict(label=et.strip(), value=et.strip())
                                for et in df["emission"].unique()
                            ],
                            id="emission_type1",
                            value=df["emission"][0],
                        ),
                        dbc.Select(
                            options=[
                                dict(label=et.strip(), value=et.strip())
                                for et in df["emission"].unique()
                            ],
                            id="emission_type2",
                            value=df["emission"][0],
                        ),
                    ],
                    className="col-4",
                ),
            ],
            className="row",
        ),
        html.Div([
            html.Div(
                    [dcc.Graph(id="example-graph-3", figure=fig3)], className="col"
                ),
        ]),
        #html.Div(output),
        html.Div([
            html.Button("Hello", className="btn btn-primary")
        ],className="row",
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
