import os
import io
import pytest
import pandas as pd
from pipeline import get_url_data, dataframe_to_CSV
from dataPreparation import processTfData, weatherDataProcess

# Constants
data_dir = 'data'
csv_data_files = [
    'traffic_collision_data.csv',
    'weather_data.csv'
]
traffic_collision_data_url = "https://data.lacity.org/resource/d5tf-ez2w.csv"

# Sample weather data (from the given sheet format) and data (as a string)
weather_data_str = """
name,datetime,tempmax,tempmin,temp,feelslikemax,feelslikemin,feelslike,dew,humidity,precip,precipprob,precipcover,preciptype,snow,snowdepth,windgust,windspeed,winddir,sealevelpressure,cloudcover,visibility,solarradiation,solarenergy,uvindex,severerisk,sunrise,sunset,moonphase,conditions,description,icon,stations
Los Angeles,2021-01-01,20,10,15,25,8,15,6,50,0.1,90,80,Clear,0,0,5,10,90,1015,35,10,200,5,6,1.2,7:00,17:00,0.2,Clear sky,Sunny,clear-sky-icon,Station1
Los Angeles,2021-01-02,18,8,12,22,6,12,7,55,0.05,85,70,Rain,0.2,0,4,8,85,1013,40,9,180,4,6,1.1,7:05,17:05,0.3,Partly cloudy,Partly cloudy with rain in the afternoon,cloud-rain-icon,Station2
Los Angeles,2021-01-03,25,15,20,30,10,18,5,40,0.2,95,90,Cloudy,0,0,3,12,100,1010,50,8,150,6,7,1.3,7:10,17:10,0.4,Cloudy,Cloudy day,cloud-icon,Station3
"""

# Fixtures
@pytest.fixture(scope='module')
def traffic_collision_data():
    traffic_df = get_url_data(traffic_collision_data_url)
    assert traffic_df is not None
    assert not traffic_df.empty
    return traffic_df

@pytest.fixture(scope='module')
def weather_data():
    # Use the renamed string variable for the weather data
    try:
        weather_df = pd.read_csv(io.StringIO(weather_data_str))
        assert not weather_df.empty, "Mock weather data is empty."
        return weather_df
    except Exception as e:
        print(f"Error while reading weather data: {e}")
        raise

# Test Cases

def test_get_traffic_collision_data_success():
    """Test if traffic collision data can be successfully fetched."""
    traffic_df = get_url_data(traffic_collision_data_url)
    assert traffic_df is not None
    assert not traffic_df.empty

def test_traffic_collision_data(traffic_collision_data):
    """Test the processing of traffic collision data."""
    output = processTfData(traffic_collision_data)
    
    assert output is not None
    
    # Check for the correct columns in the output
    expected_columns = ['date_occ', 'time_occ']  # Update to match actual columns
    for column in expected_columns:
        assert column in output.columns, f"Column {column} not found in output DataFrame."
    
    # Save the output to CSV
    dataframe_to_CSV(output, 'traffic_collision_data.csv')


def test_weather_data(weather_data):
    """Test the processing of weather data."""
    output = weatherDataProcess(weather_data)
    
    assert output is not None
    
    # Check for the columns in the output
    expected_columns = ['datetime', 'temp', 'humidity', 'windspeed', 'visibility']
    for column in expected_columns:
        assert column in output
    
    # Save the output to CSV
    dataframe_to_CSV(output, 'weather_data.csv')

def test_csv_data_files_exist():
    """Test if the CSV files are saved in the data directory."""
    for filename in csv_data_files:
        filepath = os.path.join(data_dir, filename)
        assert os.path.exists(filepath), f"ERROR: {filepath} does not exist."

# Optional: Check the contents of the saved CSV files
def test_output_file_content():
    """Test the content of the saved CSV files."""
    for filename in csv_data_files:
        filepath = os.path.join(data_dir, filename)
        # Ensure the file is not empty
        assert os.path.getsize(filepath) > 0, f"ERROR: {filepath} is empty."
