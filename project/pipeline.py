import io
import os
import logging
import pandas as pd
import requests
from io import StringIO
from dataPreparation import processTfData, weatherDataProcess

# Set up logging
logging.basicConfig(level=logging.INFO)

def collect_traffic_data(url, params, max_limit=25000):
    """
    Fetch data from the given URL using pagination due to row limits.
    
    Args:
        url (str): URL to fetch data from.
        params (dict): Parameters for the GET request.
        max_limit (int): Limit of rows per request.
    
    Returns:
        pd.DataFrame: Concatenated DataFrame with all the fetched data.
    """
    all_data = []
    offset = 0

    while True:
        # Update the parameters with the current offset and limit
        params.update({"$limit": max_limit, "$offset": offset})
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            logging.error(f"Failed to retrieve data: {response.status_code}")
            break

        # Read the fetched data into a DataFrame
        batchData = pd.read_csv(StringIO(response.text))
        
        # Break if no data is returned
        if batchData.empty:
            break

        # Append to the list and update offset
        all_data.append(batchData)
        offset += max_limit
        logging.info(f"Retrieved {len(batchData)} rows; continuing to next batch.")

    # Concatenate all batches into a single DataFrame
    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()

def get_url_data(url):
    """
    Fetch data from the given URL and load it into a DataFrame.

    Args:
        url (str): URL to fetch data from.

    Returns:
        pd.DataFrame: DataFrame containing the fetched data, or None if an error occurs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data_df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        logging.info("Data successfully retrieved from URL and loaded into DataFrame.")
        return data_df
    except requests.RequestException as e:
        logging.error(f"Unable to download data from URL: {e}")
        return None
    except pd.errors.EmptyDataError as e:
        logging.error(f"CSV file appears to be empty: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error occurred while fetching data from URL: {e}")
        return None

def dataframe_to_CSV(df_data, filename):
    """
    Save the given DataFrame to a CSV file in the /data directory.
    
    Args:
        df_data (pd.DataFrame): DataFrame to save.
        filename (str): Filename to save the DataFrame to.
    """
    directory = 'data'
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directory created: {directory}")
    
    try:
        df_data.to_csv(os.path.join(directory, filename), index=False)
        logging.info(f"Data successfully saved to {filename}.")
    except Exception as e:
        logging.error(f"Error encountered while saving file: {e}")

def main():
    # Define URLs and parameters
    traffic_data_url = "https://data.lacity.org/resource/d5tf-ez2w.csv"
    weather_data_url = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/los%20angeles/2020-01-01/2020-06-30?unitGroup=metric&include=days&key=NGNV4J2JDYHQS2AT24WRV28NH&contentType=csv'

    traffic_params = {
        "$where": "date_occ >= '2020-01-01' AND date_occ < '2020-07-01'",
        "$select": "dr_no, date_rptd, date_occ, time_occ, area, area_name, rpt_dist_no, crm_cd, crm_cd_desc, mocodes, vict_age, vict_sex, vict_descent, premis_cd, premis_desc, location, cross_street, location_1",
    }

    # Fetch and process traffic collision data
    logging.info("Starting data retrieval for traffic collision data...")
    traffic_df = collect_traffic_data(traffic_data_url, traffic_params)
    
    if not traffic_df.empty:
        processed_traffic_collision_data = processTfData(traffic_df)
        dataframe_to_CSV(processed_traffic_collision_data, "traffic_collision_data.csv")
    else:
        logging.error("Traffic collision data retrieval failed.")

    # Fetch and process weather data
    logging.info("Starting data retrieval for weather data...")
    weatherDataFrame = get_url_data(weather_data_url)
    
    if not weatherDataFrame.empty:
        processed_weather_data = weatherDataProcess(weatherDataFrame)
        dataframe_to_CSV(processed_weather_data, "weather_data.csv")
    else:
        logging.error("Weather data retrieval failed.")

if __name__ == "__main__":
    main()
