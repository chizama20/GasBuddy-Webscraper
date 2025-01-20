import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

zip_code = input("Enter a zip code: ")
gas_type = input("Enter the gas type (e.g., Regular, Midgrade, Premium, Diesel, E85, UNL88): ")

time.sleep(5)
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

scraped_data = []
try:
    
    driver.get("https://www.gasbuddy.com/home")
    
    #zip code
    input_element = driver.find_element(By.ID, "search")
    input_element.send_keys(zip_code)

    #Gas type
    dropdown_element = driver.find_element(By.ID, "searchFuelType")
    select = Select(dropdown_element)
    try:
        select.select_by_visible_text(gas_type)  # Select the gas type by visible text
    except:
        print(f"Invalid gas type '{gas_type}' entered. Using 'Regular' as default.")
        select.select_by_visible_text("Regular")


    time.sleep(.5)
    #search button
    search_button = driver.find_element(By.CLASS_NAME, "GasPriceSearchForm-module__submitButton___3m4SZ")
    search_button.click()
    time.sleep(3)

    #stations
    stations = driver.find_elements(By.CLASS_NAME, "GenericStationListItem-module__station___1O4vF")

    for station in stations:
        name = station.find_element(By.CLASS_NAME, 'StationDisplay-module__stationNameHeader___1A2q8').text
        address = station.find_element(By.CLASS_NAME, "StationDisplay-module__address___2_c7v").text
        rating = station.find_element(By.CLASS_NAME, "StationDisplay-module__ratingContainer___23GOL").text
        try:
            price = station.find_element(By.CLASS_NAME, "StationDisplayPrice-module__price___3rARL").text
        except:
            price = "N/A"

        scraped_data.append({
            'Station Name': name,
            'Address': address,
            'Rating': rating,
            'Price': price
        })

        df = pd.DataFrame(scraped_data)
        df.to_excel('gas_station_data.xlsx', index=False)

        print(f"Station Name: {name}")
        print(f"Rating: {rating} rating")
        print(f"Address: {address}")
        print(f"Price: {price}")
        print("-" * 40)
        

    print("\n\nDATA HAS BEEN SAVED TO 'gas_station_data.xlsx' AS WELL. \n\n\n\n")
    time.sleep(20)

finally:
    driver.quit()
