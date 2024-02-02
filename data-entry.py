from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
import json
import csv
import re

# Constants
INVALID_WEBSITE_NAMES = {"negocio.site", "facebook.com", "instagram.com"} # Put this into monkey-friendly json file. Somehow.

def load_config(config_file='config.json'):
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def open_google_maps():
    # Open webdriver
    driver = webdriver.Chrome()
    driver.get('https://www.google.com/maps')
    return driver

def wait_for_elements(driver, by, value, timeout=10):
    elements_present = EC.presence_of_all_elements_located((by, value))
    WebDriverWait(driver, timeout).until(elements_present)

def search_for_category(driver, category, zone):
    # Input search category
    search = f"{category} en {zone}"
    searchbox = driver.find_element(By.ID, 'searchboxinput')
    searchbox.clear()
    searchbox.send_keys(str(search))
    search_button = driver.find_element(By.ID, 'searchbox-searchbutton')
    search_button.click()

def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

def scroll_results(driver, current_amount_results, timeout=5):
    elemento = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.qjESne.veYFef'))
    )
    
    driver.execute_script("arguments[0].scrollIntoView(true);", elemento)

    n = 0
    while n <= timeout:
        try:
            if current_amount_results == len(driver.find_elements(By.CLASS_NAME, 'hfpxzc')):
                n += 1
                print("Recargando resultados 🔥")
                time.sleep(1)
            else:
                return True
        except:
            return False

def get_place_data(driver, place):
    # Extract place data
    scroll_into_view(driver, place)
    place.click()
    time.sleep(1) # Replace the cooldown with some verification proccess

    wait_for_elements(driver, By.CSS_SELECTOR, ".DUwDvf.lfPIob")

    place_name = re.sub(r"['\"&]", "", driver.find_element(By.CSS_SELECTOR, ".DUwDvf.lfPIob").text)

    try:
        place_website_element = driver.find_element(By.CSS_SELECTOR, '.rogA2c.ITvuef .Io6YTe')

        if place_website_element.text not in INVALID_WEBSITE_NAMES:
            place_website = place_website_element.text
        else:
            place_website = 0

    except:
        place_website = 0

    return {"Name": place_name, "Website": place_website}

def save_to_csv(data_list, csv_filename='places_data.csv'):
    with open(csv_filename, mode='w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['Name', 'Website']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for data in data_list:
            writer.writerow(data)

    print(f'Data saved to {csv_filename}')

def main():
    # Load configurations from JSON file
    config = load_config()
    data_list = []

    # Main logic
    driver = open_google_maps()
    wait_for_elements(driver, By.CLASS_NAME, 'searchboxinput')

    for category, location in zip(config['categories'], config['target_locations']):
        search_for_category(driver, category, location)

        wait_for_elements(driver, By.CLASS_NAME, 'hfpxzc')


        discovered_places = 0
        while True:
            try:
                available_places = len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))
                if available_places == discovered_places:
                    print("Todo descubierto!")
                    if not scroll_results(driver, available_places):
                        break
                else:
                    print("Falta por descubrir")
                    discovered_places = len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))

            except TimeoutException: # Make this more time efficient
                print("Elemento no encontrado dentro del tiempo de espera")
                break

        places = driver.find_elements(By.CLASS_NAME, 'hfpxzc')

        for place in places:
            place_data = get_place_data(driver, place)
            data_list.append(place_data)

        print(data_list)

        # Save data to CSV
        save_to_csv(data_list, config['csv_filename'])

    # Close the browser after processing
    driver.quit()

if __name__ == "__main__":
    main()
