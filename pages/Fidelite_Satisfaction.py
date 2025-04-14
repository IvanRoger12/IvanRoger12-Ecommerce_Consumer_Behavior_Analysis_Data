
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="👑 Fidélité & Satisfaction", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("Ecommerce_Consumer_Behavior_Analysis_Data.csv")
    df['Purchase_Amount'] = df['Purchase_Amount'].replace('[\$,]', '', regex=True).astype(float)
    df['Time_of_Purchase'] = pd.to_datetime(df['Time_of_Purchase'], errors='coerce')
    df['Month'] = df['Time_of_Purchase'].dt.strftime('%B %Y')
    return df

df = load_data()


st.markdown("<div class='title-container'><h1>👑 Fidélité & Satisfaction Client</h1></div>", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)
col1.metric("Taux de fidélité", f"{df['Customer_Loyalty_Program_Member'].mean()*100:.1f}%")
col2.metric("Satisfaction moyenne", f"{df['Customer_Satisfaction'].mean():.1f} / 10")
col3.metric("Achats fidélité", f"{df[df['Customer_Loyalty_Program_Member']==True]['Purchase_Amount'].sum():,.0f} €")

st.markdown("---")

st.subheader("📦 Satisfaction par catégorie d'achat")
fig = px.box(df, x="Purchase_Category", y="Customer_Satisfaction", color="Purchase_Category")
st.plotly_chart(fig, use_container_width=True)

st.subheader("👥 Répartition des clients fidèles vs non fidèles")
fidelite_counts = df['Customer_Loyalty_Program_Member'].value_counts().reset_index()
fidelite_counts.columns = ['Fidèle', 'Nombre']
fidelite_counts['Fidèle'] = fidelite_counts['Fidèle'].map({True: "Membre", False: "Non membre"})

fig2 = px.pie(fidelite_counts, values='Nombre', names='Fidèle', hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("💬 Satisfaction selon le statut fidélité")
fig3 = px.histogram(df, x="Customer_Satisfaction", color="Customer_Loyalty_Program_Member",
                    barmode='overlay', nbins=10,
                    labels={"Customer_Loyalty_Program_Member": "Fidèle"},
                    color_discrete_map={True: "#2ECC71", False: "#E74C3C"})
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.markdown("<center>💙 Fidélité & satisfaction au cœur de la stratégie client</center>", unsafe_allow_html=True)


st.markdown("---")
st.subheader("📈 Évolution mensuelle du taux de fidélité")
df["Month"] = df["Time_of_Purchase"].dt.to_period("M").astype(str)
monthly_loyalty = df.groupby("Month")["Customer_Loyalty_Program_Member"].mean().reset_index()
monthly_loyalty["Customer_Loyalty_Program_Member"] *= 100
fig_loyalty = px.line(monthly_loyalty, x="Month", y="Customer_Loyalty_Program_Member",
                      markers=True,
                      labels={"Customer_Loyalty_Program_Member": "Taux de fidélité (%)"},
                      title="Taux de fidélité par mois")
fig_loyalty.update_traces(line=dict(width=3), marker=dict(size=8))
st.plotly_chart(fig_loyalty, use_container_width=True)

st.subheader("🧲 Corrélation Satisfaction / Fidélité")
fig_corr = px.violin(df, y="Customer_Satisfaction", color="Customer_Loyalty_Program_Member",
                     box=True, points="all",
                     labels={"Customer_Loyalty_Program_Member": "Fidèle"})
st.plotly_chart(fig_corr, use_container_width=True)

st.subheader("💎 Top 10 clients fidèles les plus rentables")
top_fideles = df[df["Customer_Loyalty_Program_Member"] == True].groupby("Customer_ID")["Purchase_Amount"].sum().sort_values(ascending=False).head(10).reset_index()
fig_top = px.bar(top_fideles, x="Customer_ID", y="Purchase_Amount", text_auto=True,
                 labels={"Purchase_Amount": "Montant total (€)", "Customer_ID": "Client"})
fig_top.update_traces(marker_color="#3498DB")
st.plotly_chart(fig_top, use_container_width=True)
