from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time, random, json

CHROMEDRIVER_PATH = "chromedriver.exe"

def random_sleep(i: int, f: int) -> None:
    """Randomly choose a float number between i-f and sleep during that random time"""
    time.sleep(random.uniform(i, f))

def get_doctor_data(div) -> dict:
    """Get the data from the given div object"""
    name = div.find_element(By.TAG_NAME, "h4").text
    random_sleep(1,3)
    crm, data_inscricao, prim_inscricao, inscricao = [t.text.split(" ")[-1] for t in div.find_elements(By.CSS_SELECTOR, ".col-md-4")]
    random_sleep(1,3)
    situacao = div.find_element(By.CSS_SELECTOR, ".col-md").text.split(" ")[-1]
    random_sleep(1,3)
    endereco = div.find_element(By.CSS_SELECTOR, ".row.endereco").find_element(By.TAG_NAME, "div").text
    random_sleep(1,3)
    telefone = div.find_element(By.CSS_SELECTOR, ".row.telefone").find_element(By.TAG_NAME, "div").text
    return {
        "crm": crm,
        "name": name,
        "data_inscricao": data_inscricao,
        "prim_inscricao": prim_inscricao,
        "inscricao": inscricao,
        "situacao": situacao,
        "endereco": endereco,
        "telefone": telefone
    }

# op = webdriver.ChromeOptions()
# op.add_argument("headless") # don't open a Chrome window
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)#, options=op)

# SELECT UF -> PB / SHOW DATA
driver.get("https://crmpb.org.br/busca-medicos/")
random_sleep(3,5)
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

# GET FIRST PAGE DATA AND SAVE
print("Getting data...")
divs_med = [d for d in driver.find_element(By.CSS_SELECTOR, ".busca-resultado").find_elements(By.TAG_NAME, "div")
            if "resultado-item resultMedico_" in d.get_attribute("class")]
random_sleep(1,3)
data = [get_doctor_data(div) for div in divs_med]
print("Data collected.\n")
with open("crm_data.json", "w") as f:
    json.dump(data, f)

# GET DATA FROM THE FOLLOWING PAGES
last_page = int([p.get_attribute("data-num") for p in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")][-1])
print(last_page)
for p in range(2, last_page+1):
    random_sleep(5,7)
    [li for li in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")
     if li.get_attribute("data-num") == str(p)][0].click()
    print(f"Page {p}")
    random_sleep(7,9)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
    
    print("Getting data...")
    divs_med = [d for d in driver.find_element(By.CSS_SELECTOR, ".busca-resultado").find_elements(By.TAG_NAME, "div")
                if "resultado-item resultMedico_" in d.get_attribute("class")]
    random_sleep(1,3)
    data = [get_doctor_data(div) for div in divs_med]
    print("Data collected.\n")
    
    with open("crm_data.json", "r") as f:
        data += json.load(f)
    with open("crm_data.json", "w") as f:
        json.dump(data, f)

    random_sleep(1,3)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    random_sleep(1,3)
driver.quit()
