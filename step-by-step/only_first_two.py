#only for first two products

import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Ensure the screenshots directory exists
screenshots_dir = 'screenshots'
if not os.path.exists(screenshots_dir):
    os.makedirs(screenshots_dir)

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the initial Cupio product page (replace with actual URL)
driver.get('https://www.cupio.ro/ulei-cuticule-cu-glitter-cupio-sunkissed-10ml')

# Give the page some time to load
time.sleep(5)

# Initialize ActionChains for scrolling
actions = ActionChains(driver)

# Initialize a set to keep track of visited product links
visited_links = set()

# JavaScript to inject the easter egg
easter_egg_script = """
var easterEgg = document.createElement('div');
easterEgg.style.position = 'fixed';
easterEgg.style.bottom = '10px';
easterEgg.style.right = '10px';
easterEgg.style.padding = '10px';
easterEgg.style.backgroundColor = 'yellow';
easterEgg.style.border = '2px solid red';
easterEgg.style.zIndex = '1000';
easterEgg.innerText = 'Easter Egg!';
document.body.appendChild(easterEgg);
"""

# Scroll through the products and process them continuously
while True:
    # Find all product items
    products = driver.find_elements(By.CLASS_NAME, 'product-item-info')
    
    # Filter out already visited products
    products = [product for product in products if product.find_element(By.TAG_NAME, 'a').get_attribute('href') not in visited_links]
    
    if not products:
        print("No new products found on this page. Exiting.")
        break
    
    # Randomly select a product from the list
    product = random.choice(products)
    
    # Scroll to the product
    actions.move_to_element(product).perform()
    
    # Wait for 5 seconds
    time.sleep(5)
    
    # Get the product link
    product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
    
    # Add the product link to the visited set
    visited_links.add(product_link)
    
    # Click on the product to open its page
    product.click()
    
    # Wait for the product page to load
    time.sleep(5)
    
    # Inject the easter egg JavaScript
    driver.execute_script(easter_egg_script)
    
    # Get the product name
    product_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'page-title'))  # Replace with the actual class name for the product name
    )
    product_name = product_name_element.text.strip().replace(" ", "_").replace("/", "-")  # Ensure valid filename
    
    # Take a screenshot and save it
    screenshot_path = os.path.join(screenshots_dir, f"{product_name}.png")
    driver.save_screenshot(screenshot_path)
    
    # Wait for 5 seconds before proceeding to the next product
    time.sleep(5)
    
    # Go to a random new product by navigating directly to its link
    driver.get(product_link)
    
    # Wait for the new product page to load
    time.sleep(5)

# Close the driver (the loop will run indefinitely until manually stopped)
# driver.quit()
