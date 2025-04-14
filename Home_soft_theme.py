
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SmartClient – Accueil",
    page_icon="🌸",
    layout="wide"
)

# CSS pour un thème doux et élégant
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f6f9fc;
        }
        .block-container {
            padding-top: 2rem;
        }
        h1 {
            color: #2c3e50;
            font-size: 40px;
        }
        .kpi {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
            margin-bottom: 10px;
        }
        .footer {
            text-align: center;
            padding: 1rem;
            font-size: 13px;
            color: #95a5a6;
        }
    </style>
""", unsafe_allow_html=True)

# Charger les données
@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")
    df['Purchase_Amount'] = df['Purchase_Amount'].replace('[\$,]', '', regex=True).astype(float)
    df['Time_of_Purchase'] = pd.to_datetime(df['Time_of_Purchase'], errors='coerce')
    df['Month'] = df['Time_of_Purchase'].dt.strftime('%b %Y')
    return df

df = load_data()

st.title("🌸 Bienvenue sur SmartClient Dashboard")

st.markdown("Analysez les comportements d'achat de vos clients avec des visuels doux et puissants 🎯")

# KPIs avec thème doux
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Total Achats", f"{df['Purchase_Amount'].sum():,.0f} €")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    st.metric("Clients uniques", df['Customer_ID'].nunique())
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="kpi">', unsafe_allow_html=True)
    taux_fidelite = df['Customer_Loyalty_Program_Member'].mean() * 100
    st.metric("Fidélité", f"{taux_fidelite:.1f} %")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# Graphique doux : achats par mois
st.subheader("📈 Évolution des ventes")
monthly = df.groupby('Month')['Purchase_Amount'].sum().reset_index()
fig = px.area(
    monthly, x='Month', y='Purchase_Amount',
    labels={'Purchase_Amount': 'Montants (€)', 'Month': 'Mois'},
    title="Achats mensuels",
    color_discrete_sequence=["#A3CEF1"]
)
st.plotly_chart(fig, use_container_width=True)

# Satisfaction moyenne par appareil
st.subheader("📱 Satisfaction par type d'appareil")
fig2 = px.box(df, x='Device_Used_for_Shopping', y='Customer_Satisfaction',
              color='Device_Used_for_Shopping',
              color_discrete_sequence=px.colors.sequential.Teal_r)
st.plotly_chart(fig2, use_container_width=True)

# Footer doux
st.markdown("<div class='footer'>Design doux avec 💙 par Ivan Nfinda</div>", unsafe_allow_html=True)
