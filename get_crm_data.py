from helper import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from os.path import exists
import pandas as pd
import pickle as pk

CHROMEDRIVER_PATH = "chromedriver.exe"
COLUMNS = ["nome", "crm", "data_inscricao", "prim_inscricao", "inscricao", "situacao", "endereco", "telefone"]

if not exists("crm_pb_data.csv"): # if file don't exist create an empty csv
    pd.DataFrame(columns=COLUMNS).to_csv("crm_pb_data.csv", header=True, index=False)

# init last collected page as 0, if there is a variable saved then load the variable
last_collected_page = 0
if exists("last_collected_page.pkl"):
    with open("last_collected_page.pkl", "rb") as f:
        last_collected_page = pk.load(f)

# op = webdriver.ChromeOptions()
# op.add_argument("headless") # don't open a Chrome window
sc = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=sc)#, options=op)
driver.get("https://crmpb.org.br/busca-medicos/")
random_sleep(3,5)
fill_form(driver)

# get last page
last_page = int([p.get_attribute("data-num") for p in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")][-1])
if 0 < last_collected_page < last_page:
    print("Going to last collected page...")
    go_to_page(driver, last_collected_page+1)

active_page = get_active_page(driver)
current_page = 0
loop_count = 0
while active_page < last_page or loop_count < 10:
    print_current_hour()
    print(f"Page {active_page}")
    
    if active_page != current_page: # after clicking to next page, if it is now a different page, then collect data
        print("Getting data...")
        data = get_doctors_data(driver)
        print("Data collected.\n")
        pd.DataFrame(data=data, columns=COLUMNS).to_csv("crm_pb_data.csv", header=False, index=False, mode="a")
        current_page = active_page
        with open("last_collected_page.pkl", "wb") as f:
            pk.dump(active_page, f) # save last page collected
    else:
        loop_count += 1

    go_to_page(driver, active_page+1)
    active_page = get_active_page(driver)
driver.quit()