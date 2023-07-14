from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time, random
from datetime import datetime

def print_current_hour() -> None:
    """Print the current hour:min:sec"""
    now = datetime.now()
    print(f"Current time {now.hour}:{now.minute}:{now.second}")

def random_sleep(i: int, f: int) -> None:
    """Randomly choose a float number between i-f and sleep during that random time"""
    time.sleep(random.uniform(i, f))

def fill_form(driver) -> None:
    """Fill UF as PB and show search"""
    # SELECT UF -> PB / SHOW DATA
    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.CSS_SELECTOR, ".form.panel"))
    random_sleep(1,3)
    driver.find_element(By.ID, "uf").click()
    random_sleep(1,3)
    Select(driver.find_element(By.ID, "uf")).select_by_value("PB")
    print("UF PB selected.")
    random_sleep(1,3)
    driver.find_element(By.TAG_NAME, "body").click()
    random_sleep(1,3)
    driver.find_element(By.CSS_SELECTOR, ".w-100.btn-buscar.btnPesquisar").click()
    print("Page 1")
    random_sleep(5,7)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    random_sleep(1,3)

def get_doctor_data(div) -> dict:
    """Get the data from the given div object"""
    name = div.find_element(By.TAG_NAME, "h4").text
    random_sleep(1,2)
    crm, data_inscricao, prim_inscricao, inscricao = [t.text.split(" ")[-1] for t in div.find_elements(By.CSS_SELECTOR, ".col-md-4")]
    random_sleep(1,2)
    situacao = div.find_element(By.CSS_SELECTOR, ".col-md").text.split(" ")[-1]
    random_sleep(1,2)
    endereco = div.find_element(By.CSS_SELECTOR, ".row.endereco").find_element(By.TAG_NAME, "div").text
    random_sleep(1,2)
    telefone = div.find_element(By.CSS_SELECTOR, ".row.telefone").find_element(By.TAG_NAME, "div").text
    {
        "crm": crm,
        "name": name,
        "data_inscricao": data_inscricao,
        "prim_inscricao": prim_inscricao,
        "inscricao": inscricao,
        "situacao": situacao,
        "endereco": endereco,
        "telefone": telefone
    }
    return [crm, name, data_inscricao, prim_inscricao, inscricao, situacao, endereco, telefone]