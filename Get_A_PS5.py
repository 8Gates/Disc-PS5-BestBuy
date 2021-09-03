import winsound
import time
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc    # pip install undetected-chromedriver
from selenium.webdriver.support.ui import WebDriverWait


username = ''
password = ''
sku_id = "'6426149'"    # sku-id for product to purchase
count = 0
continue_run = True
options = uc.ChromeOptions()
options.headless = True
headless_driver = uc.Chrome(options=options)
url = "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149"


try:
    headless_driver.get(url)
except:
    print("Error accessing URL.")
    headless_driver.quit()

def in_stock(headless_driver, sku):
    """Headless check if button displays sold out."""
    element = WebDriverWait(headless_driver, 8).until(lambda d: d.find_element_by_xpath("//button[@data-sku-id="+sku+"]"))
    if element.text == "Sold Out":
        return False
    else:
        return True


def add_to_cart(url, sku):
    # alert user stock may be available
    for i in range(3):
        winsound.Beep(440, 200)
    options = Options()                     
    options.headless = False
    options.page_load_strategy = 'eager'    
    driver = uc.Chrome(options=options)
    driver.get(url)
    """Adds item to cart and checks out. Not headless."""
    try:
        # add item to the cart
        driver.find_element_by_xpath("//button[@data-sku-id="+sku+"]").click()
        time.sleep(2)
        # go to the cart
        driver.find_element_by_xpath("//div[@class='go-to-cart-button']").click()
        time.sleep(2)
        # in cart checkout
        driver.find_element_by_xpath("//button[@data-track='Checkout - Top']").click()
        time.sleep(2)
        # sign in to profile
        driver.find_element_by_xpath("//input[@type='email']").send_keys(username)
        driver.find_element_by_xpath("//input[@type='password']").send_keys(password)
        driver.find_element_by_xpath("//button[@data-track='Sign In']").click()
        time.sleep(2)
        # place your order
        driver.find_element_by_xpath("//button[@data-track='Place your Order - Contact Card']").click()

        # hangs the browser so you can verify purchase before closing
        user_input = 'loop'
        while user_input != 'exit':
            user_input = input("Purchase successful! Enter 'exit' to quit:  ")
        return

    except:
        user_input = 'loop'
        while user_input != 'exit':
            user_input = input("An error occurred while checking out. Enter 'exit' to quit:")
        return


while continue_run:
    # check for stock, add to cart and checkout
    if in_stock(headless_driver, sku_id):
        add_to_cart(url, sku_id)
        continue_run = False
    else:
        count+=1
        print("Out of Stock. #"+ str(count))
    time.sleep(30)
