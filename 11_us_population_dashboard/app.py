from venv import create
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

##################################################################################################
# Setting web page configuration
st.set_page_config(
    page_title="US-Population Dashboard",
    page_icon="🇺🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Setting data visualization theme
alt.theme.enable("dark")

# Loading the dataset
df = pd.read_csv("dataset/us-population-2010-2019-reshaped.csv")

##################################################################################################
# Siderbar
with st.sidebar:
    st.title("🇺🇸 US-Population Dashboard")

    # Another way to reverse a list
    # year_list = list(df.year.unique()[::-1])
    year_list = list(reversed(df.year.unique()))
    selected_year = st.selectbox('Select a Year', year_list)

    df_selected_year = df[df['year'] == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    theme_color_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_theme_color = st.sidebar.selectbox('Theme Color', theme_color_list)

##################################################################################################
def create_circular_progress_bar(input_response, input_text, input_color):
    if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']
        
    source = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% value": [100, 0]
    })
        
    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            #domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=130, height=130)
        
    text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% value",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=130, height=130)
    return plot_bg + plot + text


##################################################################################################
# Making Heatmap and Choropleth Map
# Choropleth Map
def create_choropleth_map(input_df, selected_theme_color):
    choropleth = px.choropleth(input_df, locations= 'states_code', color= 'population', locationmode= "USA-states",
                               color_continuous_scale= selected_theme_color,
                               range_color= (0, max(input_df.population)),
                               scope= "usa",
                               labels= {'population':'Population'}
                              )
    choropleth.update_layout(
            template= 'plotly_dark',
            plot_bgcolor= 'rgba(0, 0, 0, 0)',
            paper_bgcolor= 'rgba(0, 0, 0, 0)',
            margin= dict(l= 0, r= 0, t= 0, b= 0),
            height= 350
        )

    return choropleth

# Heatmap
def create_heatmap(input_df, selected_theme_color):

    heatmap = alt.Chart(input_df).mark_rect().encode(
        y = alt.Y('year:O', axis = alt.Axis(title= "Year", titleFontSize= 16, titlePadding= 15, titleFontWeight= 900, labelAngle= 0)),
        x = alt.X('states:O', axis = alt.Axis(title= "States", titleFontSize= 16, titlePadding= 15, titleFontWeight= 900)),
        color = alt.Color('max(population):Q',
                         legend= alt.Legend(title = " "),
                         scale= alt.Scale(scheme = selected_theme_color)),
        stroke= alt.value('black'),
        strokeWidth= alt.value(0.25),
    ).properties(width= 900
    ).configure_axis(
        labelFontSize= 12,
        titleFontSize= 12
    )

    return heatmap

# Calculate population difference
def calculate_population_difference(input_df, input_year):
    selected_year_data = input_df[input_df['year'] == input_year].reset_index()
    previous_year_data = input_df[input_df['year'] == input_year -1].reset_index()

    selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
    selected_year_data['population_difference_absolute'] = abs(selected_year_data.population_difference)

    return pd.concat([
        selected_year_data.states,
        selected_year_data.id, 
        selected_year_data.population, 
        selected_year_data.population_difference, 
        selected_year_data.population_difference_absolute], 
        axis=1
        ).sort_values(by="population_difference", ascending=False)

# Format large numbers into text (K,M etc)
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculate migration percentage for states with population difference > 50000 and < -50000
# And display the circular progress bar
def calculate_migration_percentage(input_df_population_difference, selected_year):
    if selected_year > 2010:
    
        df_greater_50000 = input_df_population_difference[input_df_population_difference.population_difference > 50000]
        df_less_50000 = input_df_population_difference[input_df_population_difference.population_difference < -50000]

        states_migration_greater = round((len(df_greater_50000)/input_df_population_difference.states.nunique())*100)
        states_migration_less = round((len(df_less_50000)/input_df_population_difference.states.nunique())*100)

    else:
        states_migration_greater = 0
        states_migration_less = 0
    
    inbound_migration = create_circular_progress_bar(states_migration_greater, 'Inbound Migration', 'green')
    outbound_migration = create_circular_progress_bar(states_migration_less, 'Outbound Migration', 'red')

    return inbound_migration, outbound_migration
##################################################################################################
# Main Dashboard Panel

# Configuring Layout
col = st.columns((1.5, 6, 2), gap="medium")

# Adding population difference
with col[0]:
    st.title("Gain/Loss")
    df_population_difference_sorted = calculate_population_difference(df, selected_year)

    if selected_year > 2010:
        first_state_name = df_population_difference_sorted['states'].iloc[0]
        first_state_population = format_number(df_population_difference_sorted['population'].iloc[0])
        first_state_delta = format_number(df_population_difference_sorted['population_difference'].iloc[0])
    else:
        first_state_name = '-'
        first_state_population = '-'
        first_state_delta = '-'
    
    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

    if (selected_year - 1) > 2010:
        last_state_name = df_population_difference_sorted['states'].iloc[-1]
        last_state_population = format_number(df_population_difference_sorted['population'].iloc[-1])
        last_state_delta = format_number(df_population_difference_sorted['population_difference'].iloc[-1])
    else:
        last_state_name = '-'
        last_state_population = '-'
        last_state_delta = '-'
    
    st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)

    # ------------------------------------------------------------------------------
    st.subheader('States Migration')

    inbound_circular_progress_bar, outbound_circular_progress_bar = calculate_migration_percentage(df_population_difference_sorted, selected_year)

    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:
        st.write('Inbound')
        st.altair_chart(inbound_circular_progress_bar)
        st.write('Outbound')
        st.altair_chart(outbound_circular_progress_bar)

# Displaying Choropleth Map and Heatmap
with col[1]:
    st.title("Total Population")
    choropleth = create_choropleth_map(df_selected_year_sorted, selected_theme_color)
    heatmap = create_heatmap(df, selected_theme_color)

    st.plotly_chart(choropleth, use_container_width=True)
    st.altair_chart(heatmap, use_container_width=True)

# Displaying the top states names and population
with col[2]:
    st.title("Top States")

    st.dataframe(df_selected_year_sorted,
                 column_order=("states", "population"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "states": st.column_config.TextColumn(
                        "States",
                    ),
                    "population": st.column_config.ProgressColumn(
                        "Population",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_year_sorted.population),
                     )}
                 )