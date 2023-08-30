from CRM import CRM
from os.path import exists
import pandas as pd
import pickle as pk

FILE_NAME = "crm_pb_data.csv"
COLUMNS = ["nome", "crm", "data_inscricao", "prim_inscricao", "inscricao", "situacao", "endereco", "telefone"]
CHROMEDRIVER_PATH = "chromedriver.exe"

if not exists(FILE_NAME): # if file don't exist create an empty csv
    pd.DataFrame(columns=COLUMNS).to_csv(FILE_NAME, header=True, index=False)

# init last collected page as 0, if there is a variable saved then load the variable
last_collected_page = 0
if exists("last_collected_page.pkl"):
    with open("last_collected_page.pkl", "rb") as f:
        last_collected_page = pk.load(f)

crm_bot = CRM(CHROMEDRIVER_PATH)
crm_bot.driver.get("https://crmpb.org.br/busca-medicos/")
crm_bot.random_sleep(3,5)
crm_bot.fill_form()

last_page = crm_bot.get_last_page()
if 0 < last_collected_page < last_page:
    print("Going to last collected page...")
    crm_bot.go_to_page(last_collected_page+1)

active_page = crm_bot.get_active_page()
current_page = loop_count = 0
while active_page < last_page or loop_count < 10:
    
    if active_page != current_page: # after clicking to next page, if it is now a different page, then collect data
        print("Getting data...")
        crm_bot.random_sleep(1,2)
        data = crm_bot.get_doctors_data()
        print("Data collected.\n")

        for crm in [d[1] for d in data]:
            if crm in pd.read_csv(FILE_NAME)["crm"].unique():
                print("Data already collected.")
                exit()
                
        pd.DataFrame(data=data, columns=COLUMNS).to_csv(FILE_NAME, header=False, index=False, mode="a")
        current_page = active_page
        with open("last_collected_page.pkl", "wb") as f:
            pk.dump(active_page, f) # save last page collected
    else:
        loop_count += 1

    crm_bot.go_to_page(active_page+1)
    active_page = crm_bot.get_active_page()
crm_bot.driver.quit()