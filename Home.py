
import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="Accueil – Analyse Comportementale E-commerce",
    page_icon="📊",
    layout="wide"
)

# Titre avec style intégré
st.markdown("""<div style='background-color:#2C3E50;
                padding:2rem;
                border-radius:16px;
                color:white;
                text-align:center;
                margin-bottom:2rem;
                border:2px solid #2C3E50;
                box-shadow:0 8px 20px rgba(0,0,0,0.2);
                font-size:2rem;'>
<h1>📊 Analyse Comportementale – E-commerce</h1>
</div>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")
    df['Purchase_Amount'] = df['Purchase_Amount'].replace('[\$,]', '', regex=True).astype(float)
    df['Time_of_Purchase'] = pd.to_datetime(df['Time_of_Purchase'], errors='coerce')
    df['Month'] = df['Time_of_Purchase'].dt.strftime('%b %Y')
    df['YearMonth'] = df['Time_of_Purchase'].dt.to_period('M').astype(str)
    return df

with st.spinner("📦 Chargement des données..."):
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.005)
        my_bar.progress(percent_complete + 1)
    df = load_data()

# KPIs
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Achats", f"{df['Purchase_Amount'].sum():,.0f} €")
with col2:
    st.metric("Satisfaction Moyenne", f"{df['Customer_Satisfaction'].mean():.1f} / 10")
with col3:
    loyal_rate = df["Customer_Loyalty_Program_Member"].mean() * 100
    st.metric("Clients Fidèles", f"{loyal_rate:.1f} %")

st.markdown("---")

# Graphique animé
st.subheader("🎞️ Animation des achats par région (évolution mensuelle)")
df_anim = df.groupby(['YearMonth', 'Location'])['Purchase_Amount'].sum().reset_index()
fig_anim = px.bar(df_anim, x='Location', y='Purchase_Amount',
                  animation_frame='YearMonth',
                  range_y=[0, df_anim['Purchase_Amount'].max()*1.1],
                  title="Évolution mensuelle des achats par région",
                  labels={'Purchase_Amount': 'Montant (€)', 'Location': 'Région'})
st.plotly_chart(fig_anim, use_container_width=True)

st.markdown("---")
st.write("👋 Merci de tester ce dashboard ! Vous pouvez explorer les onglets pour plus d’analyses.")

