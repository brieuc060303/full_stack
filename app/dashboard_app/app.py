from data_processing_dash import filtration_df, clean_time, categorize_time
from graphs import fatalandnot, ageGraph, bySexGraph, hoursGraph, byYearGraph, periodGraph, byActivityGraph
from maps import usaGraph, worlGraph, africaGraph, australiaGraph
from dashboard import create_dashboard
from callbacks import get_callbacks
import dash 
from get_data import get_data
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Initialisation de l'application Dash
app = dash.Dash(__name__)
server = app.server 

# Mapping des colonnes pour correspondre aux noms de colonnes dans l'interface
columns_mapping = {
    'caseNumber': 'Case Number',
    'date': 'Date',
    'year': 'Year',
    'type': 'Type',
    'country': 'Country',
    'area': 'Area',
    'location': 'Location',
    'activity': 'Activity',
    'name': 'Name',
    'sex': 'Sex',
    'age': 'Age',
    'injury': 'Injury',
    'fatal': 'Fatal (Y/N)',
    'time': 'Time',
    'species': 'Species',
    'investigator_or_source': 'Investigator or Source',
    'pdf': 'pdf',
    'href_formula': 'href formula',
    'href': 'href',
    'original_order': 'original order'
}

def update_layout():
    """Met à jour le tableau de bord avec les dernières données de l'application Dash"""
    
    # Récupération des données les plus récentes
    data = get_data()  # Implémentez cette fonction pour obtenir les données actuelles
    
    # Renommage des colonnes selon le mapping
    data = data.rename(columns=columns_mapping)

    # Filtrage et prétraitement des données
    sharks_df, sharks_activity, sharks_year, sharks_species = filtration_df(data)

    # Création des graphiques avec les données filtrées
    fig_year = byYearGraph(sharks_year)
    fig_activity = byActivityGraph(sharks_activity)
    fig_sx = bySexGraph(sharks_df)
    fig_world = worlGraph(sharks_df)
    fig_hours = hoursGraph(sharks_df)
    fig_time_periods = periodGraph(sharks_df)
    fig_age, shark_sorted_df = ageGraph(sharks_df)
    fig_usa = usaGraph(sharks_df)
    fig_aus = australiaGraph(sharks_df)
    fig_sa = africaGraph(sharks_df)
    fig_fatal, fig_not_fatal = fatalandnot(sharks_species)

    # Mise à jour du layout de l'application avec les nouveaux graphiques
    layout = html.Div(id='dashboard-content', style={'backgroundColor': 'cornsilk'}, children=[
        # Bouton pour actualiser les données
        html.Button("Actualiser", id="refresh-button", n_clicks=0),
        dcc.Tabs([  # Différents onglets, chaque onglet pour un graphique
            dcc.Tab(id='tab1', label='Années', children=[  # Graphique: nombre d'attaques par année
                html.Div([
                    dcc.Graph(id='graph1', figure=fig_year),  # Graphique de l'année
                    html.Div(
                        id='description1',
                        children="Le nombre d'attaques de requins par année",  # Description pour cet onglet
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}
                    )
                ])
            ]),
            dcc.Tab(id='tab2', label='Sexe', children=[  # Graphique: nombre d'attaques par sexe
                html.Div([
                    dcc.Graph(id='graph2', figure=fig_sx),
                    html.Div(
                        id='description2',
                        children="La proportion d'attaques de requins par sexe depuis 1800",
                        style={'text-align': 'center', 'font-size': '22px', 'margin-top': '50px'}
                    )
                ])
            ]),
            dcc.Tab(id='tab3', label='Fatalité ou Non', children=[  # Graphique: attaques fatales vs non-fatales
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
            dcc.Tab(id='tab4', label='Activité', children=[  # Graphique: nombre d'attaques par activité humaine
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
            dcc.Tab(id='tab6', label='Attaques par Âge', children=[  # Graphique des attaques par âge
                html.Div([
                    dcc.Graph(id='graph7', figure=fig_age)
                ])
            ]),
            dcc.Tab(id='tab7', label='Carte des USA', children=[  # Carte des attaques aux USA
                html.Div([dcc.Graph(id='graph_usa_map', figure=fig_usa)])
            ]),
            dcc.Tab(id='tab8', label='Carte d’Australie', children=[  # Carte des attaques en Australie
                html.Div([dcc.Graph(id='graph_aus_map', figure=fig_aus)])
            ]),
            dcc.Tab(id='tab9', label='Carte d’Afrique du Sud', children=[  # Carte des attaques en Afrique du Sud
                html.Div([dcc.Graph(id='graph_sa_map', figure=fig_sa)])
            ]),
            dcc.Tab(id='tab10', label='Carte du Monde', children=[  # Carte du monde des attaques
                html.Div([dcc.Graph(id='graph_world_map', figure=fig_world)])
            ])
        ])
    ])

    return layout


# Initialisation des dataFrames pour les différentes données
shark_sorted_df = pd.DataFrame(columns=['Year', 'Age', 'Fatal (Y/N)', 'Country', 'Species', 'Activity'])
sharks_species = pd.DataFrame(columns=['Species', 'Count', 'Fatal (Y/N)'])
sharks_activity = pd.DataFrame(columns=['Activity', 'Count'])
sharks_year = pd.DataFrame(columns=['Year', 'Fatal (Y/N)'])
sharks_df = pd.DataFrame(columns=['Country', 'Year', 'Fatal', 'Sex', 'Age', 'Fatal (Y/N)', 'Location'])

# Initialisation des graphiques avec des figures vides
fig_year = px.line(title='Attaques de requins par année')
fig_sx = px.line(title='Attaques de requins par sexe')
fig_activity = px.line(title='Attaques de requins par activité')
fig_world = px.line(title='Carte mondiale des attaques de requins')
fig_hours = px.line(title='Attaques de requins par heure')
fig_time_periods = px.line(title='Attaques de requins par période')
fig_age = px.line(title='Attaques de requins par âge')
fig_usa = px.line(title='Attaques de requins aux USA')
fig_aus = px.line(title='Attaques de requins en Australie')
fig_sa = px.line(title='Attaques de requins en Afrique du Sud')
fig_fatal = px.line(title = 'Attaques fatales')
fig_not_fatal = px.line(title = 'Attaques non-fatales')

# Création du tableau de bord avec les figures initialisées
create_dashboard(app, fig_year, fig_sx, fig_activity, fig_world, fig_hours, fig_time_periods, fig_age, fig_fatal, fig_not_fatal, fig_usa, fig_aus, fig_sa)

# Lier les callbacks à l'application
get_callbacks(app)

# Lancer le serveur Dash
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
