import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By


def search(request):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless=old')

    driver = webdriver.Chrome(options=option)

    driver.get('https://www.google.com/search?q=' + request)

    result = driver.find_element(By.CLASS_NAME, 'yuRUbf').find_element(By.TAG_NAME, 'a').get_attribute('href')

    driver.quit()

    webbrowser.open(result)

