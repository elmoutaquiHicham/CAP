import streamlit as st
import pandas as pd
import pydeck as pdk

def convertir_et_nettoyer(df, colonnes):
    for colonne in colonnes:
        # Remplacer les virgules par des points et convertir en float
        df[colonne] = df[colonne].str.replace(',', '.').astype(float)
    return df


# Fonction pour charger les données (ajustez selon votre source de données)
def load_data():
    # Exemple de chargement de données - remplacez par votre propre chargement de données
    df_chantiers = pd.read_csv("deploiment/chantiers.csv", sep = ';')
    df_capteurs = pd.read_csv("deploiment/capteurs.csv", sep = ';')

    return df_chantiers, df_capteurs

# Charger les données
df_chantiers, df_capteurs = load_data()

colonnes_a_convertir = ['latitude', 'longitude']

df_chantiers = convertir_et_nettoyer(df_chantiers, colonnes_a_convertir)

colonnes_a_convertir_ = ['lat', 'lon']
df_capteurs = convertir_et_nettoyer(df_capteurs, colonnes_a_convertir_)

# Configurer la carte
def create_map(df_chantiers, df_capteurs):
    # Créer des couches pour les chantiers et les capteurs
    chantiers_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_chantiers,
        get_position='[longitude, latitude]',
        get_color='[255, 0, 0, 160]',
        get_radius=100,
    )

    capteurs_layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_capteurs,
        get_position='[lon, lat]',
        get_color='[0, 255, 0, 160]',
        get_radius=100,
    )

    # Définir la vue de la carte
    view_state = pdk.ViewState(latitude=df_chantiers['latitude'].mean(), longitude=df_chantiers['longitude'].mean(), zoom=10)

    # Créer et retourner la carte
    return pdk.Deck(layers=[chantiers_layer, capteurs_layer], initial_view_state=view_state)

# Titre de l'application
st.title("Visualisation des chantiers et des capteurs")

# Afficher la carte dans l'application Streamlit
st.pydeck_chart(create_map(df_chantiers, df_capteurs))

if __name__ == "__main__":
    main()
