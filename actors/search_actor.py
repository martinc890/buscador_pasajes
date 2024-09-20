import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pykka

class SearchActor(pykka.ThreadingActor):

    def on_receive(self, message):
        origin = message.get('origin')
        destination = message.get('destination')
        date = message.get('date')  # El formato recibido es YYYY-MM-DD
        
        # Ejecutar scraping para LATAM, Avianca y Aerolíneas Argentinas
        flights_data = []
        flights_data += self.scrape_latam(origin, destination, date)
        flights_data += self.scrape_avianca(origin, destination, date)
        flights_data += self.scrape_aerolineas_argentinas(origin, destination, date)
        
        return flights_data

    def scrape_latam(self, origin, destination, date):
        url_latam = f"https://www.latamairlines.com/ar/es/ofertas-vuelos?origin={origin}&inbound=null&outbound={date}T12%3A00%3A00.000Z&destination={destination}&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED"
        print(f"URL generado para LATAM: {url_latam}")
        
        try:
            driver = webdriver.Chrome()
            driver.get(url_latam)
            
            # Esperar un tiempo para que la página cargue completamente
            print("Página de LATAM cargada. Esperando manualmente a que aparezcan los resultados...")
            time.sleep(15)
            
            # Esperar hasta que el primer precio esté visible
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.latam-typography--heading-06.displayCurrencystyle__CurrencyAmount-sc__sc-hel5vp-2")))

            print("El precio del vuelo de LATAM está visible, procediendo con el scraping...")

            # Extraer el precio del vuelo disponible
            price = driver.find_element(By.CSS_SELECTOR, "span.latam-typography--heading-06.displayCurrencystyle__CurrencyAmount-sc__sc-hel5vp-2").text

            # Extraer la hora de salida
            departure_time = driver.find_elements(By.CSS_SELECTOR, ".flightInfostyle__TextHourFlight-sc__sc-169zitd-4")[0].text

            # Extraer la hora de llegada
            arrival_time = driver.find_elements(By.CSS_SELECTOR, ".flightInfostyle__TextHourFlight-sc__sc-169zitd-4")[1].text

            # Imprimir los datos para verificar
            print(f"LATAM - Precio: {price}, Hora de salida: {departure_time}, Hora de llegada: {arrival_time}")

            # Crear el diccionario con los datos extraídos
            flight_data = {
                'airline': 'LATAM',
                'price': price,
                'departure_time': departure_time,
                'arrival_time': arrival_time
            }

            driver.quit()
            return [flight_data]
        
        except Exception as e:
            print(f"Error scraping LATAM: {e}")
            driver.quit()
            return []

    def scrape_avianca(self, origin, destination, date):
        url_avianca = f"https://www.avianca.com/es/booking/select/?origin1={origin}&destination1={destination}&departure1={date}&adt1=1&tng0&inf1=0&currency=ARS&posCode=AR"
        print(f"URL generado para Avianca: {url_avianca}")
        
        try:
            driver = webdriver.Chrome()
            driver.get(url_avianca)
            
            # Esperar un tiempo para que la página cargue completamente
            print("Página de Avianca cargada. Esperando manualmente a que aparezcan los resultados...")
            time.sleep(15)
            
            # Esperar hasta que el contenedor del precio esté visible
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.journey_price-currency")))

            print("El precio del vuelo de Avianca está visible, procediendo con el scraping...")

            # Extraer el precio completo del contenedor "journey_price-currency"
            price_full = driver.find_element(By.CSS_SELECTOR, "div.journey_price-currency").text.strip()

            # Limpiar el precio, eliminando 'Desde', 'ARS', y los decimales
            price_clean = price_full.split("\n")[2]  # Extrae solo el valor numérico principal

            # Extraer la hora de salida
            departure_time = driver.find_element(By.CSS_SELECTOR, "div.journey-schedule_time-departure").text

            # Extraer la hora de llegada
            arrival_time = driver.find_element(By.CSS_SELECTOR, "div.journey-schedule_time-return").text

            # Imprimir los datos para verificar
            print(f"Avianca - Precio: {price_clean}, Hora de salida: {departure_time}, Hora de llegada: {arrival_time}")

            # Crear el diccionario con los datos extraídos
            flight_data = {
                'airline': 'Avianca',
                'price': price_clean,
                'departure_time': departure_time,
                'arrival_time': arrival_time
            }

            driver.quit()
            return [flight_data]
        
        except Exception as e:
            print(f"Error scraping Avianca: {e}")
            driver.quit()
            return []

    def scrape_aerolineas_argentinas(self, origin, destination, date):
        # Formatear la fecha de YYYY-MM-DD a YYYYMMDD para la URL de Aerolíneas Argentinas
        date_formatted = date.replace("-", "")
        
        url_aerolineas = f"https://www.aerolineas.com.ar/flights-offers?adt=1&inf=0&chd=0&flexDates=false&cabinClass=Economy&flightType=ONE_WAY&leg={origin}-{destination}-{date_formatted}"
        print(f"URL generado para Aerolíneas Argentinas: {url_aerolineas}")
        
        try:
            driver = webdriver.Chrome()
            driver.get(url_aerolineas)
            
            # Esperar un tiempo para que la página cargue completamente
            print("Página de Aerolíneas Argentinas cargada. Esperando manualmente a que aparezcan los resultados...")
            time.sleep(15)
            
            # Esperar hasta que el contenedor del precio esté visible
            wait = WebDriverWait(driver, 60)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "label.styled__Fare-l1i8es-3.cKeNDT.label-fare")))

            print("El precio del vuelo de Aerolíneas Argentinas está visible, procediendo con el scraping...")

            # Extraer el precio
            price = driver.find_element(By.CSS_SELECTOR, "label.styled__Fare-l1i8es-3.cKeNDT.label-fare").text.strip()

            # Extraer la hora de salida
            departure_time = driver.find_element(By.CSS_SELECTOR, "div.ItineraryDetails__Hour-w7o1ng-2.FEvou.label-hour").text

            # Extraer la hora de llegada
            arrival_time = driver.find_elements(By.CSS_SELECTOR, "div.ItineraryDetails__Hour-w7o1ng-2.FEvou.label-hour")[1].text

            # Imprimir los datos para verificar
            print(f"Aerolíneas Argentinas - Precio: {price}, Hora de salida: {departure_time}, Hora de llegada: {arrival_time}")

            # Crear el diccionario con los datos extraídos
            flight_data = {
                'airline': 'Aerolíneas Argentinas',
                'price': price,
                'departure_time': departure_time,
                'arrival_time': arrival_time
            }

            driver.quit()
            return [flight_data]
        
        except Exception as e:
            print(f"Error scraping Aerolíneas Argentinas: {e}")
            driver.quit()
            return []
