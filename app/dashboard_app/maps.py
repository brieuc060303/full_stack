import plotly.express as px
import json
import pandas as pd

def worlGraph(df):
    # Comptage du nombre d'attaques par pays
    byCountry_count = df['Country'].value_counts().reset_index().rename(columns={'Country':'Count','index':'Country'}) 
    
    # Création de la carte choroplèthe pour le monde
    fig = px.choropleth(data_frame = byCountry_count,
                        locations = 'Country',
                        color='Count',  # La couleur dépend du nombre d'attaques
                        color_continuous_scale="Viridis",  # Choix de l'échelle de couleur
                        locationmode = 'country names',  # Mode des pays
                        scope = 'world',  # Carte du monde
                        title = 'Shark Attack around the World')  # Titre du graphique

    # Mise à jour du style de la carte
    fig.update_layout(
                    plot_bgcolor='rgba(252,248,244,1.00)',  # Couleur de fond du graphique
                    paper_bgcolor='cornsilk',  # Couleur de fond du papier
                    font = dict(
                        family = "Montserrat",  # Police d'écriture
                        size = 18,  # Taille de la police
                        color = 'black'  # Couleur de la police
                        )
            )
    return fig

def usaGraph(df):
    # Filtrer les données pour les USA
    byAreaUS_count = df[df['Country'] == "USA"]['Area'].value_counts().reset_index().rename(columns={'Area':'Count','index':'Area'})

    # Dictionnaire pour faire correspondre les états aux codes des États-Unis
    states_code = {'Alabama': 'AL','Alaska': 'AK','Arizona': 'AZ','Arkansas': 'AR','California': 'CA',
                'Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC',
                'Florida': 'FL','Georgia': 'GA','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL','Indiana': 'IN',
                'Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME','Maryland': 'MD',
                'Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS','Missouri': 'MO',
                'Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH','New Jersey': 'NJ',
                'New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND','Ohio': 'OH',
                'Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA','Rhode Island': 'RI','South Carolina': 'SC',
                'South Dakota': 'SD','Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT','Virginia': 'VA',
                'Washington': 'WA','West Virginia': 'WV','Wisconsin': 'WI','Wyoming': 'WY'}

    # Ajout des codes des états au dataframe
    byAreaUS_count['State Code'] = byAreaUS_count['Area'].map(states_code)

    # Création de la carte choroplèthe pour les USA
    fig = px.choropleth(data_frame = byAreaUS_count,
                        locations = 'State Code',
                        color='Count',  # Couleur selon le nombre d'attaques
                        color_continuous_scale="Viridis",  # Choix de l'échelle de couleur
                        locationmode = 'USA-states',  # Carte par états
                        scope = 'usa',  # Carte des États-Unis
                        title = 'Shark Attacks in the USA',  # Titre du graphique
                        hover_name = 'Area')  # Affichage des noms des régions au survol

    # Mise à jour du style de la carte
    fig.update_layout(
                    plot_bgcolor='rgba(252,248,244,1.00)',  # Couleur de fond du graphique
                    paper_bgcolor='cornsilk',  # Couleur de fond du papier
                    font = dict(
                        family = "Montserrat",  # Police d'écriture
                        size = 18,  # Taille de la police
                        color = 'black'  # Couleur de la police
                        )
            )

    return fig

def australiaGraph(df):
    # Chargement du fichier GeoJSON pour la carte de l'Australie
    with open('/app/dashboard_app/ressources/states_australia.geojson', 'r') as file:
        aus_map = json.load(file)
    
    # Comptage des attaques par région en Australie
    byAreaAUS_count = df[df['Country'] == "AUSTRALIA"]['Area'].value_counts().reset_index().rename(columns={'Area':'Count','index':'Area'})

    # Création de la carte choroplèthe pour l'Australie
    fig = px.choropleth(byAreaAUS_count,
                        geojson=aus_map,  # Utilisation du fichier GeoJSON
                        locations='Area',  # Colonnes avec les régions
                        color='Count',  # Couleur selon le nombre d'attaques
                        color_continuous_scale="Viridis",  # Choix de l'échelle de couleur
                        featureidkey="properties.STATE_NAME",  # Clé pour lier les régions
                        title = 'Shark Attack in Australia')  # Titre du graphique

    # Mise à jour des propriétés de la carte
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":10})
    fig.update_geos(fitbounds="locations", visible=False)  # Ajuste la carte selon les régions présentes dans le dataset
    fig.update_layout(
                    plot_bgcolor='rgba(252,248,244,1.00)',  # Couleur de fond du graphique
                    paper_bgcolor='cornsilk',  # Couleur de fond du papier
                    font = dict(
                        family = "Montserrat",  # Police d'écriture
                        size = 18,  # Taille de la police
                        color = 'black'  # Couleur de la police
                        )
            )
    return fig

def africaGraph(df):
    # Chargement du fichier GeoJSON pour la carte de l'Afrique du Sud
    with open('/app/dashboard_app/ressources/states_south_africa.json', 'r') as file:
        sa_map = json.load(file)
    
    # Comptage des attaques par province en Afrique du Sud
    byAreaSA_count = df[df['Country'] == "SOUTH AFRICA"]['Area'].value_counts().reset_index().rename(columns={'Area':'Count','index':'Area'})

    # Dictionnaire pour renommer les provinces
    mapping = {
        'Western Cape Province': 'Western Cape',
        'Eastern Cape Province': 'Eastern Cape',
        'Western Province': 'Western Cape',
        'Eastern Province': 'Eastern Cape',
        'KwaZulu-Natal between Port Edward and Port St': 'KwaZulu-Natal',
    }

    # Ajout des régions sans attaques avec un compte de 0
    other_regions = [
        {'Area': 'Free State', 'Count': 0},
        {'Area': 'Gauteng', 'Count': 0},
        {'Area': 'Limpopo', 'Count': 0},
        {'Area': 'Mpumalanga', 'Count': 0},
        {'Area': 'North West', 'Count': 0},
        {'Area': 'Northern Cape', 'Count': 0},
    ]

    other_regions_df = pd.DataFrame(other_regions)
    byAreaSA_count = pd.concat([byAreaSA_count, other_regions_df], ignore_index=True)

    # Renommage des régions avec le dictionnaire
    byAreaSA_count['Area'] = byAreaSA_count['Area'].apply(lambda x: mapping.get(x, x))
    byAreaSA_count = byAreaSA_count.groupby('Area', as_index=False)['Count'].sum()

    # Création de la carte choroplèthe pour l'Afrique du Sud
    fig = px.choropleth(byAreaSA_count,
                    geojson=sa_map,  # Utilisation du fichier GeoJSON
                    locations='Area',  # Colonnes avec les régions
                    color='Count',  # Couleur selon le nombre d'attaques
                    color_continuous_scale="Viridis",  # Choix de l'échelle de couleur
                    featureidkey="properties.PROVINCE",  # Clé pour lier les régions
                    hover_name='Area',  # Affichage des noms des régions au survol
                    )
    fig.update_geos(fitbounds="locations", visible=False)  # Affichage uniquement des régions présentes dans les données
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":10})  # Suppression des marges autour de la carte
    fig.update_layout(
                    plot_bgcolor='rgba(252,248,244,1.00)',  # Couleur de fond du graphique
                    paper_bgcolor='cornsilk',  # Couleur de fond du papier
                    font = dict(
                        family = "Montserrat",  # Police d'écriture
                        size = 18,  # Taille de la police
                        color = 'black'  # Couleur de la police
                        )
            )
    return fig
