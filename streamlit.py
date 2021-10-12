import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import geopy
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import weather_api



df = None
@st.cache
def getCurrent():
    print("Getting Data")
    current = weather_api.CurrentWeather()
    data = current.getData()
    current.toDataBase()
    df = current.toDataFrame()
    return df

df = getCurrent()

# st.write(df.head())

street = st.sidebar.selectbox('City',df['Name'])
state = df[df['Name'] == street]['State'].values[0]
zipcode = df[df['Name'] == street ]['Zip'].values[0]
lat = df[df['Name'] == street ]['Latitude'].values[0]
lon = df[df['Name'] == street ]['Longitude'].values[0]
st.sidebar.write("Zipcode: " + zipcode)
st.sidebar.write("Latitude: " + str(lat))
st.sidebar.write("Longitude: " + str(lon))

col1, col2 = st.columns(2)

with col1:
    st.header("WeatherMap")
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_data)
    
with col2:
    st.header("Status")
    temperature = df[df['Name'] == street ]['Temperature'].values[0]
    temp_min = df[df['Name'] == street ]['Temp_Min'].values[0]
    temp_max = df[df['Name'] == street ]['Temp_Max'].values[0]
    wind = df[df['Name'] == street ]['Wind'].values[0]
    humidity = df[df['Name'] == street ]['Humidity'].values[0]
    st.write('Current Temperature:', temperature, 'F')
    st.write('Temperature Min:', temp_min, 'F' )
    st.write('Temperature Max:', temp_max, 'F')
    st.write('Wind Speed:', wind, 'mph')
    st.write('Humidity:', humidity, 'g/m3')
    
