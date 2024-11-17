# Google Maps Scraper

## Overview
This script automates data scraping from Google Maps using Selenium. It performs searches based on user-provided queries, extracts detailed location information (name, coordinates, ratings, reviews, contact details, and more), and appends this data to a CSV file for further analysis.

## Features
* Automates searching and data extraction from Google Maps
* Saves location data into a single CSV file named with a timestamp
* Handles errors gracefully if some data fields are unavailable
* Uses a configuration file (`config.json`) for query customization

## Requirements
Before running the script, ensure the following are installed:

* [Python 3.7+](https://www.python.org/)
* Google Chrome
* ChromeDriver (compatible with your version of Chrome)
* Install Selenium package

## Installation
```bash
# Clone or download the repository

# Install required Python libraries
pip install selenium

# Download ChromeDriver
# Ensure ChromeDriver matches your Chrome version
# Add ChromeDriver to your PATH
```

## Usage
1. **Set up `config.json`:**
   
   Create a file named `config.json` in the root folder. Define your search queries as follows:
   ```json
   {
       "queries": [
           "restaurants near me",
           "cafes in New York",
           "hotels in Paris"
       ]
   }
   ```

2. **Run the script:**
   ```bash
   python script_name.py
   ```

3. **Access the output:**
   
   The results will be saved in the `output` folder with a filename like `scrap-YYYY-MM-DD_HH-MM-SS.csv`.

> **Usage tip:** As Google Maps limits the results per query, I strongly suggest using specific queries in the config.json file. For instance, specify query per state instead of a country.

## Detailed Explanation

### Code Workflow
1. **Initialization:** The script creates an output folder and a CSV file with headers for storing location data.
2. **Configuration Loading:** Reads search queries from `config.json`.
3. **Google Maps Automation:**
   * Launches Google Maps in a headless Chrome browser (or visible window for debugging)
   * Performs searches using the provided queries
4. **Data Extraction:** For each location result:
   * Extracts data like name, coordinates, ratings, reviews, address, phone, and website
   * Handles missing fields with fallback mechanisms
   * Appends extracted data to the CSV file
5. **Cleanup:** Closes the browser after processing all queries

### Key Functions
* `load_config`: Reads and parses the `config.json` file
* `open_google_maps`: Initializes the Chrome WebDriver and opens Google Maps
* `search_query`: Searches Google Maps using a provided query
* `get_place_data`: Extracts details about a specific location
* `click_all_elements`: Iteratively clicks on location elements and triggers data extraction
* `append_to_csv`: Appends data to the CSV file

## Output
The output is a CSV file saved in the `output` folder. The file includes the following fields:

* `name`: Name of the place
* `url`: URL of the Google Maps page for the place
* `latitude`: Latitude of the location
* `longitude`: Longitude of the location
* `average_rating`: Average review rating (if available)
* `review_count`: Number of reviews (if available)
* `address`: Address of the location (if available)
* `phone`: Phone number (if available)
* `website`: Website URL (if available)

## Troubleshooting
* Ensure ChromeDriver is in your PATH and matches your Chrome version
* If elements are not found, verify that Google Maps has not changed its DOM structure. Update selectors as needed
* If the browser doesn't open or work properly, confirm that dependencies are installed correctly

## Contact
For support or contributions, you can contact me at lorenzomarquesini@gmail.com