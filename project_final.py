"""
Name: Ryan Dancoes
CS230: SN1
Data: skyscrapers.csv
URL: https://share.streamlit.io/ryandancoes/exploring_skyscrapers/main/project_final.py

Description: Three informative graphs exploring the history and location of skyscrapers built
around the world using data adapted from Wikipedia.
"""

import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import numpy as np


def summer(num, check):
    if num == 1 and check:
        return True
    return False


def home():
    st.title('Welcome to Ryan\'s final project')
    number = np.random.randint(0, 5)
    mood = st.checkbox('')
    check = summer(number, mood)
    if check:
        st.write('Have a great summer break!')


def heatmap(dataframe):

    st.title('Heatmap')
    year = st.slider('Show skyscrapers constructed up to:', 1930, 2020)
    st.write('Concentration of skyscrapers (red > yellow):')

    # creates new dataframe with dates before selected year
    df_map = dataframe[dataframe['Year'] <= year]

    # building the deck
    view_state = pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom=0.3)
    layer = pdk.Layer(
        # heatmap of skyscraper density in an area
        'HeatmapLayer',
        data=df_map,
        get_position='[Lon, Lat]',
        radius=1000)

    # display map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=view_state,
        layers=layer))


def multiplot(dataframe):
    
    # initializing and setting variables/dictionaries
    l_sky, l_comm, l_conc, l_co_st, l_steel, l_chim, l_latt = \
        [], [], [], [], [], [], []
    x_sky, x_comm, x_conc, x_co_st, x_steel, x_chim, x_latt = \
        [], [], [], [], [], [], []
    types = {'sky': 'Skyscraper', 'comm': 'Communications tower',
             'conc': 'Concrete tower', 'co_st': 'Concrete/steel tower',
             'steel': 'Steel tower', 'chim': 'Chimney', 'latt': 'Lattice tower'}
    
    st.title('Multiplot')
    st.write('Select which types of skyscraper to display:')
    sky = st.checkbox('Skyscraper')
    comm = st.checkbox('Communications Tower')
    conc = st.checkbox('Concrete Tower')
    co_st = st.checkbox('Concrete/Steel Tower')
    steel = st.checkbox('Steel Tower')
    chim = st.checkbox('Chimney')
    latt = st.checkbox('Lattice Tower')
    yticks = np.arange(0, 50, 5)
    
    # Sorted existing df and set index back to [0, 1, 2,...]
    df_sorted = dataframe.sort_values('Year').reset_index()
    
    # link shortname with full type name
    for name, type_ in types.items():
        year, n, l, x = 0, 0, [], []
        
        # iterate through rows of building type
        for building in df_sorted[df_sorted['Type'] == type_].itertuples():
            year = building.Year
            x.append(year)
            n += 1
            l.append(n)
        
        # if no skyscrapers built in 2020, continued the line all the way across
        if year < 2020:
            for i in range(2020-year):
                year += 1
                x.append(year)
                l.append(n)
        
        if name == 'sky':
            x_sky = x
            l_sky = l
        elif name == 'comm':
            x_comm = x
            l_comm = l
        elif name == 'conc':
            x_conc = x
            l_conc = l
        elif name == 'co_st':
            x_co_st = x
            l_co_st = l
        elif name == 'steel':
            x_steel = x
            l_steel = l
        elif name == 'chim':
            x_chim = x
            l_chim = l
        elif name == 'latt':
            x_latt = x
            l_latt = l
            
    fig, ax = plt.subplots()
    if sky:  # if checkbox checked
        ax.step(x_sky, l_sky, where='post')
    if comm:
        ax.step(x_comm, l_comm, where='post')
    if conc:
        ax.step(x_conc, l_conc, where='post')
    if co_st:
        ax.step(x_co_st, l_co_st, where='post')
    if steel:
        ax.step(x_steel, l_steel, where='post')
    if chim:
        ax.step(x_chim, l_chim, where='post')
    if latt:
        ax.step(x_latt, l_latt, where='post')
    ax.set_title('Multiplot Graph')
    ax.set_xlabel('Year')
    ax.set_ylabel('Skyscrapers built')
    ax.set_xbound(1929, 2021)  # static x and y-axis
    ax.set_ybound(0, 50)
    ax.set_yticks(yticks)
    st.pyplot(fig)


def bar(dataframe):
    
    # initialize and set variables/dictionaries
    locations = {'Africa': [], 'Antarctica': [],
                 'Asia': ['United Arab Emirates', 'Japan', 'China',
                          'Saudi Arabia', 'South Korea', 'Russia', 'Taiwan',
                          'Malaysia', 'Iran', 'Kazakhstan', 'Kuwait',
                          'Uzbekistan', 'Sri Lanka'],
                 'Europe': ['Ukraine', 'Latvia', 'Germany', 'Slovenia', 'Spain',
                            'Romania'],
                 'North America': ['United States', 'Canada'],
                 'South America': [], 'Oceania': []}
    f_africa, f_antarctic, f_asia, f_europe, f_north, f_south, f_ocean = \
        0, 0, 0, 0, 0, 0, 0
    
    st.title('Bar')
    year = st.slider('Show skyscrapers constructed up to:', 1930, 2020)
    
    # new df like before (before date selected)
    df_bar = dataframe[dataframe['Year'] <= year]
    
    # I decided to do this the long way (could have just used df.count())
    for country in df_bar.Country:
        if country[1:] in locations['Africa']:
            f_africa += 1
        elif country[1:] in locations['Antarctica']:
            f_antarctic += 1
        elif country[1:] in locations['Europe']:
            f_europe += 1
        elif country[1:] in locations['Asia']:
            f_asia += 1
        elif country[1:] in locations['North America']:
            f_north += 1
        elif country[1:] in locations['South America']:
            f_south += 1
        elif country[1:] in locations['Oceania']:
            f_ocean += 1
    
    # graphing
    fig, ax = plt.subplots()
    x = [cont for cont in locations.keys()]
    freq = [f_africa, f_antarctic, f_asia, f_europe, f_north, f_south, f_ocean]
    for i in range(len(x)):
        ax.bar(x[i], freq[i])
    ax.set_title('Bar Chart through time')
    ax.set_ylabel('Skyscrapers built')
    ax.set_xticklabels(x, rotation=45)
    ax.set_ybound(0, 53)
    st.pyplot(fig)


with open('skyscrapers.csv', 'r') as file:
    df = pd.read_csv(file).fillna(0)

display = st.sidebar.selectbox(
    'Which chart would you like to display?',
    ('', '3D Map', 'Multiplot', 'Bar'))
if display == '':
    home()
elif display == '3D Map':
    heatmap(df)
elif display == 'Multiplot':
    multiplot(df)
elif display == 'Bar':
    bar(df)
