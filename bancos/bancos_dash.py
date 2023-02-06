import dash
from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
 
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from dash_bootstrap_templates import load_figure_template

load_figure_template("minty")


app = dash.Dash(external_stylesheets=[dbc.themes.MINTY])
server = app.server

#entrada de dados manual 
df_data = pd.read_excel("demo.xlsx", engine="openpyxl", sheet_name = "Sheet1")

#df_data["Dt_Contratacao_Op"] = pd.to_datetime(df_data["Dt_Contratacao_Op"])
#                           html.H5("Estados :"),
#                           dcc.Checklist(df_data["UF"].value_counts().index,
#                            df_data["UF"].value_counts().index, id="check_UF",
# 40                           inputStyle={"margin-right": "5px", "margin-left": "20px"}),
#43                               dcc.RadioItems(["Valor ", "Ano_Contratacao_Op"], "Valor_FDNE_Contratado", id="main_variable",
# =========  Layout  =========== #
app.layout = html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            
                            html.H2("SUDENE", style={"font-family": "Impact", "font-size": "60px","color": "green"}),
                            html.Hr(),

                            html.H5("Agências  :"),
                            dcc.Checklist(df_data["Agências "].value_counts().index,
                            df_data["Agências "].value_counts().index,id="check_UF",
                            inputStyle={"margin-right": "5px", "margin-left": "20px"}),

                            html.H5("Variável de análise:", style={"margin-top": "30px"}),
                            dcc.RadioItems(["Agências ", "UF "],"Agências ", id="main_variable",

                            inputStyle={"margin-right": "5px", "margin-left": "20px"}),

                        ], style={"height": "90vh", "margin": "20px", "padding": "20px"})
                        
                    ], sm=3),

                    dbc.Col([
                        dbc.Row([
                            dbc.Col([dcc.Graph(id="UF_fig"),], sm=4),
                            dbc.Col([dcc.Graph(id="gender_fig"),], sm=4),
                            dbc.Col([dcc.Graph(id="pay_fig"),], sm=4)
                        ]),
                        dbc.Row([dcc.Graph(id="U_fig")]),
                        dbc.Row([dcc.Graph(id="income_per_product_fig")]),
                    ], sm=9)
                ])   
            ]
        )


# =========  Callbacks  =========== #
# crianção dos callbacks para inserir os gráficos 
@app.callback([
            Output('UF_fig', 'figure'),
            Output('pay_fig', 'figure'),
            Output('gender_fig', 'figure'),
            Output('U_fig', 'figure'),            
            Output('income_per_product_fig', 'figure'),
        ],
            [
                Input('check_UF', 'value'),
                Input('main_variable', 'value')
            ])
def render_graphs(bancos, main_variable):
    # lugares = ["Yangon", "Mandalay"]
    # main_variable= "gross income"
    df = df_data[df_data["Agências "].isin(bancos)]
   

    fig_Carteira = px.bar(df, x="Carteira de Operações de Crédito", y=main_variable)
    fig_Lucro = px.bar(df, y=main_variable, x="Lucro Líquido/Prejuízo", color="UF", orientation="h", barmode="group")
    fig_NR = px.bar(df, y=main_variable, x="NR  - D & H(%) ", color="UF", barmode="group")
    fig_MODAL = px.bar(df, x=main_variable, y="MODALIDADE(%)")
    fig_AE = px.bar(df, y=main_variable, x="ATIVIDADE ECÔNOMICA(%)")

    for fig in [fig_Carteira, fig_MODAL, fig_NR, fig_AE]:
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=200, template="minty")

    fig_Lucro.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500)
        
    return fig_AE, fig_MODAL, fig_NR, fig_Lucro, fig_Carteira

# =========  Run server  =========== #





if __name__ == "__main__":
    app.run_server(debug=True)

