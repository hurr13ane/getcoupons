import os
import cv2
import numpy as np
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Path to the "sun" image
template_path = 'sun\sun.png'

# Directory to save screenshots
screenshot_dir = 'screenshots'
os.makedirs(screenshot_dir, exist_ok=True)

# Initialize the WebDriver (you may need to specify the path to the WebDriver executable)
driver = webdriver.Chrome()

def find_sun_image(driver, template_path):
    # Load the template image
    template = cv2.imread(template_path, 0)
    w, h = template.shape[::-1]

    # Take a screenshot of the webpage
    screenshot_path = 'screenshot.png'
    driver.save_screenshot(screenshot_path)

    # Read the screenshot
    screenshot = cv2.imread(screenshot_path, 0)

    # Perform template matching
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    if len(loc[0]) > 0:
        return True, screenshot_path
    else:
        return False, None

# Navigate to the target webpage
driver.get('https://www.cupio.ro/ulei-cuticule-cu-glitter-cupio-sunkissed-10ml')

try:
    # Wait for the product list to load (adjust the selector to fit your needs)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.product-item-info'))
    )

    while True:
        # Find all product elements
        products = driver.find_elements(By.CSS_SELECTOR, '.product-item-info')

        # Randomly select a product and click it
        product = random.choice(products)
        actions = ActionChains(driver)
        actions.move_to_element(product).perform()
        product.click()

        # Wait for the page to load the product details (adjust the selector to fit your needs)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.page-title-wrapper'))
        )

        # Check for the "sun" image
        sun_found, screenshot_path = find_sun_image(driver, template_path)

        if sun_found:
            # Find the "sun" element and click it (adjust the selector to fit your needs)
            sun_element = driver.find_element(By.CSS_SELECTOR, 'SELECTOR_FOR_SUN_IMAGE')
            sun_element.click()

            # Save the screenshot to the directory
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            save_path = os.path.join(screenshot_dir, f'screenshot_{timestamp}.png')
            os.rename(screenshot_path, save_path)
            print(f'Sun image found and saved to {save_path}')
            break

        # Navigate back to the product listing
        driver.back()

        # Wait for the product list to load again
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.product-item-info'))
        )

        # Scroll down to load more products
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Adjust the sleep time if necessary

finally:
    driver.quit()