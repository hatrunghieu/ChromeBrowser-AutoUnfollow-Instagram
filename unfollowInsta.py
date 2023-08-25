import sys
from time import sleep

from selenium import webdriver  # pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import \
    ChromeDriverManager  # pip install webdriver-manager

options = webdriver.ChromeOptions()
options.add_argument("start-minimized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-notifications")
options.add_argument("--disable-extensions")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-setuid-sandbox")
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])


def exitBrowser():
    input("Press any key to exit...")
    driver.quit()
    sys.exit()


def login(username):
    try:
        driver.get("https://www.instagram.com/" + username + "/following/")
        sleep(5)
    except Exception:
        print('Login failed!')
        exitBrowser()


def unfollow(n):
    if n <= 0:
        return None
    try:
        box = driver.find_element(By.CLASS_NAME, "_aano")
        buttons = box.find_elements(By.CSS_SELECTOR, "button")
        i = 0
        for button in buttons:
            if button.text == 'Đang theo dõi' or button.text == 'Following':
                driver.execute_script(
                    "arguments[0].scrollIntoView(true);", button)
                wait = WebDriverWait(driver, 10)
                btn = wait.until(EC.element_to_be_clickable(button))
                button.click()
                sleep(1)

                confirm = driver.find_element(
                    By.CSS_SELECTOR, "button._a9--._a9-_")
                confirm.click()
                sleep(1)
                print('Unfollowed! Index =', n)
                n -= 1
                if n <= 0:
                    return None

                i += 1
                if i == 12:
                    unfollow(n)
    except Exception:
        print('Unfollow failed!')
        exitBrowser()


def main():
    InstaUsername = input("Enter your Instagram username: ")
    n = int(input("Enter number of people to unfollow: "))

    print("Please log in to your Instagram account in the browser that is about to open, then press any key to continue.")
    sleep(1)

    global driver
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)
    driver.get("https://www.instagram.com/")

    input('Press any key to continue...')
    print("Starting...")
    login(InstaUsername)

    if n <= 50:
        unfollow(n)
    else:
        for i in range(int(n/50)):
            unfollow(50)
            print('Done round %d. 50 people unfollowed!' % (i+1))
            print('Waiting 50 seconds...')
            sleep(50)
        unfollow(n % 50)

    print('Unfollowed %d people successfully!' % n)
    exitBrowser()


main()
