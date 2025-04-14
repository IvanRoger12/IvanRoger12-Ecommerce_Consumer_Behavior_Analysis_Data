
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🎯 Ciblage & Recommandations", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")
    df['Purchase_Amount'] = df['Purchase_Amount'].replace('[\$,]', '', regex=True).astype(float)
    df['Time_of_Purchase'] = pd.to_datetime(df['Time_of_Purchase'], errors='coerce')
    df['Month'] = df['Time_of_Purchase'].dt.strftime('%B %Y')
    return df

df = load_data()


st.markdown("<div class='title-container'><h1>🎯 Ciblage & Recommandations</h1></div>", unsafe_allow_html=True)


# Score simple basé sur achat + satisfaction
df['EngagementScore'] = (df['Purchase_Amount'] / df['Purchase_Amount'].max()) * 0.6 + (df['Customer_Satisfaction'] / 10) * 0.4
df['EngagementScore'] = df['EngagementScore'] * 100

def segmenter(score):
    if score > 80:
        return "Champions"
    elif score > 60:
        return "Fidèles"
    elif score > 40:
        return "À potentiel"
    else:
        return "À réactiver"

df['Segment'] = df['EngagementScore'].apply(segmenter)

st.subheader("📌 Répartition des segments clients")
seg_counts = df['Segment'].value_counts().reset_index()
seg_counts.columns = ['Segment', 'Nombre']
fig = px.bar(seg_counts, x='Segment', y='Nombre', color='Segment', text_auto=True,
             color_discrete_map={
                 "Champions": "#2ECC71",
                 "Fidèles": "#3498DB",
                 "À potentiel": "#F1C40F",
                 "À réactiver": "#E74C3C"
             })
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 💡 Recommandations par segment")
segments = ["Champions", "Fidèles", "À potentiel", "À réactiver"]

recos = {
    "Champions": ["Offres exclusives VIP", "Programme de parrainage", "Produits en avant-première"],
    "Fidèles": ["Récompenses de fidélité", "Cross-selling ciblé", "Emails personnalisés"],
    "À potentiel": ["Incitations à acheter", "Offres de bienvenue", "Gamification de l’achat"],
    "À réactiver": ["Campagnes de relance", "Promotions fortes", "Sondage de feedback"]
}

for seg in segments:
    with st.expander(f"🔍 {seg}"):
        for action in recos[seg]:
            st.markdown(f"- ✅ {action}")

st.markdown("---")
st.subheader("💬 Satisfaction par segment")
fig2 = px.box(df, x='Segment', y='Customer_Satisfaction', color='Segment',
              color_discrete_map={
                  "Champions": "#2ECC71",
                  "Fidèles": "#3498DB",
                  "À potentiel": "#F1C40F",
                  "À réactiver": "#E74C3C"
              })
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.markdown("<center>🚀 Des actions concrètes basées sur l'engagement et la satisfaction</center>", unsafe_allow_html=True)


st.markdown("---")
st.subheader("📊 Répartition des segments par genre")
fig_genre = px.histogram(df, x="Gender", color="Segment", barmode="group")
st.plotly_chart(fig_genre, use_container_width=True)

st.subheader("🎯 Taux d'utilisation des promotions par segment")
promo_segment = df.groupby("Segment")["Discount_Used"].mean().reset_index()
promo_segment["Discount_Used"] = promo_segment["Discount_Used"] * 100
fig_promo = px.bar(promo_segment, x="Segment", y="Discount_Used", text_auto=True,
                   labels={"Discount_Used": "Utilisation des promotions (%)"})
st.plotly_chart(fig_promo, use_container_width=True)

st.subheader("⏱️ Délai moyen entre achats par segment")

# Trier et calculer la différence
df_sorted = df.sort_values(by=["Customer_ID", "Time_of_Purchase"])
df_sorted["TimeDiff"] = df_sorted.groupby("Customer_ID")["Time_of_Purchase"].diff().dt.days

# Ne garder que les clients avec au moins 2 achats
df_filtered = df_sorted.dropna(subset=["TimeDiff"])

# Calcul de la moyenne par segment
moyenne_deltas = df_filtered.groupby("Segment")["TimeDiff"].mean().reset_index()
moyenne_deltas["TimeDiff"] = moyenne_deltas["TimeDiff"].round(1)

fig_delta = px.bar(moyenne_deltas, x="Segment", y="TimeDiff", text_auto=True,
                   labels={"TimeDiff": "Délai moyen (jours)"})
st.plotly_chart(fig_delta, use_container_width=True)
df_sorted = df.sort_values(["Customer_ID", "Time_of_Purchase"])
df_sorted["TimeDiff"] = df_sorted.groupby("Customer_ID")["Time_of_Purchase"].diff().dt.days
moyenne_deltas = df_sorted.groupby("Segment")["TimeDiff"].mean().reset_index()
fig_delta = px.bar(moyenne_deltas, x="Segment", y="TimeDiff", text_auto=True,
                   labels={"TimeDiff": "Délai moyen (jours)"})
st.plotly_chart(fig_delta, use_container_width=True)
