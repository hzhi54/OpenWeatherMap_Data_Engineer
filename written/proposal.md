# Proposal
## Problem & Idea
For this project, I'm will create a dashboard or screening that will produce weather conditions in North America. Creating possible forcast of weather conditions for the week in different locations. The application will be updated daily and will provide visuals to show the updates.

## Data
Collecting data from OpenWeatherMap using their API and they provide the data in JSON file. The data contains many features such as id, date, name, coord, city, country, weather, and other more. There are hierarchal formatting (ie. coord.lat and coord.lon) in the JSON file to configure after obtaining the data.

## Algorithms
Pipelining will be my best friend when I clean data and aggregate data. Things that I consider to pipeline will be filtering by zip-code, and city. Also create pipeline steps to update visual consistently as new data requested by the OWM API.

## Tools
For now, I'm planning to use big data handling to help me process the data. Stores the data to MongoDB because the data has many heiarchy. Ultimately, I wanted to create an application or a dashboard that will take the process or cleaned data so that there will be visuals (ie. a map of weather conditions in specific places or like the weather app iPhone has).
