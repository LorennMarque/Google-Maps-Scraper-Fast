# Google Maps Web Scraper for Place Data

This script utilizes Selenium to extract data from commercial places on the web. Make sure to follow the steps below to set up and run the script.

You can set multiple target categories in different locations so the script can scrap +200 rows at ease.

Information scraped:

- Name
- Website URL
- Reviews Score
- Reviews Amount
- Phone number
- GoogleMaps URL

## Installation of Requirements

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/LorennMarque/Plug-Go-Google-Maps-Scrapper
   ```

2. Install the dependencies using the requirements.txt file:

   ```bash
   pip install -r requirements.txt
   ```

3. Configuration of the config.json File:
   Open the config.json file and customize it with the information you are looking for. Here is an example configuration:

   ```json
   {
     "categories": ["restaurants"],
     "target_locations": ["san juan, Argentina"],
     "csv_filename": "places_data.csv"
   }
   ```

   - categories: The type of business you want to extract (you can add or remove categories as needed).
   - target_locations: Specific places where you want to perform the extraction (you can add or remove locations as needed).
   - csv_filename: The name of the CSV file to export the data.

## Running the Script

Once you have configured the config.json file, execute the following command to start the script:

```
python data-entry.py
```

Monitor the console to see how the script is working. Note that obtaining results may take up to 10 seconds to be stored.

That's it! You should now have a CSV file with the extracted data from the places you specified in the configuration file.
