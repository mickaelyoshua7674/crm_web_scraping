from CRM import CRM
import pandas as pd
import pickle as pk
from selenium.common.exceptions import UnexpectedAlertPresentException
from time import sleep
import os


FILE_NAME = "crm_pb_data.csv"
LAST_PAGE_NAME = "last_collected_page.pkl"
LAST_ESPEC_NAMNE = "last_collected_espec.pkl"
COLUMNS = ["nome", "crm", "data_inscricao", "prim_inscricao", "inscricao", "situacao", "especialidades", "endereco", "telefone"]
CHROMEDRIVER_PATH = "chromedriver.exe"

def main():
    # Init object
    crm_bot = CRM(CHROMEDRIVER_PATH)
    crm_bot.driver.get("https://crmpb.org.br/busca-medicos/")

    if not os.path.exists(FILE_NAME): # if file don't exist create an empty csv
        pd.DataFrame(columns=COLUMNS).to_csv(FILE_NAME, header=True, index=False)

    # init last collected page as 0, if there is a variable saved then load the variable
    last_collected_page = 0
    if os.path.exists(LAST_PAGE_NAME):
        with open(LAST_PAGE_NAME, "rb") as f:
            last_collected_page = pk.load(f)

    # init last collected espec as "Todas", if there is a variable saved then load the variable
    # init with "Todas" because when split the list the split will happen with the given value, so with "Todas" the split will just remove the element "Todas"
    last_collected_espec = "Todas"
    if os.path.exists(LAST_ESPEC_NAMNE):
        with open(LAST_ESPEC_NAMNE, "rb") as f:
            last_collected_espec = pk.load(f)

    espec = crm_bot.get_values_from_field_form("especialidade")
    crm_bot.random_sleep(1,2)
    
    try:
        for e in espec[espec.index(last_collected_espec)+1:]:
            crm_bot.fill_form(uf="PB", mun="João Pessoa", espec=e)
            crm_bot.random_sleep(5,6)

            last_page = crm_bot.get_last_page()
            if 0 < last_collected_page < last_page:
                print("Going to last collected page...")
                crm_bot.go_to_page(last_collected_page+1)

            active_page = crm_bot.get_active_page()
            if active_page == last_page:
                crm_bot.concat_data(FILE_NAME, COLUMNS)
            else:
                while True:
                    crm_bot.concat_data(FILE_NAME, COLUMNS)
                    with open(LAST_PAGE_NAME, "wb") as f:
                        pk.dump(active_page, f) # save last page collected

                    active_page = crm_bot.get_active_page()
                    if active_page >= last_page:
                        break
                    crm_bot.go_to_page(active_page+1)

            with open(LAST_ESPEC_NAMNE, "wb") as f:
                pk.dump(e, f)
            if os.path.exists(LAST_PAGE_NAME):
                os.remove(LAST_PAGE_NAME)

        crm_bot.driver.quit()

    except UnexpectedAlertPresentException:
        print("UnexpectedAlertPresentException!\nSleeping for 30min...")
        crm_bot.driver.quit()
        sleep(30*60)
        print("Go again!\n\n")
        main()

main()