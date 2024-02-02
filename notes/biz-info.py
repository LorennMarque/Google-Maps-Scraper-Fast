from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time

driver = webdriver.Chrome()
driver.get('https://www.google.com/maps')

elements_present = EC.presence_of_all_elements_located((By.CLASS_NAME, "searchboxinput"))
WebDriverWait(driver, 10).until(elements_present)

searchbox = driver.find_element(By.ID, 'searchboxinput')
searchbox.send_keys("salones de eventos en cordoba")

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

        data = {
        }

        while True:
            current_url = driver.current_url
            data["Current_URL"] = current_url
            title_name = soup.select('.DUwDvf.lfPIob')
            Category = soup.select('.DkEaL')    
            data["Name"] = title_name[0].text
            data["Category"] = Category[0].text
            print(data["Name"])
            puntaje_element = soup.select_one('div.F7nice span[aria-hidden="true"]')
            cantidad_revisiones_element = soup.select_one('div.F7nice span:nth-child(2) span[aria-label]')

            if puntaje_element and cantidad_revisiones_element:
                data["Puntaje"] = puntaje_element.text
                cantidad_revisiones_text = cantidad_revisiones_element.text
                cantidad_revisiones_text = cantidad_revisiones_text.replace('(', '').replace(')', '').replace('.', '')

                if cantidad_revisiones_text.isdigit():
                    data["Reseñas_total"] = int(cantidad_revisiones_text)
                else:
                    print("La cantidad de revisiones no es un número válido.")
            else:
                print("Uno o ambos elementos no fueron encontrados en la página HTML.")

            direccion_element = soup.select('[data-item-id="address"]')    
            menu_element = soup.select('[data-item-id="menu"]')   
            website_element = soup.select('[data-item-id="authority"]')   
            order_element = soup.select('a[data-item-id="action:4"]')   
            telefono_element = soup.select('[data-item-id^="phone"]')

            if direccion_element:
                data["Direccion"] = direccion_element[0].text
            
            if website_element:
                data["Website"] = website_element[0].text

            if order_element:
                print(order_element[0]['href'])

            if telefono_element:
                telefono = telefono_element[0]['aria-label'].split(':')[-1].strip()
                telefono = telefono.replace(" ", "").replace("-", "")
                data["Telefono"] = telefono
                data['accessUrl'] =  f"https://api.whatsapp.com/send/?phone=+54{telefono}&text=Hola {title_name[0].text}! Mi nombre es Lorenzo. Les gustaría que haga un sitio web para su negocio?&type=phone_number&app_absent=0" 
            identifier = f"{data['Name']}_{data['Direccion']}"

            if identifier in processed_combinations:
                print(f"La combinación de nombre y dirección ya ha sido procesada. Saltando este negocio.")
                count -= 1  # Restar 1 al contador si es un duplicado
                break
            else:
                processed_combinations.add(identifier)

            data_list.append(data)
            break

    except TimeoutException:
        print("Tiempo de espera agotado al esperar elementos en la página.")
    except IndexError:
        print("Índice fuera de rango. Puede haber un problema con la selección de elementos.")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

csv_file_path = 'datos_locales.csv'
csv_headers = ['Name', 'Direccion', 'Website', 'accessUrl', 'Telefono', 'Puntaje', 'Reseñas_total', 'Category', 'Current_URL']

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    csv_writer.writeheader()
    
    for data in data_list:
        csv_writer.writerow(data)

print(f"Los datos se han guardado exitosamente en {csv_file_path}")