# Project Plan

## Title

<!-- Give your project a short title. -->

Investigating the impact of weather conditions on road crashes in Los Angeles

## Main Question

<!-- Think about one main question you want to answer based on the data. -->

What is the correlation between weather conditions and traffic collisions in Los Angeles from January to June 2020?

## Description

<!-- Describe your data science project in max. 200 words. Consider writing about why and how you attempt it. -->

The purpose of this study is to investigate the relationship between weather conditions and road crashes in Los Angeles. This research will examine whether significant correlations exist between daily weather parameters such as temperature, rainfall, visibility, and wind speed and the frequency and severity of road crashes. Understanding this relationship will offer valuable insights for city planners and public safety officials, supporting strategies to improve road safety and reduce weather-related accidents. The study will employ statistical analysis and data visualization techniques to identify patterns and trends, presenting a comprehensive view of how weather impacts road safety in Los Angeles.

## Datasources

<!-- Describe each data source you plan to use in a section. Use the prefix "DatasourceX" where X is the id of the data source. -->

##Datasource 1: Traffic Collision Data

### Metadata URL: https://data.lacity.org/Public-Safety/Traffic-Collision-Data-from-2010-to-Present/d5tf-ez2w/about_data

### Data URL: https://data.lacity.org/resource/d5tf-ez2w.csv

Data Type: CSV
Description: The traffic collision data, sourced from the Los Angeles City Open Data Portal, provides detailed records of reported traffic incidents in Los Angeles from 2010 to the present. This dataset includes crucial information such as the date, time, and location of each collision, as well as factors related to crash severity, causes, and any injuries or fatalities involved. For this study, the dataset will be filtered to include only incidents from January to June 2020, aligning with the weather data. We need an account to download or fetch data more than 1000 and for that reason we have used a separate function sue to the row limit.

#Datasource 2: Weather data

### Metadata URL: https://www.visualcrossing.com/resources/documentation/weather-data/weather-data-documentation/

### Data URL: https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/retrievebulkdataset?&key=NGNV4J2JDYHQS2AT24WRV28NH&taskId=aae51ed3104c7803e597cd073839ce9b&zip=false

Data Type: CSV
Description: The weather data, obtained from Visual Crossing, provides historical weather information for Los Angeles, covering various meteorological parameters such as temperature, precipitation, visibility, wind speed, and humidity. This dataset is available on a daily basis and includes comprehensive records necessary to analyze environmental conditions. For this study, weather data from January to June 2020 will be used to match the traffic collision data timeframe, allowing for a detailed examination of how specific weather conditions correlate with road crashes.

## Work Packages

<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Define Problem Statement and Objectives #1
2. Identify and Collect Data #2
3. Data Preparation and Processing (ETL pipeline) #3
4. Data Report (Preliminary) #4
5. Data Analysis, Interpretation, and Visualization #5
6. Final Report (Result) #6
