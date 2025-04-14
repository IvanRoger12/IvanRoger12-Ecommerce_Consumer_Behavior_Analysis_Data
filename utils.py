
import streamlit as st

def afficher_titre(titre):
    st.markdown(f"""
        <div style='background-color:#2C3E50;
                    padding:2rem;
                    border-radius:16px;
                    color:white;
                    text-align:center;
                    margin-bottom:2rem;
                    border:2px solid #2C3E50;
                    box-shadow:0 8px 20px rgba(0,0,0,0.2);
                    font-size:2rem;'>
            <h1>{titre}</h1>
        </div>
    """, unsafe_allow_html=True)
