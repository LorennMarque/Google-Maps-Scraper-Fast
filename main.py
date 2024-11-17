# Selenium Imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# Standard Library Imports
import os
import re
import csv
import time
import json
from datetime import datetime

# Create the output folder if it doesn't exist
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Create a single CSV file at the start with a timestamp
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CSV_FILENAME = os.path.join(OUTPUT_FOLDER, f"scrap-{timestamp}.csv")

# Write the headers to the CSV file
with open(CSV_FILENAME, mode="w", encoding="utf-8", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=[
        "name", "url", "latitude", "longitude", "average_rating",
        "review_count", "address", "phone", "website"
    ])
    writer.writeheader()

def append_to_csv(data):
    """
    Appends a dictionary of data to the pre-created CSV file.

    Args:
        data (dict): A dictionary containing the data to append.
    """
    with open(CSV_FILENAME, mode="a", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data.keys())
        writer.writerow(data)
    print(f"✍ Data appended to {CSV_FILENAME}")

def load_config(config_file = 'config.json'):
    """
    This function loads and returns configuration data from a 
    specified JSON file, defaulting to config.json, using UTF-8
    encoding.
    """
    with open(config_file, 'r', encoding="utf-8") as file:
        config = json.load(file)
    return config

def open_google_maps(show_window = False):
    """
    This function opens Google Maps in a Chrome browser, optionally
    in a visible window, and returns the WebDriver instance.
    """
    chrome_options = Options()
    if(show_window):
        chrome_options.add_argument("--window-size=1920,1080")
    else:
        chrome_options.add_argument("--headless=new") # for Chrome >= 109

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.google.com/maps')

    wait_for_elements(driver, By.CLASS_NAME, 'searchboxinput')

    print("✅ Webdriver started")
    return driver


def wait_for_elements(driver, by, value):
    """
    This function waits up to 10 seconds for all elements matching
    the specified locator (by and value) to be present in the given 
    WebDriver instance.
    """
    elements_present = EC.presence_of_all_elements_located((by, value))
    WebDriverWait(driver, 10).until(elements_present)

def search_query(driver, query):
    """
    This function searches for a specified query in Google Maps
    by interacting with the search box and search button elements on the page.
    """
    # Input search category
    searchbox = driver.find_element(By.ID, 'searchboxinput')
    searchbox.clear()
    searchbox.send_keys(str(query))

    search_button = driver.find_element(By.ID, 'searchbox-searchbutton')
    search_button.click()

    # Wait for results to load
    wait_for_elements(driver, By.CLASS_NAME, 'hfpxzc')

    print(f"🔎 Searching {query}...")

def scroll_into_view(driver, element):
    """
    Scrolls given element into view
    """
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

def get_place_data(driver, location_element):
    """
    Extracts key data from a location element on Google Maps.

    Args:
        driver: The Selenium WebDriver instance.
        location_element: The specific location element to process.

    Returns:
        dict: A dictionary containing the extracted data, including:
            - name: The name of the place.
            - url: The current URL of the place.
            - latitude, longitude: Coordinates extracted from the URL.
            - average_rating: Average review rating of the place (if available).
            - review_count: Number of reviews for the place (if available).
            - address: Address of the place (if available).
            - phone: Phone number of the place (if available).
            - website: Website of the place (if available).
    """
    scroll_into_view(driver, location_element)
    wait_for_elements(driver, By.CSS_SELECTOR, ".DUwDvf.lfPIob")
    location_element.click()

    try:
        # Extraer nombre del lugar
        place_name = driver.find_element(By.CSS_SELECTOR, ".DUwDvf.lfPIob").text
        
        # Extraer URL actual
        place_url = driver.current_url

        # Extraer coordenadas del URL
        match = re.search(r"@(-?\d+\.\d+),(-?\d+\.\d+)", place_url)
        latitude, longitude = match.groups() if match else (None, None)

        # Extraer promedio de reseñas
        try:
            average_rating = driver.find_element(By.CSS_SELECTOR, ".F7nice span[aria-hidden='true']").text
        except:
            average_rating = None

        # Extraer cantidad de reseñas
        try:
            review_count_text = driver.find_element(By.CSS_SELECTOR, ".F7nice span[aria-label*='opiniones']").text
            review_count = int(re.search(r"\d+", review_count_text.replace(",", "")).group())
        except:
            review_count = None

        # Extraer dirección
        try:
            address = driver.find_element(By.CSS_SELECTOR, "button[data-item-id='address'] .Io6YTe").text
        except:
            address = None

        # Extraer teléfono
        try:
            phone = driver.find_element(By.CSS_SELECTOR, "button[data-item-id*='phone'] .Io6YTe").text
        except:
            phone = None

        # Extraer sitio web
        try:
            website = driver.find_element(By.CSS_SELECTOR, "a[data-item-id='authority'] .Io6YTe").text
        except:
            website = None

        print(f"🚗💨 Data extracted from: {place_name}")
    except Exception as e:
        print(f"❌ ERROR to extract location data: {e}")
        return {}

    # Crear diccionario con los datos extraídos
    data = {
        "name": place_name,
        "url": place_url,
        "latitude": latitude,
        "longitude": longitude,
        "average_rating": average_rating,
        "review_count": review_count,
        "address": address,
        "phone": phone,
        "website": website
    }

    return data

def click_all_elements(driver):
    clicked_elements = set()  # Para rastrear los elementos ya clicados
    total_elements_found = 0  # Contador de elementos encontrados
    element_removed = False   # Bandera para saber si ya se eliminó el elemento

    while True:
        # Encuentra todos los elementos actuales con la clase 'hfpxzc'
        elements = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
        new_elements_found = False

        # Verifica si el elemento problemático debe eliminarse
        if not element_removed:
            try:
                # Intenta seleccionar el elemento
                element_to_remove = driver.find_element(By.CSS_SELECTOR, '.RiRi5e.Hk4XGb.Yt0HSb')
                
                # Ejecuta JavaScript para eliminarlo del DOM
                driver.execute_script("arguments[0].remove();", element_to_remove)
                element_removed = True  # Marca como eliminado
                print("✅ Elemento eliminado del DOM")
            except:
                # Si no se encuentra el elemento, ignora y continúa
                print("❌ Elemento no encontrado. No se eliminó nada.")

        for element in elements:
            # Identifica elementos no clicados usando su referencia única
            if element not in clicked_elements:
                try:
                    # Captura la URL actual antes del clic
                    current_url = driver.current_url
                    
                    # Intenta hacer clic en el elemento
                    element.click()
                    clicked_elements.add(element)
                    total_elements_found += 1  # Incrementa el contador
                    new_elements_found = True
                    print(f"✅ Click en un nuevo elemento (Total: {total_elements_found})")
                    
                    # Espera a que la URL se actualice
                    WebDriverWait(driver, 10).until(EC.url_changes(current_url))

                    # Obtener los datos del lugar usando la función get_place_data
                    place_data = get_place_data(driver, element)
                    append_to_csv(place_data)
                    
                    time.sleep(0.5)  # Pausa para evitar problemas de carga
                except ElementClickInterceptedException:
                    try:
                        # Usa ActionChains como alternativa si el clic está interceptado
                        ActionChains(driver).move_to_element(element).click().perform()
                        clicked_elements.add(element)
                        total_elements_found += 1
                        new_elements_found = True
                        print(f"✅ Click (ActionChains) en un nuevo elemento (Total: {total_elements_found})")
                        
                        # Espera a que la URL cambie
                        WebDriverWait(driver, 10).until(EC.url_changes(current_url))
                        print(f"✅ URL cambió después del clic: {driver.current_url}")
                        
                    except Exception as e:
                        print(f"❌ Elemento no se pudo clicar: {e}")
                except Exception as e:
                    print(f"❌ No se pudo hacer clic en un elemento: {e}")

        # Si no se encontraron nuevos elementos, asumimos que se terminó el scroll
        if not new_elements_found:
            print(f"✅ No hay más elementos nuevos para clicar. Total procesados: {total_elements_found}")
            break

        # Scroll para cargar más elementos si es necesario
        try:
            last_element = elements[-1]
            scroll_into_view(driver, last_element)
            time.sleep(1)  # Espera para que se carguen más resultados
        except Exception as e:
            print(f"❌ Error al intentar hacer scroll: {e}")
            break

def main():
    # Load configurations from JSON file
    config = load_config()

    # Main logic
    # driver = open_google_maps()
    driver = open_google_maps(show_window = True)

    for query in config['queries']:
        search_query(driver, query)
        click_all_elements(driver)

    # Close the browser after processing
    driver.quit()


if __name__ == "__main__":
    print("🚀 Script Started")
    main()
