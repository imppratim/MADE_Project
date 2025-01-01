import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def processTfData(tfDataFrame):
    try:
        logger.info(f"Columns in DataFrame: {list(tfDataFrame.columns)}")

        # Log the first few rows of the 'date_occ' column before conversion
        logger.info("First few entries in 'date_occ' column before conversion:")
        logger.info(tfDataFrame['date_occ'].head())

        # Convert 'date_occ' column to datetime format
        tfDataFrame['date_occ'] = pd.to_datetime(
            tfDataFrame['date_occ'], format='%Y-%m-%dT%H:%M:%S.%f', errors='coerce'
        )
        
        # Check for null values after conversion
        if tfDataFrame['date_occ'].isnull().any():
            invalid_dates = tfDataFrame[tfDataFrame['date_occ'].isnull()]
            logger.error(f"Null values detected in the 'date_occ' column after conversion. Rows with invalid dates:\n{invalid_dates}")
            # Optionally, drop these rows or handle as needed
            tfDataFrame = tfDataFrame.dropna(subset=['date_occ'])

        # Filter for dates between Jan 1st, 2020 and Jun 30th, 2020
        start_date = pd.to_datetime("2020-01-01")
        end_date = pd.to_datetime("2020-06-30")
        tfDataFrame = tfDataFrame[(tfDataFrame['date_occ'] >= start_date) & (tfDataFrame['date_occ'] <= end_date)]

        # Reformat 'date_occ' to 'yyyy-mm-dd'
        tfDataFrame['date_occ'] = tfDataFrame['date_occ'].dt.strftime('%Y-%m-%d')
        
        # Format 'time_occ' as HH:MM
        tfDataFrame['time_occ'] = tfDataFrame['time_occ'].apply(
            lambda x: f"{str(x).zfill(4)[:2]}:{str(x).zfill(4)[2:]}" if pd.notnull(x) else None
        )
        
        logger.info("First few entries in 'date_occ' column after conversion and filtering:")
        logger.info(tfDataFrame['date_occ'].head())

        # Columns to drop
        dropColumn = ['dr_no', 'date_rptd', 'area', 'area_name', 'rpt_dist_no', 'crm_cd', 'crm_cd_desc', 'mocodes', 'vict_age', 'vict_sex', 'vict_descent', 'premis_cd', 'premis_desc', 'location', 'cross_street', 'location_1']
        tfDataFrame = tfDataFrame.drop(columns=dropColumn)
        
        # Add a column for the number of collisions per day
        daily_counts = tfDataFrame.groupby('date_occ').size().reset_index(name='collision_count')

        # Return the processed data and daily counts
        return tfDataFrame, daily_counts

    except Exception as e:
        logger.error(f"An error occurred during data processing: {e}")
        return None, None

def weatherDataProcess(weatherDataFrame):
    """
    Process weather data by dropping unnecessary columns.

    Args:
        weatherDataFrame (pd.DataFrame): DataFrame containing weather data.

    Returns:
        pd.DataFrame: Processed DataFrame with selected columns removed.
    """
    dropColumn = [
        'name', 'tempmax', 'tempmin', 'feelslikemax', 'feelslikemin', 'feelslike', 'dew', 'icon', 'precip',
        'precipprob', 'precipcover', 'preciptype', 'snow', 'snowdepth', 'windgust', 'winddir', 
        'sealevelpressure', 'cloudcover', 'solarradiation', 'solarenergy', 'uvindex', 
        'severerisk', 'sunrise', 'sunset', 'moonphase', 'conditions', 'description', 'stations'
    ]
    weatherDataFrame = weatherDataFrame.drop(columns=dropColumn)
    return weatherDataFrame
