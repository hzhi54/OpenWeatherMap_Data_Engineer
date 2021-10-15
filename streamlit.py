import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import geopy
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import weather_api
from sqlalchemy import create_engine
from sqlalchemy import inspect
import seaborn as sns

def get_State(location):
    split = location.split(',')
    return split[1][1:3]

df = None
his_df = None

# st.set_page_config(layout = "wide")
@st.cache
def getCurrent():
    print("Getting Data")
    current = weather_api.CurrentWeather()
    data = current.getData()
    current.toDataBase()
    df = current.toDataFrame()
    
    engine = create_engine("sqlite:///data/data.db")
    mod_df = pd.read_sql('SELECT * FROM combined WHERE TMAX IS NOT NULL;', engine)
    mod_df['STATE'] = mod_df['NAME'].apply(get_State)
    mod_df.fillna(value=0,inplace=True)
    mod_df = mod_df[['STATE','TMAX','TMIN','AWND','LATITUDE','LONGITUDE','DATE']].copy()
    
    return df,mod_df

df, his_df = getCurrent()

# st.write(df.head())

city = st.sidebar.selectbox('City',df['Name'])
state = df[df['Name'] == city]['State'].values[0]
zipcode = df[df['Name'] == city ]['Zip'].values[0]
lat = df[df['Name'] == city ]['Latitude'].values[0]
lon = df[df['Name'] == city ]['Longitude'].values[0]
st.sidebar.write("Zipcode: " + zipcode)
st.sidebar.write("Latitude: " + str(lat))
st.sidebar.write("Longitude: " + str(lon))

col1, col2 = st.columns((2,1))

with col1:
    st.header("WeatherMap")
    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_data)
    
with col2:
    st.header("Status")
    temperature = df[df['Name'] == city ]['Temperature'].values[0]
    temp_min = df[df['Name'] == city ]['Temp_Min'].values[0]
    temp_max = df[df['Name'] == city ]['Temp_Max'].values[0]
    wind = df[df['Name'] == city ]['Wind'].values[0]
    humidity = df[df['Name'] == city ]['Humidity'].values[0]
    st.write('Current Temperature:', temperature, 'F')
    st.write('Temperature Min:', temp_min, 'F' )
    st.write('Temperature Max:', temp_max, 'F')
    st.write('Wind Speed:', wind, 'mph')
    st.write('Humidity:', humidity, 'g/m3')
    
st.write("## Historical Data")
filter_date_start_dict = {'January': '2021-01-01','Feburary': '2021-02-01','March': '2021-03-01','April': '2021-04-01',
               'May': '2021-05-01','June': '2021-06-01','July': '2021-07-01','August': '2021-08-01',
               'September': '2021-09-01','October': '2021-10-01','November': '2021-11-01','December': '2021-12-01'}
filter_date_end_dict = {'January': '2021-01-31','Feburary': '2021-02-28','March': '2021-03-31','April': '2021-04-30',
               'May': '2021-05-31','June': '2021-06-30','July': '2021-07-31','August': '2021-08-31',
               'September': '2021-09-30','October': '2021-10-31','November': '2021-11-30','December': '2021-12-31'}
filter_date = ""

# st.write(df['State'])
# st.write(np.sort(pd.unique(his_df['STATE'])))
filter_state_dict = {"Alabama": "AL","Alaska": "AK","Arizona": "AZ","Arkansas": "AR","California": "CA","Colorado": "CO","Connecticut": "CT",
    "Delaware": "DE","Florida": "FL","Georgia": "GA","Hawaii": "HI","Idaho": "ID","Illinois": "IL","Indiana": "IN","Iowa": "IA","Kansas": "KS",
    "Kentucky": "KY","Louisiana": "LA","Maine": "ME","Maryland": "MD","Massachusetts": "MA","Michigan": "MI","Minnesota": "MN","Mississippi": "MS",
    "Missouri": "MO","Montana": "MT","Nebraska": "NE","Nevada": "NV","New Hampshire": "NH","New Jersey": "NJ","New Mexico": "NM","New York": "NY",
    "North Carolina": "NC","North Dakota": "ND","Ohio": "OH","Oklahoma": "OK","Oregon": "OR","Pennsylvania": "PA","Rhode Island": "RI","South Carolina": "SC",
    "South Dakota": "SD","Tennessee": "TN","Texas": "TX","Utah": "UT","Vermont": "VT","Virginia": "VA","Washington": "WA","West Virginia": "WV",
    "Wisconsin": "WI","Wyoming": "WY"}
filter_state = state

dates = ['January','Feburary','March','April','May','June','July','August','September','October','November','December']
filter_date = st.selectbox('Date',dates)
# st.write(filter_dict[filter_date])

col1, col2 = st.columns(2)
with col1:
    st.write('## Temperature')
    fig, ax = plt.subplots()
    plt.xticks(rotation=60)
    graph = his_df[(his_df['STATE'] == filter_state_dict[state]) 
                   & (his_df['DATE'] >= filter_date_start_dict[filter_date]) 
                   & (his_df['DATE'] <= filter_date_end_dict[filter_date])].copy()
    plt.title("Max and Min Temperature")
    sns.lineplot(graph.DATE,graph.TMAX)
    sns.lineplot(graph.DATE,graph.TMIN)
    ax.set_xticklabels(graph.DATE) 
    st.pyplot(fig)
    
# col1, col2 = st.columns((2,2))
with col2:
    st.write('## Wind Speed')
    fig, ax = plt.subplots()
    plt.xticks(rotation=60)
    graph = his_df[(his_df['STATE'] == filter_state_dict[state]) 
                   & (his_df['DATE'] >= filter_date_start_dict[filter_date]) 
                   & (his_df['DATE'] <= filter_date_end_dict[filter_date])].copy()
    plt.title("Average Wind Speed")
    sns.lineplot(graph.DATE,graph.AWND) 
    ax.set_xticklabels(graph.DATE) 
    st.pyplot(fig)

fig, ax = plt.subplots()
fig.set_size_inches(15,8)
plt.xticks(rotation=45)
graph = his_df[(his_df['STATE'] == filter_state_dict[state])]
plt.title("Yearly Summary of Temperature")
sns.lineplot(graph.DATE,graph.TMAX)
# ax.set_xticks(len(filter_date_start_dict.values()))
ax.set_ylabel("Temperature")
ax.set_xlabel("Dates")
ax.set_xticks(list(filter_date_start_dict.values())[0:10])
# ax.set_xticklabels(filter_date_start_dict.values()) 
st.pyplot(fig)

    
