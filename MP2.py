import streamlit as st
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import wikipedia

# Streamlit applikation header
st.title("🍷 Vin Data Explorer med PCA")
st.write("Upload en Excel-fil med vin-data for at analysere og visualisere det i 2D og 3D.")

# Filupload funktion
uploaded_file = st.file_uploader("Vælg en Excel-fil", type="xlsx")

if uploaded_file is not None:
    try:
        # Læser data fra Excel-fil
        df = pd.read_excel(uploaded_file)  
        st.write("Eksempel på data:", df.head())

        # Forbereder data: Vælger kun de numeriske kolonner
        vin_data_numeric = df.select_dtypes(include=['float64', 'int64'])

        # Standardisering af de numeriske data
        scaler = StandardScaler()
        vin_data_scaled = scaler.fit_transform(vin_data_numeric)

        # PCA transformation til 3 komponenter
        pca = PCA(n_components=3)
        vin_pca = pca.fit_transform(vin_data_scaled)
        pca_df = pd.DataFrame(vin_pca, columns=["PCA1", "PCA2", "PCA3"])

        # Tilføjer kvalitetskolonnen (hvis den findes) til pca_df for farvekodning
        if 'quality' in df.columns:
            pca_df["quality"] = df["quality"]

        # 2D visualisering
        st.subheader("2D PCA-visualisering")
        fig2d = px.scatter(pca_df, x="PCA1", y="PCA2", color="quality")
        st.plotly_chart(fig2d)

        # 3D visualisering
        st.subheader("3D PCA-visualisering")
        fig3d = px.scatter_3d(pca_df, x="PCA1", y="PCA2", z="PCA3", color="quality")
        st.plotly_chart(fig3d)

        # Tilføjer Wikipedia information om vinens kvalitet
        try:
            # Henter artikel om vinens kvalitet fra Wikipedia
            wine_quality_info = wikipedia.page("Wine_quality").content
            st.subheader("Information om vinens kvalitet")
            # Viser hele artiklen (eller en del af den)
            st.write(wine_quality_info)
        except wikipedia.exceptions.DisambiguationError as e:
            st.error(f"Fejl: Wikipedia kunne ikke finde præcise resultater for vinens kvalitet. Forsøg at søge på en specifik vin.")
        except wikipedia.exceptions.HTTPTimeoutError:
            st.error("Fejl: Tid udløb under hentning af Wikipedia-artikel.")
        
    except Exception as e:
        st.error(f"Der opstod en fejl under filbehandling: {str(e)}")