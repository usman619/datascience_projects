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

# To get the stock price data using symbols for the first 20 companies
data = yf.download(
    tickers=list(df[:20].Symbol),
    period='ytd',
    interval='1d',
    group_by='ticker',
    auto_adjust=True,
    prepost=True,
    threads=True,
    proxy=None
)

st.header('Stock Prices of the first 20 companies')
st.dataframe(data)

def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    
    plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)

    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')

    return st.pyplot()

# Siderbar: Number of companies
num_company = st.sidebar.slider('Number of Companies', 1, 5)

if st.button('Show Plots'):
    st.header('Price Plot')
    for i in list(df.Symbol)[:num_company]:
        price_plot(i)