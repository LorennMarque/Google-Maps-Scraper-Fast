import webbrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.google.com/maps')

elements_present = EC.presence_of_all_elements_located((By.CLASS_NAME, "searchboxinput"))
WebDriverWait(driver, 10).until(elements_present)

searchbox = driver.find_element(By.ID, 'searchboxinput')
searchbox.send_keys("Peluquerías en chile")

search_button = driver.find_element(By.ID, 'searchbox-searchbutton')
search_button.click()

results_present = EC.presence_of_all_elements_located((By.CLASS_NAME, "hfpxzc"))
WebDriverWait(driver, 10).until(results_present)
input("Terminaste de scrollear?")
local_buttons = driver.find_elements(By.CLASS_NAME, 'hfpxzc')
print("LONGITUD: " + str(len(local_buttons)))

data_list = []
processed_combinations = set()
count = 0  # Inicializar el contador fuera del bucle

for local_button in local_buttons:
    try:
        count += 1  # Incrementar el contador en cada iteración

        print(f"\nProcessing {count} of {len(local_buttons)}")

        local_button.click()

        elements_present = EC.presence_of_all_elements_located((By.CLASS_NAME, "CsEnBe"))
        WebDriverWait(driver, 10).until(elements_present)

        current_page_html = driver.page_source
        soup = BeautifulSoup(current_page_html, 'html.parser')

        data = {}

        while True:
            title_name = soup.select('.DUwDvf.lfPIob')
            website_element = soup.select('[data-item-id="authority"]')   
            telefono_element = soup.select('[data-item-id^="phone"]')

            if not website_element:
                mensaje = f'''Hola {title_name[0].text}! Soy Lorenzo de Andes Software, como estan?'''
                data["Name"] = title_name[0].text
                telefono = telefono_element[0]['aria-label'].split(':')[-1].strip()
                telefono = telefono.replace(" ", "").replace("-", "")
                data["Telefono"] = telefono
                data['accessUrl'] = f"https://api.whatsapp.com/send/?phone={telefono}&text={mensaje}&type=phone_number&app_absent=0" 

            data_list.append(data)
            break

    except TimeoutException:
        print("Tiempo de espera agotado al esperar elementos en la página.")
    except IndexError:
        print("Índice fuera de rango. Puede haber un problema con la selección de elementos.")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

print(data_list)

for data in data_list:
    if 'accessUrl' in data:
        processed_combinations.add(data['accessUrl'])
        webbrowser.open_new_tab(data['accessUrl'])

driver.quit()  # Cierra el navegador después de abrir las pestañas
