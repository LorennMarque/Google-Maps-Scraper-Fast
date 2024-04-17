from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import json
import csv
import re

# Constants
INVALID_WEBSITE_NAMES = {"negocio.site", "facebook.com", "instagram.com"} # Put this into monkey-friendly json file. Somehow.

def load_config(config_file='config.json'):
    with open(config_file, 'r', encoding="utf-8") as file:
        config = json.load(file)
    return config

def open_google_maps():
    # Open webdriver
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # for Chrome >= 109
    # chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.google.com/maps')
    print("⭐ Webdriver started")
    return driver

def wait_for_elements(driver, by, value, waittime=10):
    elements_present = EC.presence_of_all_elements_located((by, value))
    WebDriverWait(driver, 10).until(elements_present)

def search_for_category(driver, category, zone):
    # Input search category
    search = f"{category} en {zone}"
    searchbox = driver.find_element(By.ID, 'searchboxinput')
    searchbox.clear()
    searchbox.send_keys(str(search))
    search_button = driver.find_element(By.ID, 'searchbox-searchbutton')
    search_button.click()
    print(f"⭐ Searching {category} in {zone} ...")


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

def scroll_results(driver, current_amount_results, waittime=100):
    try:
        wait_for_elements(driver, By.CSS_SELECTOR, '.qjESne.veYFef')
        elemento = driver.find_element(By.CSS_SELECTOR, '.qjESne.veYFef')

        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)

        times_left = 0
        print(f"⭐ {current_amount_results} results found ...")
        while times_left < waittime:
            try:
                wait_for_elements(driver, By.CSS_SELECTOR, '.hfpxzc')
                if int(current_amount_results) == int(len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))):
                    times_left += 1
                    time.sleep(0.1)
                else:
                    return True
            except:
                return False

        return False
    except:
        return False

def get_place_data(driver, place, previous_url, previous_name, category, location):
    # Extract place data
    scroll_into_view(driver, place)
    place.click()

    try:
        wait_for_elements(driver, By.CSS_SELECTOR, ".DUwDvf.lfPIob")
        place_name = re.sub(r"['\"&]", "", driver.find_element(By.CSS_SELECTOR, ".DUwDvf.lfPIob").text)
    except:
        place.click()
        wait_for_elements(driver, By.CSS_SELECTOR, ".DUwDvf.lfPIob")
        place_name = re.sub(r"['\"&]", "", driver.find_element(By.CSS_SELECTOR, ".DUwDvf.lfPIob").text)

    while not((previous_url ==  driver.current_url) == False and (previous_name == place_name) == False) :
        place.click()
        time.sleep(0.3)
        wait_for_elements(driver, By.CSS_SELECTOR, ".DUwDvf.lfPIob")

        found = True
        while found:
            try:
                place_name = re.sub(r"['\"&]", "", driver.find_element(By.CSS_SELECTOR, ".DUwDvf.lfPIob").text)
                found = False
            except:
                place.click()
                time.sleep(0.3)


    try:
        place_review_score = re.sub(r"[,]", ".",driver.find_element(By.CSS_SELECTOR, 'div.F7nice span[aria-hidden="true"]').text)
        place_review_amount = int(re.sub(r"[(\")\".]", "", driver.find_element(By.CSS_SELECTOR, 'div.F7nice span:nth-child(2) span[aria-label]').text))

    except:
        # Handle the case when either score or amount element is not found
        place_review_score = ""
        place_review_amount = ""

    try:
        place_phone_number = driver.find_element(By.CSS_SELECTOR, '[data-item-id^="phone"]').text
        # phone:tel:03548631622

    except:
        # Handle the case when either score or amount element is not found
        print("phone messed up")
        place_phone_number = ""

    try:
        place_website_element = driver.find_element(By.CSS_SELECTOR, '.rogA2c.ITvuef .Io6YTe')

        if place_website_element.text not in INVALID_WEBSITE_NAMES:
            place_website = place_website_element.text
        else:
            place_website = ""

    except:
        place_website = ""

    data = {"name": place_name, "website": place_website , "reviews_score": place_review_score , "reviews_amount": place_review_amount, 'phone': place_phone_number, 'googlemaps_link': driver.current_url,"category": category,
    'zone': location}

    # Save data to CSV
    save_to_csv([data])

    return data

def save_to_csv(data_list, csv_filename='places_data.csv'):
    with open(csv_filename, mode='a', encoding='utf-8', newline='') as csv_file:  # Changed 'w' to 'a' for append mode
        fieldnames = ['name', 'website', 'reviews_score', 'reviews_amount', 'phone','googlemaps_link', 'category', 'zone']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Check if the file is empty, if so, write the header
        csv_file.seek(0, 2)  # Move to the end of file
        if csv_file.tell() == 0:  # Check file position
            writer.writeheader()

        for data in data_list:
            writer.writerow(data)

def main():
    # Load configurations from JSON file
    config = load_config()
    data_list = []

    # Main logic
    driver = open_google_maps()
    wait_for_elements(driver, By.CLASS_NAME, 'searchboxinput')

    last_place = ""
    last_url = ""
    count = 0

    for category in config['categories']:
        for location in config['target_locations']:
            search_for_category(driver, category, location)
            wait_for_elements(driver, By.CLASS_NAME, 'hfpxzc')

            discovered_places = 0
            while True:
                try:
                    available_places = len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))
                    if available_places == discovered_places:
                        if scroll_results(driver, available_places) == False:
                            break
                    else:
                        discovered_places = len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))

                except TimeoutException: # Make this more time efficient
                    print("❓ Not found")
                    break

            places = driver.find_elements(By.CLASS_NAME, 'hfpxzc')

            for place in places:
                place_data = get_place_data(driver, place, last_url, last_place, category, location)
                while last_url == driver.current_url:
                    print("Esperando..")
                    last_url = driver.current_url
                last_place = place_data['name']
                data_list.append(place_data)
                count = count +  1 
                last_url = driver.current_url
                print(f"📩 {count} | Stored {place_data['name']}")

    # Close the browser after processing
    driver.quit()


if __name__ == "__main__":
    print("Iniciando búsqueda")
    main()
