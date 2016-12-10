#%%
#imports requirements from selenium as well as a few others
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import base64, time, os
#%%
#base64 encoded credentials, if supported, use keyring library instead
key = base64.b64decode('[BASE64_ENCODED_PASSWORD]')
def websitecheck(user, passw):
    #initialize webdriver
    binary = FirefoxBinary(r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe')
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.wait = WebDriverWait(driver, 30)
    driver.get("[URL]")
    check = ''
    css1 = "[CSS_SELECTOR_OF_FIRST_ITEM_TO_CHECK]"
    css2 = "[CSS_SELECTOR_OF_SECOND_ITEM_TO_CHECK]"
    #set elements to look for/interact with in a try except loop
    try:
        userbox = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[CSS_SELECTOR_OF_USERNAME_BOX]")))
        passbox = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#[CSS_SELECTOR_OF_PASSWORD_BOX]")))
        loginbutton = driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[CSS_SELECTOR_OF_LOGIN_BUTTON]")))
        userbox.send_keys(user)
        passbox.send_keys(passw)
        loginbutton.click()
        servicebutton = driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[CSS_SELECTOR_FIRST_TAB_TO_NAVIGATE_TO]")))
        servicebutton.click()
        authbutton = driver.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[CSS_SELECTOR_SECOND_TAB_TO_NAVIGATE_TO]")))
        authbutton.click()
        #check that two elements are present on the page
        try:
            time.sleep(3)
            driver.find_element(By.CSS_SELECTOR, css1)
            driver.find_element(By.CSS_SELECTOR, css2)
            check = 'Up'
        except:
            check = 'Down'
        #logout and confirm logout
        logout = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[CSS_SELECTOR_LOGOUT_BUTTON]")))
        logout.click()
        confirm = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[CSS_SELECTOR_CONFIRM_LOGOUT_BUTTON]")))
        confirm.click()
    except TimeoutException:
        print("An error has occured")
    time.sleep(3)
    #kill geckodriver and the browser window it opened
    os.system('taskkill /im geckodriver.exe /t /f')
    return check
website = websitecheck('[USERNAME]', key.decode('utf8'))