# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 10:41:36 2024

@author: tanuj
"""

import pandas as pd
import requests

# Read latitude, longitude, and district names from the CSV file
districts_data = pd.read_csv("districts_data.csv")

# Define API parameters
base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
parameters = "PRECTOT,T2M_RANGE,T2M_MAX,T2M_MIN"
community = "RE"
start_date = "20220101"
end_date = "20240331"
format_type = "JSON"

# Initialize an empty list to store weather data
weather_data_list = []

# Process latitude and longitude coordinates in batches of 5 by 5
batch_size = 5
for i in range(0, len(districts_data), batch_size):
    batch = districts_data.iloc[i:i+batch_size]
    
    # Initialize an empty list to store weather data for the batch
    batch_weather_data = []
    
    # Iterate over each row in the batch
    for index, row in batch.iterrows():
        latitude = row['Latitude']
        longitude = row['Longitude']
        district = row['District']
        
        # Construct the API request URL
        api_request_url = f"{base_url}?parameters={parameters}&community={community}&longitude={longitude}&latitude={latitude}&district={district}&start={start_date}&end={end_date}&format={format_type}"
        
        # Make the API request
        response = requests.get(api_request_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            weather_data = response.json()
            
            # Append the weather data to the batch list
            batch_weather_data.append(weather_data)
        else:
            print(f"Failed to fetch data for {district} (latitude: {latitude}, longitude: {longitude})")
    
    # Append the batch weather data to the main list
    weather_data_list.extend(batch_weather_data)

# make empty lists
#     
import pandas as pd

df = pd.DataFrame()

rains = []
tmin_list = []
tmax_list = []
trange_list = []
district_names = []  # List to store district names
state_names= []
dates= []
full_address= []

for idx, row in districts_data.iterrows():
    district_name = row['District']
    state_name= row['State']
    address= row['Full Address']
    
    tmin = weather_data_list[i]['properties']['parameter']['T2M_MIN'].values()
    tmax = weather_data_list[i]['properties']['parameter']['T2M_MAX'].values()
    trange = weather_data_list[i]['properties']['parameter']['T2M_RANGE'].values()
    rain = weather_data_list[i]['properties']['parameter']['PRECTOTCORR'].values()
    date = weather_data_list[1]['properties']['parameter']['T2M_MIN'].keys()
    

    for j in range(0, 821):
        tmin_1 = list(tmin)[j]
        tmax_1 = list(tmax)[j]
        trange_1 = list(trange)[j]
        rain_1 = list(rain)[j]
        date_1 = list(date)[j]

        tmin_list.append(tmin_1)
        tmax_list.append(tmax_1)
        trange_list.append(trange_1)
        rains.append(rain_1)
        district_names.append(district_name)
        state_names.append(state_name)
        dates.append(date_1)
        full_address.append(address)

# Create a DataFrame from lists
new_data = pd.DataFrame({'District': district_names, 'State':state_names,'Sdate': dates, 'TMIN': tmin_list, 'TMAX': tmax_list, 'TRANGE': trange_list, 'RAIN': rains})

# Append the new data to the existing DataFrame
df = df.append(new_data, ignore_index=True)

print(df)
df.to_csv("actual_weather_data.csv")

