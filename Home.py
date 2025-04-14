
import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="Accueil – SmartClient",
    page_icon="📊",
    layout="wide"
)

# Appliquer le style CSS personnalisé
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Barre de progression pendant le chargement
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

# Filtres dans la sidebar
st.sidebar.header("🔎 Filtres")
genre = st.sidebar.multiselect("Genre", df["Gender"].unique(), default=list(df["Gender"].unique()))
appareil = st.sidebar.multiselect("Appareil utilisé", df["Device_Used_for_Shopping"].unique(), default=list(df["Device_Used_for_Shopping"].unique()))
fidelite = st.sidebar.selectbox("Membre Fidélité", ["Tous", "Oui", "Non"])

if fidelite == "Oui":
    df = df[df["Customer_Loyalty_Program_Member"] == True]
elif fidelite == "Non":
    df = df[df["Customer_Loyalty_Program_Member"] == False]

df = df[df["Gender"].isin(genre) & df["Device_Used_for_Shopping"].isin(appareil)]

# Titre de la page
st.markdown("""<div style='background-color:#2C3E50; padding:2rem; border-radius:16px; color:white; text-align:center; margin-bottom:2rem; border:2px solid #2C3E50; box-shadow:0 8px 20px rgba(0,0,0,0.2); font-size:2rem;'><h1>📊 Analyse Comportementale – E-commerce</h1></div>""", unsafe_allow_html=True)

# KPI Cards animées
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'''
        <div class="metric-card kpi-animated">
            <div class="metric-value">{df['Purchase_Amount'].sum():,.0f} €</div>
            <div class="metric-label">Total des achats</div>
        </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
        <div class="metric-card kpi-animated">
            <div class="metric-value">{df['Customer_Satisfaction'].mean():.1f} / 10</div>
            <div class="metric-label">Satisfaction moyenne</div>
        </div>
    ''', unsafe_allow_html=True)

with col3:
    taux_fidelite = df["Customer_Loyalty_Program_Member"].mean() * 100
    st.markdown(f'''
        <div class="metric-card kpi-animated">
            <div class="metric-value">{taux_fidelite:.1f} %</div>
            <div class="metric-label">Clients Fidèles</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# Graphique évolutif par mois
st.subheader("🎞️ Animation des achats par région (évolution mensuelle)")
df_anim = df.groupby(['YearMonth', 'Location'])['Purchase_Amount'].sum().reset_index()
fig_anim = px.bar(df_anim, x='Location', y='Purchase_Amount',
                  animation_frame='YearMonth',
                  range_y=[0, df_anim['Purchase_Amount'].max()*1.1],
                  title="Évolution mensuelle des achats par région",
                  labels={'Purchase_Amount': 'Montant (€)', 'Location': 'Région'})
st.plotly_chart(fig_anim, use_container_width=True)

# Autres graphiques classiques
st.subheader("📱 Satisfaction par appareil")
fig2 = px.box(df, x="Device_Used_for_Shopping", y="Customer_Satisfaction", color="Device_Used_for_Shopping")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("💳 Méthodes de paiement")
fig3 = px.pie(df, names="Payment_Method", title="Répartition des Méthodes de Paiement")
st.plotly_chart(fig3, use_container_width=True)

st.subheader("🌍 Régions les plus dépensières")
top_region = df.groupby("Location")["Purchase_Amount"].sum().sort_values(ascending=False).head(10).reset_index()
fig4 = px.bar(top_region, x="Purchase_Amount", y="Location", orientation="h", title="Top 10 Régions")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("<div class='footer'>💙 Conçu avec passion – SmartClient 2025</div>", unsafe_allow_html=True)
