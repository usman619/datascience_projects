import yfinance as yf
import streamlit as st
import pandas as pd

st.write("""
# SIMPLE STOCK PRICE
Showing the **stock closing price** and **volumn** of the Google
""")

tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)

for keyItem, valueItem in tickerData.info.items():
    st.write(keyItem,": ",valueItem)

tickerDf = tickerData.history(period='1d', start='2020-1-8', end='2024-1-8')
# print(tickerDf.head())

st.write("## Closing Price")
st.line_chart(tickerDf.Close)

st.write("## Volume")
st.line_chart(tickerDf.Volume)