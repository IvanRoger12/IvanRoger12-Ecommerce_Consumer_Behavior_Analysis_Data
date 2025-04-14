
import streamlit as st
import pandas as pd

# Lecture des données
df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")

# Affichage du header stylisé
with st.container():
    st.markdown("""
        <div style="background-color:#2c3e50; padding:30px; border-radius:10px">
            <h1 style="color:white; text-align:center;">
                <img src="https://img.icons8.com/color/48/000000/combo-chart--v1.png" width="50"/>
                Tableau de bord – Accueil
            </h1>
        </div>
    """, unsafe_allow_html=True)

# Exemple de KPI
col1, col2, col3 = st.columns(3)
col1.metric("Total des achats", "275,064 €")
col2.metric("Satisfaction moyenne", "5.4 / 10")
col3.metric("Clients Fidèles", "49.1 %")

st.markdown("### 👋 Merci de tester ce dashboard ! Vous pouvez explorer les onglets pour plus d’analyses.")
