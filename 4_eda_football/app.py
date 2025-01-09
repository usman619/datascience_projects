import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('NFL Football Stats (Rushing) Explorer')

st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Rushing)!
* **Python libraries:** pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
""")

st.sidebar.header('Enter the Year')
selected_year = st.sidebar.selectbox('Year',list(reversed(range(1990,2025))))

# https://www.pro-football-reference.com/years/<year>/rushing.htm
@st.cache_data
def load_data(year):
    url = "https://www.pro-football-reference.com/years/" + str(year) + "/rushing.htm"
    html = pd.read_html(url, header=1)
    df = html[0]

    raw = df.fillna(0)

    raw.drop(raw.index[len(raw)-1], inplace=True)
    player_stats = raw.drop(['Rk'],axis=1)

    return player_stats

player_stats = load_data(selected_year)

# Sidebar: Select Team
sort_unique_team = player_stats.Team.unique()
selected_team = st.sidebar.multiselect('Team(s)', sort_unique_team, sort_unique_team)

# Sidebar: Select Position
unique_pos = player_stats.Pos.unique()
selected_pos = st.sidebar.multiselect('Position(s)', unique_pos, unique_pos)
# print('Teams: ',sort_unique_team)
# print('Positions: ',unique_pos)

df_selected_team = player_stats[(player_stats.Team.isin(selected_team)) & (player_stats.Pos.isin(selected_pos))]

st.write('Display Player Stats of Selected Team(s)')
st.write(f"Shape of the dataframe: Rows {str(df_selected_team.shape[0])} and Columns {str(df_selected_team.shape[1])}")
st.dataframe(df_selected_team)

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv', index=False)

    df = pd.read_csv('output.csv')
    df.drop(columns=['Player','Team','Pos','Awards'], inplace=True)

    corr = df.corr()
    mask = np.zeros_like(corr)

    st.subheader('Correlation')
    st.write(corr)

    mask[np.triu_indices_from(mask)] = True

    with sns.axes_style('white'):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)
