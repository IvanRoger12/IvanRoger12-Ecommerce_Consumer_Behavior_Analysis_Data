
import streamlit as st

# Injection du style CSS personnalisé
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

import pandas as pd
import plotly.express as px

st.set_page_config(page_title="👑 Fidélité & Satisfaction", layout="wide")

# Chargement et préparation des données
@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")
    df['Purchase_Amount'] = df['Purchase_Amount'].replace('[\$,]', '', regex=True).astype(float)
    df['Time_of_Purchase'] = pd.to_datetime(df['Time_of_Purchase'], errors='coerce')
    df['Month'] = df['Time_of_Purchase'].dt.strftime('%B %Y')
    return df

df = load_data()

# Filtres latéraux essentiels
with st.sidebar:
    st.markdown("## 🔍 Filtres")

    # Genre
    genre_options = df['Gender'].dropna().unique().tolist()
    selected_genres = st.multiselect("Genre", genre_options, default=genre_options, key="genre_filter")

    # Appareil utilisé
    device_options = df['Device_Used_for_Shopping'].dropna().unique().tolist()
    selected_devices = st.multiselect("Appareil utilisé", device_options, default=device_options, key="device_filter")

# Application des filtres
df = df[
    df['Gender'].isin(selected_genres) &
    df['Device_Used_for_Shopping'].isin(selected_devices)
]


st.title("👑 Fidélité & Satisfaction Client")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Taux de fidélité", f"{df['Customer_Loyalty_Program_Member'].mean()*100:.1f}%")
col2.metric("Satisfaction moyenne", f"{df['Customer_Satisfaction'].mean():.1f} / 10")
col3.metric("Achats fidélité", f"{df[df['Customer_Loyalty_Program_Member']==True]['Purchase_Amount'].sum():,.0f} €")

st.markdown("---")

# Graphique 1 : Satisfaction par catégorie
st.subheader("📦 Satisfaction par catégorie d'achat")
fig = px.box(df, x="Purchase_Category", y="Customer_Satisfaction", color="Purchase_Category")
st.plotly_chart(fig, use_container_width=True)

# Graphique 2 : Répartition des membres fidélité
st.subheader("👥 Répartition des clients fidèles vs non fidèles")
fidelite_counts = df['Customer_Loyalty_Program_Member'].value_counts().reset_index()
fidelite_counts.columns = ['Fidèle', 'Nombre']
fidelite_counts['Fidèle'] = fidelite_counts['Fidèle'].map({True: "Membre", False: "Non membre"})

fig2 = px.pie(fidelite_counts, values='Nombre', names='Fidèle', hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig2, use_container_width=True)

# Graphique 3 : Satisfaction selon fidélité
st.subheader("💬 Satisfaction selon le statut fidélité")
fig3 = px.histogram(df, x="Customer_Satisfaction", color="Customer_Loyalty_Program_Member",
                    barmode='overlay', nbins=10,
                    labels={"Customer_Loyalty_Program_Member": "Fidèle"},
                    color_discrete_map={True: "#2ECC71", False: "#E74C3C"})
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.markdown("<center>💙 Fidélité & satisfaction au cœur de la stratégie client</center>", unsafe_allow_html=True)
