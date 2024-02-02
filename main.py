from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
import re

# Open Google Maps and look for specified category & zone

## Category and zone variables.
category = "aeropuertos"
zone = "mendoza"
search = category + " en " + zone

## Open webdriver
driver = webdriver.Chrome()
driver.get('https://www.google.com/maps')

## Wait until all elements are present
elements_present = EC.presence_of_all_elements_located((By.CLASS_NAME, "searchboxinput"))
WebDriverWait(driver, 10).until(elements_present)

## Input Search our category.
searchbox = driver.find_element(By.ID, 'searchboxinput')
searchbox.send_keys(str(search))

search_button = driver.find_element(By.ID, 'searchbox-searchbutton')
search_button.click()

## Wait until all elements are present.
results_present = EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc"))
WebDriverWait(driver, 10).until(results_present)

# Variable to store results.
data_list = []

def scroll(current_amount_results, timeout = 5):
    # Esperar a que el elemento este presente..
    elemento = WebDriverWait(driver, 5).until( # Variable de timeout
    EC.presence_of_element_located((By.CSS_SELECTOR, '.qjESne.veYFef'))
    )

    # Scroll element into view
    driver.execute_script("arguments[0].scrollIntoView(true);", elemento)

    n = 0
    while n <= timeout:
        try: 
            if current_amount_results ==  len(driver.find_elements(By.CLASS_NAME, 'hfpxzc')):
                n +=1
                print("Recargando resultados 🔥")
                time.sleep(1)
            else:
                return True
        except:
            return False
    

discovered_places = 0
while True:
    try:   
        avaiable_places = len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))
        if avaiable_places == discovered_places:
            print("Todo descubierto!")
            if not scroll(avaiable_places):
                break
        else:
            print("Falta por descubrir")
            discovered_places = len(driver.find_elements(By.CLASS_NAME, 'hfpxzc'))

    except TimeoutException:
        print("Elemento no encontrado dentro del tiempo de espera")
        break 

places = driver.find_elements(By.CLASS_NAME, 'hfpxzc')

print(f"{len(places)} encontrados.")

for place in places:
    # Click on the result
    driver.execute_script("arguments[0].scrollIntoView(true);", place)

    place.click()
    time.sleep(1)


    # Wait till result data loads
    elements_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".DUwDvf.lfPIob"))
    WebDriverWait(driver, 10).until(elements_present)

    # Sanitize the input
    place_name = re.sub(r"['\"&]", "", driver.find_element(By.CSS_SELECTOR, ".DUwDvf.lfPIob").text)

    try:
        place_website_element = driver.find_element(By.CSS_SELECTOR, '.rogA2c.ITvuef .Io6YTe')
        
        invalid_website_names = {"negocio.site", "facebook.com", "instagram.com"}
        
        if place_website_element.text not in invalid_website_names:
            place_website = place_website_element.text
        else:
            place_website = 0

    except:
        place_website = 0
        data_list.append({"Name": place_name, "Website": place_website})

print(data_list)


# # Get the atributes
# print("Aria Label:",  places[0].get_attribute("aria-label"))
# print("Tag name:", places[0].tag_name)
# print("Text content:", places[0].text)
# print("Attributes:", places[0].get_attribute("outerHTML"))
# print("Location:", places[0].location)
# print("Size:", places[0].size)
    
#         current_page_html = driver.page_source
#         soup = BeautifulSoup(current_page_html, 'html.parser')

#         data = {
#         }

#         while True:
#             title_name = soup.select('.DUwDvf.lfPIob')
#             data["Name"] = title_name[0].text
#             print(data["Name"])

# Pasar al siguiente resultado.