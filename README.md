    <h1>Google Maps Scraper</h1>

    <h2>Overview</h2>
    <p>
        This script automates data scraping from Google Maps using Selenium. It performs searches based on user-provided queries, extracts detailed location information (name, coordinates, ratings, reviews, contact details, and more), and appends this data to a CSV file for further analysis.
    </p>

    <h2>Features</h2>
    <ul>
        <li>Automates searching and data extraction from Google Maps.</li>
        <li>Saves location data into a single CSV file named with a timestamp.</li>
        <li>Handles errors gracefully if some data fields are unavailable.</li>
        <li>Uses a configuration file (<code>config.json</code>) for query customization.</li>
    </ul>

    <h2>Requirements</h2>
    <p>Before running the script, ensure the following are installed:</p>
    <ul>
        <li><a href="https://www.python.org/">Python 3.7+</a></li>
        <li>Google Chrome</li>
        <li>ChromeDriver (compatible with your version of Chrome)</li>
        <li>Python dependencies listed in <code>requirements.txt</code></li>
    </ul>

    <h2>Installation</h2>
    <pre>
# Clone or download the repository

# Install required Python libraries
echo "selenium" > requirements.txt
pip install -r requirements.txt

# Download ChromeDriver
# Ensure ChromeDriver matches your Chrome version
# Add ChromeDriver to your PATH
    </pre>

    <h2>Usage</h2>
    <ol>
        <li>
            <strong>Set up <code>config.json</code>:</strong>
            <p>Create a file named <code>config.json</code> in the root folder. Define your search queries as follows:</p>
            <pre>
{
    "queries": [
        "restaurants near me",
        "cafes in New York",
        "hotels in Paris"
    ]
}
            </pre>
        </li>
        <li>
            <strong>Run the script:</strong>
            <pre>python script_name.py</pre>
        </li>
        <li>
            <strong>Access the output:</strong>
            <p>The results will be saved in the <code>output</code> folder with a filename like <code>scrap-YYYY-MM-DD_HH-MM-SS.csv</code>.</p>
        </li>
    </ol>

   > Usage tip: As google maps limits the results per query i strongly suggest to use specific queries in the config.json file. For instance specify query per state instead of a country.

    <h2>Detailed Explanation</h2>
    <h3>Code Workflow</h3>
    <ol>
        <li><strong>Initialization:</strong> The script creates an output folder and a CSV file with headers for storing location data.</li>
        <li><strong>Configuration Loading:</strong> Reads search queries from <code>config.json</code>.</li>
        <li><strong>Google Maps Automation:</strong>
            <ul>
                <li>Launches Google Maps in a headless Chrome browser (or visible window for debugging).</li>
                <li>Performs searches using the provided queries.</li>
            </ul>
        </li>
        <li><strong>Data Extraction:</strong> For each location result:
            <ul>
                <li>Extracts data like name, coordinates, ratings, reviews, address, phone, and website.</li>
                <li>Handles missing fields with fallback mechanisms.</li>
                <li>Appends extracted data to the CSV file.</li>
            </ul>
        </li>
        <li><strong>Cleanup:</strong> Closes the browser after processing all queries.</li>
    </ol>

    <h3>Key Functions</h3>
    <ul>
        <li><code>load_config</code>: Reads and parses the <code>config.json</code> file.</li>
        <li><code>open_google_maps</code>: Initializes the Chrome WebDriver and opens Google Maps.</li>
        <li><code>search_query</code>: Searches Google Maps using a provided query.</li>
        <li><code>get_place_data</code>: Extracts details about a specific location.</li>
        <li><code>click_all_elements</code>: Iteratively clicks on location elements and triggers data extraction.</li>
        <li><code>append_to_csv</code>: Appends data to the CSV file.</li>
    </ul>

    <h2>Output</h2>
    <p>
        The output is a CSV file saved in the <code>output</code> folder. The file includes the following fields:
    </p>
    <ul>
        <li><code>name</code>: Name of the place.</li>
        <li><code>url</code>: URL of the Google Maps page for the place.</li>
        <li><code>latitude</code>: Latitude of the location.</li>
        <li><code>longitude</code>: Longitude of the location.</li>
        <li><code>average_rating</code>: Average review rating (if available).</li>
        <li><code>review_count</code>: Number of reviews (if available).</li>
        <li><code>address</code>: Address of the location (if available).</li>
        <li><code>phone</code>: Phone number (if available).</li>
        <li><code>website</code>: Website URL (if available).</li>
    </ul>

    <h2>Troubleshooting</h2>
    <ul>
        <li>Ensure ChromeDriver is in your PATH and matches your Chrome version.</li>
        <li>If elements are not found, verify that Google Maps has not changed its DOM structure. Update selectors as needed.</li>
        <li>If the browser doesn't open or work properly, confirm that dependencies are installed correctly.</li>
    </ul>

    <h2>Contact</h2>
    <p>
        For support or contributions, you can contact me at lorenzomarquesini@gmail.com
    </p>
</body>
</html>
