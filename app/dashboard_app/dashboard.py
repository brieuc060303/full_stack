from dash import dcc
from dash import html
from callbacks import get_callbacks

def create_dashboard(app, fig_year, fig_sx, fig_activity, fig_world, fig_hours, fig_time_periods, fig_age, fig_fatal, fig_not_fatal, fig_usa, fig_aus, fig_sa):
    app.layout = html.Div(id='dashboard-content', style={'backgroundColor': 'cornsilk'}, children=[
        html.H3(
            "Le dashboard n'a pas encore les données. Veuillez les charger puis actualiser.",
            style={'text-align': 'center', 'font-size': '24px', 'margin-top': '20px'}
        ),
        html.Button("Actualiser", id="refresh-button", n_clicks=0),
        dcc.Tabs([  # Différentes onglets, chaque onglet contient un graphique
            dcc.Tab(id='tab1', label='Années', children=[  # Premier graphique : nombre d'attaques par année
                html.Div([
                    dcc.Graph(id='graph1', figure=fig_year),  # Rechargement du graphique
                    html.Div(
                        id='description1',
                        children="Le nombre d'attaques de requins par année",  # Description pour cet onglet
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}
                    )
                ])
            ]),
            dcc.Tab(id='tab2', label='Genre', children=[  # Deuxième graphique : nombre d'attaques selon le genre
                html.Div([
                    dcc.Graph(id='graph2', figure=fig_sx),
                    html.Div(
                        id='description2',
                        children="La proportion d'attaques de requins par genre depuis 1800",
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}
                    )
                ])
            ]),
            dcc.Tab(id='tab3', label='Fatalité', children=[  # Attaques fatales vs non-fatales
                html.Div([
                    html.Div([  # Graphique des attaques fatales
                        dcc.Graph(id='graph3-fatal', figure=fig_fatal),
                        html.Div(
                            id='description3-fatal',
                            children="Attaques fatales par espèce de requin",
                            style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}
                        )
                    ], style={'display': 'inline-block', 'width': '48%', 'padding': '10px'}),
                    html.Div([  # Graphique des attaques non-fatales
                        dcc.Graph(id='graph3-not-fatal', figure=fig_not_fatal),
                        html.Div(
                            id='description3-not-fatal',
                            children="Attaques non-fatales par espèce de requin",
                            style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}
                        )
                    ], style={'display': 'inline-block', 'width': '48%', 'padding': '10px'})
                ])
            ]),
            dcc.Tab(id='tab4', label='Activité', children=[  # Nombre d'attaques par activité humaine
                html.Div([
                    dcc.Graph(id='graph4', figure=fig_activity),
                    html.Div(
                        id='description4',
                        children="Le nombre d'attaques de requins par activité humaine depuis 1800",
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}
                    )
                ])
            ]),
            dcc.Tab(id='tab5', label='Temps', children=[  # Graphiques liés au temps
                html.Div([
                    dcc.Graph(id='graph5', figure=fig_hours),
                    dcc.Graph(id='graph6', figure=fig_time_periods)
                ])
            ]),
            dcc.Tab(id='tab6', label='Attaques par âge', children=[  # Attaques de requins par âge
                html.Div([
                    dcc.Graph(id='graph7', figure=fig_age)
                ])
            ]),
            dcc.Tab(id='tab7', label='Carte des USA', children=[  # Carte des attaques aux USA
                html.Div([dcc.Graph(id='graph_usa_map', figure=fig_usa)])
            ]),
            dcc.Tab(id='tab8', label='Carte de l\'Australie', children=[  # Carte des attaques en Australie
                html.Div([dcc.Graph(id='graph_aus_map', figure=fig_aus)])
            ]),
            dcc.Tab(id='tab9', label='Carte de l\'Afrique du Sud', children=[  # Carte des attaques en Afrique du Sud
                html.Div([dcc.Graph(id='graph_sa_map', figure=fig_sa)])
            ]),
            dcc.Tab(id='tab10', label='Carte du Monde', children=[  # Carte des attaques dans le monde
                html.Div([dcc.Graph(id='graph_world_map', figure=fig_world)])
            ])
        ])
    ])
