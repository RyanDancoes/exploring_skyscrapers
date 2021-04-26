import pandas as pd
import streamlit as st
import pydeck as pdk
import numpy as np


def home():
    st.title('Welcome to Ryan\'s final project')


def map(df):
    st.title('Map')
    year = st.slider('Select Year:', 1930, 2020, step=5)
    df_map = df[df['Year'] <= year]


    view_state = pdk.ViewState(
        latitude=0,
        longitude=0,
        zoom=0
    )
    layer = pdk.Layer(
        'HeatmapLayer',
        data=df_map,
        get_position='[Lon, Lat]',
        radius=1000,
        pickable=True,
        opacity=0.9
    )
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=view_state,
        layers=layer
    ))


def multiplot(df):
    st.title('Multiplot')


def bar(df):
    st.title('Bar')


with open('skyscrapers.csv', 'r') as file:
    df = pd.read_csv(file)
    st.write(df)


display = st.sidebar.selectbox(
    'Which chart would you like to display?',
    ('None', '3D Map', 'Multiplot', 'Bar')
)
if display == 'None':
    home()
elif display == '3D Map':
    map(df)
    pass
elif display == 'Multiplot':
    multiplot(df)
elif display == 'Bar':
    bar(df)

