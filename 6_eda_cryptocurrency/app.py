from locale import currency
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from bs4 import BeautifulSoup
import requests
import json
import time

image = Image.open('crypto-logo.png')
st.image(image)

expander_bar = st.expander('About')
expander_bar.header("""
- **Python libraries:** streamlit, pandas, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
- **Data source:** [CoinMarketCap](http://coinmarketcap.com).
""")

sidebar = st.sidebar
col1, col2 = st.columns((2,1))

sidebar.header('Input Output')

currency_price_unit = sidebar.selectbox('Select currency for price', ('USD','BTC','ETM'))

