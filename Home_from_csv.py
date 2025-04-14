
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="SmartClient – Dashboard",
    page_icon="📊",
    layout="wide"
)

# Chargement et nettoyage des données
@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")
    df['Purchase_Amount'] = df['Purchase_Amount'].replace('[\$,]', '', regex=True).astype(float)
    df['Time_of_Purchase'] = pd.to_datetime(df['Time_of_Purchase'], errors='coerce')
    df['Month'] = df['Time_of_Purchase'].dt.strftime('%B %Y')
    return df

df = load_data()

# Sidebar – filtres
st.sidebar.title("🎛️ Filtres")
mois = st.sidebar.multiselect("Mois d'achat", df['Month'].dropna().unique(), default=list(df['Month'].dropna().unique()))
appareils = st.sidebar.multiselect("Appareil", df['Device_Used_for_Shopping'].unique(), default=list(df['Device_Used_for_Shopping'].unique()))
methodes = st.sidebar.multiselect("Méthode de paiement", df['Payment_Method'].unique(), default=list(df['Payment_Method'].unique()))

# Filtrage
df_filtre = df[
    (df['Month'].isin(mois)) &
    (df['Device_Used_for_Shopping'].isin(appareils)) &
    (df['Payment_Method'].isin(methodes))
]

# Titre
st.title("📊 Dashboard - Analyse Client & Achats")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("🛒 Total achats", f"{df_filtre['Purchase_Amount'].sum():,.0f} €")
col2.metric("👤 Clients uniques", df_filtre['Customer_ID'].nunique())
col3.metric("🏅 Taux de fidélité", f"{df_filtre['Customer_Loyalty_Program_Member'].mean()*100:.1f}%")

st.markdown("---")

# Graphiques
col1, col2 = st.columns(2)

with col1:
    st.subheader("Répartition par catégorie d'achat")
    cat = df_filtre['Purchase_Category'].value_counts().reset_index()
    cat.columns = ['Catégorie', 'Nombre']
    fig = px.pie(cat, values='Nombre', names='Catégorie', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Répartition des montants par méthode de paiement")
    payment = df_filtre.groupby('Payment_Method')['Purchase_Amount'].sum().reset_index()
    fig2 = px.bar(payment, x='Payment_Method', y='Purchase_Amount', color='Payment_Method', text_auto='.0f')
    st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Appareils utilisés pour le shopping")
    dev = df_filtre['Device_Used_for_Shopping'].value_counts().reset_index()
    dev.columns = ['Appareil', 'Nombre']
    fig3 = px.bar(dev, x='Appareil', y='Nombre', color='Appareil', text_auto=True)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Satisfaction client (moyenne)")
    fig4 = px.histogram(df_filtre, x='Customer_Satisfaction', nbins=10, color_discrete_sequence=['#3498DB'])
    st.plotly_chart(fig4, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<center>Créé avec 💙 par Streamlit – Données réelles</center>", unsafe_allow_html=True)
