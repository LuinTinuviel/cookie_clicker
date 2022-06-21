import shutil

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import time, sleep
from datetime import datetime
from os import path
from shutil import copy
from random import choice
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists


# and if it doesn't exist, download it automatically,
# then add chromedriver to path


def launchBrowser():
    driver = webdriver.Chrome()
    driver.get("https://orteil.dashnet.org/cookieclicker/")
    return driver

def buy_products():
    available_products = driver.find_elements(By.XPATH, "//div[@class='product unlocked enabled']")

    if len(available_products) > 0:
        products_ids = [item.get_attribute("id") for item in available_products]
        if len(products_ids) > 0:
            names = []
            for upgrade in products_ids:
                names.append(driver.find_element(By.CSS_SELECTOR, f"#{upgrade} > div.content div.title"))

            prices = []
            for upgrade in products_ids:
                prices.append(driver.find_element(By.CSS_SELECTOR, f"#{upgrade} > div.content span.price"))

            product_names = [name.text for name in names]
            product_prices = [int(float(price.text.split(" ")[-1].replace(",", ""))) for price in prices if
                               price.text != ""]

            names_dict = dict()
            for n in range(len(products_ids)):
                names_dict[products_ids[n]] = product_names[n]

            products = dict()
            for n in range(len(product_prices)):
                products[product_prices[n]] = products_ids[n]

            available = []
            for product in products.keys():
                if cookies >= product:
                    available.append(product)

            available.reverse()

            if len(available) > 0:
                try:
                    driver.find_element(By.ID, products[available[0]]).click()
                except Exception:
                    print("Error during buying...")
                else:
                    print(f"buy: {names_dict[products[available[0]]]}")
                return products[available[0]]

        return None
    else:
        print("No product to buy")

def buy_upgradess():
    available_upgrades = driver.find_elements(By.XPATH, "//div[@class='crate upgrade enabled']")

    if len(available_upgrades) > 0:
        upgrade_to_buy = choice(available_upgrades)
        try:
            upgrade_to_buy.click()
        except Exception:
            print("Error during buying...")
        else:
            print(f"Upgrade bought")

def save_game():
    try:
        # go to options
        driver.find_element(By.ID, "prefsButton").click()
        sleep(5)
        # open export
        driver.find_element(By.CSS_SELECTOR, "div > div > div:nth-child(4) > a:nth-child(1)").click()
        sleep(5)
        save_str = driver.find_element(By.CSS_SELECTOR, "#textareaPrompt").text
        if save_str:
            if path.exists("save_data/save.txt"):
                shutil.copy2("save_data\\save.txt", f"save_data\\save_{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.txt")
            with open("save_data/save.txt", 'w') as file:
                file.write(save_str)
        driver.find_element(By.CSS_SELECTOR, "#promptContent > div.optionBox").click()
        sleep(1)
        # close options
        driver.find_element(By.CSS_SELECTOR, "div.close.menuClose").click()
    except Exception as e:
        print(f"Could not save data:\n{e}")

def load_game():
    try:
        # open import
        driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.CONTROL + "O")
        sleep(3)
        load_box = driver.find_element(By.CSS_SELECTOR, "#textareaPrompt")
        if load_box:
            if path.exists("save_data/save.txt"):
                with open("save_data/save.txt", 'r') as file:
                    save_str = file.read()
                    load_box.send_keys(save_str)
        driver.find_element(By.CSS_SELECTOR, "#promptOption0").click()
        sleep(1)
    except Exception as e:
        print(f"Could not load data:\n{e}")

driver = launchBrowser()
sleep(5)

# Select language:
driver.find_element(By.ID, "langSelect-EN").click()
sleep(5)

# Disable short numbers
try:
    driver.find_element(By.ID, "prefsButton").click()
    sleep(5)
    # disable fancy numbers
    driver.find_element(By.ID, "formatButton").click()
    sleep(5)
    # close options
    driver.find_element(By.CSS_SELECTOR, "div.close.menuClose").click()
except Exception as e:
    print(f"Could not close fancy numbers:\n{e}")

load_game()

cookie = driver.find_element(By.ID, "bigCookie")
money = driver.find_element(By.ID, "cookies")

store = driver.find_elements(By.CSS_SELECTOR, "#products div")
upgrades = driver.find_elements(By.CLASS_NAME, "product unlocked enabled")

timeout = time() + 60 * 5
last_buy = time()

# last_buy_diff = 4
last_buy_diff = 6940

while True:
    try:
        cookie.click()
    except Exception:
        print("Error during cookie click")

    money_split = money.text.split(" ")
    try:
        cookies = money_split[0].replace(",", "")
        cookies = int(cookies.split("\n")[0])
    except Exception:
        cookies = 0

    try:
        cookies_per_second = money_split[-1]
    except Exception:
        cookies_per_second = 0

    if time() - last_buy > last_buy_diff:

        buy_upgradess()
        sleep(1)
        bought_item = buy_products()

        last_buy = time()

        save_game()

    if time() > timeout:
        print(f"Cookies per second: {cookies_per_second}")
        timeout = time() + 60 * 5
        last_buy_diff += 4
        print(f"Buy Window length: {last_buy_diff}")
