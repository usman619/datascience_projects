import streamlit as st
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
- **Python libraries:** base64, pandas, streamlit
- **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.header('Display Player Stats of Selected Team')
st.sidebar.header('User Input Feature')
selected_year = st.sidebar.select_slider('Year',list(reversed(range(1950,2025))))

@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url,header=0)
    df = html[0]
    df = df.fillna(0)
    player_stats = df.drop(['Rk'],axis=1)

    return player_stats
