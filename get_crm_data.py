from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

CHROMEDRIVER_PATH = "chromedriver.exe"

# op = webdriver.ChromeOptions()
# op.add_argument("headless") # don't open a Chrome window
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)#, options=op)

# SELECT UF -> PB
driver.get("https://crmpb.org.br/busca-medicos/")
time.sleep(1)
driver.find_element(By.ID, "uf").click()
time.sleep(0.5)
Select(driver.find_element(By.ID, "uf")).select_by_value("PB")
time.sleep(0.5)
print("UF PB selected.")

print(driver.find_element(By.CLASS_NAME, ".col-md-2").find_element(By.TAG_NAME, "button").text)

time.sleep(5)







driver.quit()
