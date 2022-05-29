from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import time
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists


# and if it doesn't exist, download it automatically,
# then add chromedriver to path


def launchBrowser():
    driver = webdriver.Chrome()
    driver.get("https://orteil.dashnet.org/experiments/cookie/")
    return driver

def buy_worker():
    prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
    item_price = [int(price.text.split(" ")[-1].replace(",", "")) for price in prices if
                  price.text != ""]

    upgrades = dict()
    for n in range(len(item_price)):
        upgrades[item_price[n]] = upgrades_ids[n]

    available = []
    for upgrade in upgrades.keys():
        if cookies >= upgrade:
            available.append(upgrade)

    available.reverse()

    if len(available) > 0:
        driver.find_element(By.ID, upgrades[available[0]]).click()
        print(f"buy: {upgrades[available[0]]}")
        return upgrades[available[0]]
    else:
        return None

driver = launchBrowser()

cookie = driver.find_element(By.ID, "cookie")
money = driver.find_element(By.ID, "money")
cookies_per_second = driver.find_element(By.ID, "cps")

store = driver.find_elements(By.CSS_SELECTOR, "#store div")
upgrades_ids = [item.get_attribute("id") for item in store]
print(upgrades_ids)

timeout = time() + 60 * 5
last_buy = time()

last_buy_diff = 4

while True:
    cookie.click()
    print(money.text)
    try:
        cookies = int(money.text.replace(",", ""))
    except ValueError:
        cookies = 0

    if time() - last_buy > last_buy_diff:
        bought_item = buy_worker()

        if bought_item == "buyElder Pledge":
            buy_worker()

        last_buy = time()

    if time() > timeout:
        print(f"Cookies per second: {cookies_per_second.text}")
        timeout = time() + 60 * 5
        last_buy_diff += 4

# cursor_price = int(driver.find_element(By.CSS_SELECTOR, "#buyCursor > b").text.split(" ")[-1].replace(",",""))
# grandma_price = int(driver.find_element(By.CSS_SELECTOR, "#buyGrandma > b").text.split(" ")[-1].replace(",",""))
# factory_price = int(driver.find_element(By.CSS_SELECTOR, "#buyFactory > b").text.split(" ")[-1].replace(",",""))
# mine_price = int(driver.find_element(By.CSS_SELECTOR, "#buyMine > b").text.split(" ")[-1].replace(",",""))
# shipment_price = int(driver.find_element(By.CSS_SELECTOR, "#buyShipment > b").text.split(" ")[-1].replace(",",""))
# lab_price = int(driver.find_element(By.CSS_SELECTOR, "#buyAlchemy\ lab > b").text.split(" ")[-1].replace(",",""))
# portal_price = int(driver.find_element(By.CSS_SELECTOR, "#buyPortal > b").text.split(" ")[-1].replace(",",""))
# elder_pledge = int(driver.find_element(By.CSS_SELECTOR, "#buyElder\ Pledge > b").text.split(" ")[-1].replace(",",""))
# time_machine_price = int(driver.find_element(By.CSS_SELECTOR, "#buyTime\ machine > b").text.split(" ")[-1].replace(",",""))
#
# while True:
#     cookie.click()
#
#     try:
#         cookies = int(money.text.replace(",",""))
#     except ValueError:
#         cookies = 0
#
#     if time() - last_buy > 3:
#         last_buy = time()
#
#         cursor_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyCursor > b").text.split(" ")[-1].replace(",",
#                                                                                                ""))
#         grandma_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyGrandma > b").text.split(" ")[-1].replace(",",
#                                                                                                 ""))
#         factory_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyFactory > b").text.split(" ")[-1].replace(",",
#                                                                                                 ""))
#         mine_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyMine > b").text.split(" ")[-1].replace(",",
#                                                                                              ""))
#         shipment_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyShipment > b").text.split(" ")[-1].replace(
#                 ",", ""))
#         lab_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyAlchemy\ lab > b").text.split(" ")[
#                 -1].replace(",", ""))
#         portal_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyPortal > b").text.split(" ")[-1].replace(",",
#                                                                                                ""))
#
#         elder_pledge_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyElder\ Pledge > b").text.split(" ")[-1].replace(",",
#                                                                                                ""))
#         time_machine_price = int(
#             driver.find_element(By.CSS_SELECTOR, "#buyTime\ machine > b").text.split(" ")[
#                 -1].replace(",", ""))
#
#         if cookies >= time_machine_price:
#             buy_time_machine = driver.find_element(By.ID, "buyTime machine")
#             buy_time_machine.click()
#             print("buy time machine")
#         elif cookies >= portal_price and portal_price < 70000000:
#             buy_portal = driver.find_element(By.ID, "buyPortal")
#             buy_portal.click()
#             print("buy portal")
#         elif cookies >= elder_pledge_price and elder_pledge_price < 500000:
#             buy_portal = driver.find_element(By.ID, "buyElder pledge")
#             buy_portal.click()
#             print("buy elder edge")
#         elif cookies >= lab_price and lab_price < 333333:
#             buy_lab = driver.find_element(By.ID, "buyAlchemy lab")
#             buy_lab.click()
#             print("buy lab")
#         elif cookies >= shipment_price and shipment_price < 25000:
#             buy_shipment = driver.find_element(By.ID, "buyShipment")
#             buy_shipment.click()
#             print("buy shipment")
#         elif cookies >= mine_price and mine_price < 3500:
#             buy_mine = driver.find_element(By.ID, "buyMine")
#             buy_mine.click()
#             print("buy mine")
#         elif cookies >= factory_price and factory_price < 1000:
#             buy_factory = driver.find_element(By.ID, "buyFactory")
#             buy_factory.click()
#             print("buy factory")
#         elif cookies >= grandma_price and grandma_price < 250:
#             buy_grandma = driver.find_element(By.ID, "buyGrandma")
#             buy_grandma.click()
#             print("buy grandma")
#         elif cookies >= cursor_price and cursor_price < 25:
#             buy_cursor = driver.find_element(By.ID, "buyCursor")
#             buy_cursor.click()
#             print("buy cursor")
#         else:
#             print(f"buy nothing - Cookies: {cookies}")
#
#
#     if time() > timeout:
#         print(f"Cookies per second: {cookies_per_second.text}")
#         timeout = time() + 60 * 5


# driver.quit()
