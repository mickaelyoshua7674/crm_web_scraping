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
    random_sleep(5,7)
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    random_sleep(1,3)

def get_doctors_data(driver) -> dict:
    """Get the data from the given div object"""
    divs_med = [d for d in driver.find_element(By.CSS_SELECTOR, ".busca-resultado").find_elements(By.TAG_NAME, "div")
                    if "resultado-item resultMedico_" in d.get_attribute("class")] # get all doctor blocks
    random_sleep(1,3)

    return [[div.find_element(By.TAG_NAME, "h4").text,
            *[t.text.split(" ")[-1] for t in div.find_elements(By.CSS_SELECTOR, ".col-md-4")],
            div.find_element(By.CSS_SELECTOR, ".col-md").text.split(" ")[-1],
            div.find_element(By.CSS_SELECTOR, ".row.endereco").find_element(By.TAG_NAME, "div").text,
            div.find_element(By.CSS_SELECTOR, ".row.telefone").find_element(By.TAG_NAME, "div").text]
            for div in divs_med]

def click_page(driver, page: int) -> None:
    """Click the given page"""
    [li for li in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")
    if li.get_attribute("data-num") == str(page)][0].click()

def go_to_last_collected_page(driver, last_collected_page: int) -> None:
    while True:
        random_sleep(3,5)
        pages_list_obj = [li for li in driver.find_element(By.CSS_SELECTOR, ".paginationjs-pages").find_elements(By.TAG_NAME, "li")]
        try:
            pages_list_obj[[li.get_attribute("data-num") for li in pages_list_obj].index(str(last_collected_page))].click()
            break
        except ValueError:
            pages_list_obj[-3].click()