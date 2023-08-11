from helper import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from os.path import exists
import pandas as pd
import pickle as pk

CHROMEDRIVER_PATH = "chromedriver.exe"
COLUMNS = ["crm", "name", "data_inscricao", "prim_inscricao", "inscricao", "situacao", "endereco", "telefone"]

if not exists("crm_pb_data.csv"): # if file don't exist create an empty csv
    pd.DataFrame(columns=COLUMNS).to_csv("crm_pb_data.csv", header=True, index=False)

# init last collected page as 0, if there is a variable saved then load the variable
last_collected_page = 0
if exists("last_collected_page.pk"):
    with open("last_collected_page.pkl", "rb") as f:
        last_collected_page = pk.load(f)

# op = webdriver.ChromeOptions()
# op.add_argument("headless") # don't open a Chrome window
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)#, options=op)
driver.get("https://crmpb.org.br/busca-medicos/")
random_sleep(3,5)
fill_form(driver)

# get last page
last_page = int([p.get_attribute("data-num") for p in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")][-1])
if last_collected_page > 0:
    pages = [p for p in range(last_collected_page+1, last_page+1)]
    go_to_last_collected_page(driver, last_collected_page)
else:
    pages = [p for p in range(1, last_page+1)]

for p in pages:
    if p == 1:
        # GET FIRST PAGE DATA AND SAVE
        random_sleep(1,3)
        print_current_hour()
        print("Getting data...")
        data = get_doctors_data(driver)
        print("Data collected.\n")
        pd.DataFrame(data=data, columns=COLUMNS).to_csv("crm_pb_data.csv", header=False, index=False, mode="a") # concatenate into dataframe
    else:
        print_current_hour()
        random_sleep(5,7)
        click_page(driver, p)
        print(f"Page {p}")
        random_sleep(7,9)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME) # Click Home button and go up
        
        print("Getting data...")
        data = get_doctors_data(driver)
        print("Data collected.\n")
        pd.DataFrame(data=data, columns=COLUMNS).to_csv("crm_pb_data.csv", header=False, index=False, mode="a")
        random_sleep(1,3)

        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END) # Click End button and go down
        random_sleep(1,3)
        
        with open("last_collected_page.pkl", "wb") as f:
            pk.dump(p, f) # save last page collected
driver.quit()