from selenium import webdriver  # pip install selenium
from webdriver_manager.chrome import ChromeDriverManager   # pip install webdriver-manager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("start-minimized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.page_load_strategy = 'eager'
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.addArguments("--headless")
# options.add_argument("--no-sandbox")

winUser = input("Enter your Windows username: ")
InstaUser = input("Enter your Instagram username: ")
n = int(input("Enter number of people to unfollow: "))
print("Please log in to your Instagram account in the browser that is about to open. Then press any key to continue...")
sleep(3)
options.add_argument("user-data-dir=C:\\Users\\"+ winUser +"\\AppData\\Local\\Google\\Chrome\\User Data")   #Change user data dir here
options.add_argument("profile-directory=Default")   #Change user profile here
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
input()
print("Starting...")

def exitBrowser():
    input("Press any key to exit...")
    driver.quit()
    exit()

def login(InstaUser):
    try:
        driver.get("https://www.instagram.com/"+ InstaUser +"/following/")
        sleep(5)
        # cookies = pickle.load(open( "cookies.pkl", "rb"))
        # for cookie in cookies:
        #     driver.add_cookie(cookie)
        # driver.refresh()
        # sleep(5)
    except Exception as e:
        print('Login failed!', e)
        exitBrowser()

def unfollow(n):
    try:
        box = driver.find_element(By.CLASS_NAME, "_aano")
        buttons = box.find_elements(By.CSS_SELECTOR, "button")
        i = 0
        for button in buttons:
            if button.text == 'Đang theo dõi':
                # driver.execute_script("arguments[0].scrollIntoView(true);", button)
                # wait = WebDriverWait(driver, 10)
                # btn = wait.until(EC.element_to_be_clickable(button))
                button.click()
                sleep(1)
                confirm = driver.find_element(By.CSS_SELECTOR, "button._a9--._a9-_")
                confirm.click()
                sleep(1)
                print('Unfollowed!', n)
                n -= 1
                if n == 0:
                    return
                i += 1
                if i == 12:
                    unfollow(n)            
    except Exception as e:
        print('Unfollow failed!', e)
        exitBrowser()


login(InstaUser)
if n <= 50:
    unfollow(n)
else:
    for i in range(int(n/50)):
        unfollow(50)
        print('Done round %d. 50 people unfollowed!' % (i+1))
        print('Waiting 50 seconds...')
        sleep(50)
    unfollow(n%50)
print('Unfollowed %d people successfully!' % n)
exitBrowser()