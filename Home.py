import streamlit as st

st.markdown("<style>" + open("styles.css").read() + "</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
        .block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="landing-container">
        <h1 class="glitch" data-text="FINANCES DASHBOARD">FINANCES DASHBOARD</h1>
        <p class="landing-subtitle">Track · Analyse · Control</p>
    </div>
""", unsafe_allow_html=True)

st.image("img.svg", width="stretch")

st.markdown("""
    <div class="landing-buttons">
        <a class="neon-btn neon-btn--blue" href="/Main_Page">Enter Dashboard</a>
        <a class="neon-btn neon-btn--pink" href="/Data_Entry">Add Records</a>
    </div>
""", unsafe_allow_html=True)
