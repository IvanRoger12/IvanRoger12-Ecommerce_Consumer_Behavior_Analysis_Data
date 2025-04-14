
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



# Filtres latéraux essentiels
with st.sidebar:
    st.markdown("## 🔍 Filtres")

    # Genre
    st.markdown("### Genre")
    genre_options = df['Gender'].dropna().unique().tolist()
    selected_genres = st.multiselect("Genre", genre_options, default=genre_options)

    # Lieu
    st.markdown("### Localisation")
    location_options = df['Location'].dropna().unique().tolist()
    selected_locations = st.multiselect("Localisation", location_options, default=location_options)

    # Appareil utilisé
    st.markdown("### Appareil")
    device_options = df['Device_Used_for_Shopping'].dropna().unique().tolist()
    selected_devices = st.multiselect("Appareil utilisé", device_options, default=device_options)

# Application des filtres
df = df[
    df['Gender'].isin(selected_genres) &
    df['Location'].isin(selected_locations) &
    df['Device_Used_for_Shopping'].isin(selected_devices)
]


# KPIs

# Cartes de résumé stylisées
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div style='border: 2px solid #2C3E50; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; font-weight: bold; color: #2C3E50;'>{df['Purchase_Amount'].sum():,.0f} €</div>
        <div style='color: grey;'>Total des achats</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='border: 2px solid #2C3E50; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; font-weight: bold; color: #2C3E50;'>{df['Customer_Satisfaction'].mean():.1f} / 10</div>
        <div style='color: grey;'>Satisfaction moyenne</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style='border: 2px solid #2C3E50; border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center;'>
        <div style='font-size: 2rem; font-weight: bold; color: #2C3E50;'>{df["Customer_Loyalty_Program_Member"].mean() * 100:.1f} %</div>
        <div style='color: grey;'>Clients Fidèles</div>
    </div>
    """, unsafe_allow_html=True)


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




# Graphique 1 : Méthodes de paiement
st.subheader("💳 Méthodes de paiement")
payment_df = df["Payment_Method"].value_counts(normalize=True).reset_index()
payment_df.columns = ["Méthode", "Proportion"]
fig1 = px.pie(payment_df, names="Méthode", values="Proportion", title="Répartition des Méthodes de Paiement")
st.plotly_chart(fig1, use_container_width=True)

# Graphique 2 : Satisfaction par appareil
st.subheader("📱 Satisfaction par appareil")
fig2 = px.box(df, x="Device_Used_for_Shopping", y="Customer_Satisfaction", color="Device_Used_for_Shopping",
              title="Satisfaction Client par Appareil")
st.plotly_chart(fig2, use_container_width=True)

# Graphique 3 : Achats par mois
st.subheader("📈 Achats par mois")
monthly_df = df.groupby("Month")["Purchase_Amount"].sum().reset_index()
fig3 = px.line(monthly_df, x="Month", y="Purchase_Amount", markers=True,
               title="Achats Mensuels", labels={"Purchase_Amount": "Montant (€)"})
fig3.update_traces(fill="tozeroy")
st.plotly_chart(fig3, use_container_width=True)


st.markdown('👋 Merci de tester ce dashboard ! Vous pouvez explorer les onglets pour plus d’analyses.')