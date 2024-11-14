import pandas as pd


def filtration_df(df):
    # Renommer les colonnes pour supprimer les espaces superflus à la fin des noms
    df = df.rename(columns={'Species ': 'Species'})  # Retirer l'espace après la colonne "Species"
    df = df.rename(columns={'Sex ': 'Sex'})  # Retirer l'espace après la colonne "Sex"
    
    # Supprimer les lignes où toutes les valeurs sont NaN
    df = df.dropna(how='all')
    
    # Afficher les premières valeurs des colonnes "Fatal (Y/N)" et "Age" pour vérification
    print(df['Fatal (Y/N)'].head())
    print(df['Age'].head())
    
    # Convertir la colonne "Year" en numérique, les valeurs non numériques deviennent NaN
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Remplacer les NaN dans la colonne "Year" par 0 et convertir la colonne en entier
    df['Year'] = df['Year'].fillna(0).astype(int)
    
    # Filtrer les années avant 1800
    df = df[df['Year'] >= 1800]
    
    # Modification des valeurs dans la colonne "Sex"
    # Remplir d'abord les valeurs NaN par "Unknown"
    df['Sex'] = df['Sex'].fillna("Unknown")
    # Remplacer les valeurs correspondant à "M" ou "M " par "Male"
    df.loc[df['Sex'].str.contains("M|M "), 'Sex'] = "Male"
    # Remplacer les valeurs correspondant à "F" ou "F " par "Female"
    df.loc[df['Sex'].str.contains("F|F "), 'Sex'] = "Female"
    # Tout autre valeur dans "Sex" devient "Unknown"
    df.loc[~df['Sex'].str.contains("Male|Female"), 'Sex'] = "Unknown"
    
    # Création d'un DataFrame pour les activités
    df_Activity = df.copy()
    df_Activity = df_Activity.dropna(subset=['Activity'])  # Supprimer les lignes sans activité
    # Regrouper les différents types de pêche sous la même catégorie "Fishing"
    df_Activity.loc[df_Activity['Activity'].str.contains('fishing|Fishing', case=False), 'Activity'] = 'Fishing'
    # Regrouper les différents types de plongée sous la même catégorie "Diving"
    df_Activity.loc[df_Activity['Activity'].str.contains('diving|Diving', case=False), 'Activity'] = 'Diving'
    
    # Compter le nombre d'attaques par année
    counts_per_year = df['Year'].value_counts().sort_index()
    df_Year = counts_per_year.reset_index()
    df_Year.columns = ['Year', 'Attacks']  # Renommer les colonnes pour plus de clarté
    
    # Création d'un DataFrame pour les espèces
    df_Species = df.copy()
    df_Species = df_Species.dropna(subset=['Species'])  # Supprimer les lignes sans espèce
    # Regrouper les différentes écritures de certaines espèces sous un même nom
    df_Species.loc[df_Species['Species'].str.contains('white shark|White shark', case=False), 'Species'] = 'White shark'
    df_Species.loc[df_Species['Species'].str.contains('tiger shark|Tiger shark', case=False), 'Species'] = 'Tiger shark'
    df_Species.loc[df_Species['Species'].str.contains('6\'|1.8 m', case=False), 'Species'] = '1.8m shark'
    df_Species.loc[df_Species['Species'].str.contains('Zambesi|zambesi', case=False), 'Species'] = 'Zambesi shark'
    df_Species.loc[df_Species['Species'].str.contains('bronze|Bronze', case=False), 'Species'] = 'Bronze whaler shark'
    df_Species.loc[df_Species['Species'].str.contains('5\'|1.5 m', case=False), 'Species'] = '1.5m shark'
    df_Species.loc[df_Species['Species'].str.contains('4\'|1.2 m', case=False), 'Species'] = '1.2m shark'
    df_Species.loc[df_Species['Species'].str.contains('12\'|3.7 m', case=False), 'Species'] = '3.7m shark'
    df_Species.loc[df_Species['Species'].str.contains('3\'|0.9 m', case=False), 'Species'] = '0.9m shark'
    df_Species.loc[df_Species['Species'].str.contains('8\'|2.4 m', case=False), 'Species'] = '2.4m shark'
    df_Species.loc[df_Species['Species'].str.contains('10\'|3 m', case=False), 'Species'] = '3m shark'
    df_Species.loc[df_Species['Species'].str.contains('2 m', case=False), 'Species'] = '2m shark'
    df_Species.loc[df_Species['Species'].str.contains('not confirmed|unconfirmed', case=False), 'Species'] = None
    
    # Retourner les DataFrames nettoyés
    return df, df_Activity, df_Year, df_Species


# Fonction pour nettoyer l'heure (format 24h ou termes comme "midday", "morning")
def clean_time(time_str):
    time_str = str(time_str).lower()  # Convertir en minuscule pour uniformité
    if 'h' in time_str:  # Si l'heure contient un "h", conserver uniquement l'heure
        time_str = time_str.split('h')[0]
    if time_str.isdigit() and len(time_str) == 1:  # Si c'est un chiffre unique, ajouter un zéro devant
        time_str = time_str.zfill(2)
    if 'midday' in time_str:  # Si c'est "midday", mettre "12"
        time_str = '12'
    if 'noon' in time_str:  # Si c'est "noon", mettre "afternoon"
        time_str = 'afternoon'
    if 'morning' in time_str:  # Si c'est "morning", mettre "morning"
        time_str = 'morning'
    if len(time_str) == 4 and time_str.isdigit():  # Si l'heure est au format "HHmm", ne garder que l'heure
        time_str = time_str[:2]

    return time_str


# Fonction pour catégoriser l'heure en "night", "morning", "afternoon" ou "evening"
def categorize_time(time_str):
    if time_str.isdigit():
        hour = int(time_str)  # Convertir l'heure en entier
        if 0 <= hour < 6:
            return "night"  # De 0 à 5 heures, c'est la nuit
        elif 6 <= hour < 12:
            return "morning"  # De 6 à 11 heures, c'est le matin
        elif 12 <= hour < 18:
            return "afternoon"  # De 12 à 17 heures, c'est l'après-midi
        elif 18 <= hour < 24:
            return "evening"  # De 18 à 23 heures, c'est le soir
    else:
        return time_str  # Si l'heure n'est pas un chiffre, retourner telle quelle
