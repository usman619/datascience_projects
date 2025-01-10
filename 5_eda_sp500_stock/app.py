import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

st.title('EDA SP-500 Stock')
st.markdown("""
This app retrieves list of the **sp500** (S&P 500) stock prices and its corresponding **stock closing** price!
- **Python libraries:** pandas, streamlit, numpy, matplotlib, seaborn
- **Data source:** [Wikipedia](https://www.wikipedia.org).
""")

@st.cache_data
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()

sector = df.groupby('GICS Sector')

# Sidebar: Select Sector
st.sidebar.header('User Input Features')
sorted_sector_unique = sorted(df['GICS Sector'].unique())
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique)

# Filtering
df_selected_sector = df[(df['GICS Sector'].isin(selected_sector))]

st.header('Displaying Companies in Selected Sector')
st.write(f'Shape of Data Frame: Rows({str(df_selected_sector.shape[0])}) Columns({str(df_selected_sector.shape[1])})')
st.dataframe(df_selected_sector)
