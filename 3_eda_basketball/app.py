import streamlit as st
import base64
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
- **Python libraries:** pandas, streamlit, numpy, matplotlib, seaborn
- **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

# Siderbar: Select Year
st.sidebar.header('User Input Feature')
selected_year = st.sidebar.selectbox('Year',list(reversed(range(1950,2025))))

@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url,header=0)
    df = html[0]
    df = df.fillna(0)

    player_stats = df.drop(['Rk'],axis=1)
    # print(player_stats.columns)

    return player_stats

player_stats = load_data(selected_year)

# Sidebar: Select Team
st.sidebar.header('Select Team(s)')
sort_unqiue_team = sorted(player_stats.Team.astype(str).unique())

# Removing the '0' from the teams list
sort_unqiue_team.remove('0')

selected_team = st.sidebar.multiselect('Team(s)', sort_unqiue_team, sort_unqiue_team)

# Siderbar: Select Position
st.sidebar.header('Select Position(s)')
unqiue_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', unqiue_pos, unqiue_pos)

# Filtering the Player Stats
df_selected_team = player_stats[player_stats.Team.isin(selected_team) & player_stats.Pos.isin(selected_pos)]

# Displaying the Dataframe
st.header('Display Player Stats of Selected Team(s)')
st.write(f"Shape of the dataframe: Rows {str(df_selected_team.shape[0])} and Columns {str(df_selected_team.shape[1])}")
st.dataframe(df_selected_team)

# Download the selected players dataframe in csv formate 
# (but now the 'st.dataframe()' comes with download and search functionality)
# def download_file(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()
#     href = f'<a href="data/file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
#     return href

# st.markdown(download_file(df_selected_team), unsafe_allow_html=True)

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv', index=False)

    df = pd.read_csv('output.csv')
    df.drop(columns=['Player','Team','Pos','Awards'],inplace=True)

    corr = df.corr()
    mask = np.zeros_like(corr)

    st.subheader('Correlation')
    st.write(corr)

    mask[np.triu_indices_from(mask)] = True

    with sns.axes_style('white'):
        f, ax = plt.subplots(figsize=(7,5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)