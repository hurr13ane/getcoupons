import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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

# Initialize a set to keep track of visited product links
visited_links = set()

# JavaScript to inject the easter egg
easter_egg_script = """
if (!document.getElementById('easterEgg')) {
    var easterEgg = document.createElement('div');
    easterEgg.id = 'easterEgg';
    easterEgg.style.position = 'fixed';
    easterEgg.style.bottom = '10px';
    easterEgg.style.right = '10px';
    easterEgg.style.padding = '10px';
    easterEgg.style.backgroundColor = 'yellow';
    easterEgg.style.border = '2px solid red';
    easterEgg.style.zIndex = '1000';
    easterEgg.innerText = 'Easter Egg! Click me to continue.';
    easterEgg.onclick = function() { window.easterEggClicked = true; };
    document.body.appendChild(easterEgg);
} else {
    window.easterEggClicked = false;
}
"""

# Function to extract easter egg code and description from a tab
def extract_easter_egg_info(driver):
    try:
        # Click on the Easter Egg element
        print("Looking for Easter Egg element...")
        easter_egg_main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'easterEggMain'))
        )
        driver.execute_script("arguments[0].click();", easter_egg_main)
        print("Easter Egg clicked.")

        # Wait for the popup to appear and extract the code and description
        print("Extracting coupon code and description...")
        egg_coupon_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'egg-coupon-code'))
        ).text
        
        egg_description = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="egg-coupon-congrats"]/p/span'))
        ).text
        
        return egg_coupon_code, egg_description
    except Exception as e:
        print(f"Error extracting easter egg info: {e}")
        return None, None

# Function to update the text file with new data
def update_text_file(file_path, data):
    with open(file_path, 'a') as file:
        for code, description in data:
            file.write(f"{code}\t{description}\n")

# Initialize a list to store the collected easter egg data
egg_data = []

# Initialize the main window handle
main_window = driver.current_window_handle

# Initialize product counter
product_counter = 0

# Path to the text file
file_path = 'coupons.txt'

# Write the header to the text file
with open(file_path, 'w') as file:
    file.write("Coupon Code\tDescription\n")

# Step 1: Open product pages in new tabs
while product_counter < 10:
    # Find all product items
    products = driver.find_elements(By.CLASS_NAME, 'product-item-info')
    
    # Filter out already visited products
    products = [product for product in products if product.find_element(By.TAG_NAME, 'a').get_attribute('href') not in visited_links]
    
    if not products:
        # Scroll down to load more products if available
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # Find products again after scrolling
        products = driver.find_elements(By.CLASS_NAME, 'product-item-info')
        products = [product for product in products if product.find_element(By.TAG_NAME, 'a').get_attribute('href') not in visited_links]
    
    if not products:
        print("No new products found. Exiting.")
        break
    
    for product in products:
        if product_counter >= 10:
            break
        
        # Get the product link
        product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
        
        # Add the product link to the visited set
        visited_links.add(product_link)
        
        # Open the product link in a new tab
        print(f"Opening product link in a new tab: {product_link}")
        driver.execute_script("window.open(arguments[0]);", product_link)
        product_counter += 1
        time.sleep(2)
    
    if product_counter >= 10:
        break

# Step 2: Extract coupon codes concurrently
for handle in driver.window_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        
        # Inject the easter egg JavaScript
        print("Injecting Easter Egg script...")
        driver.execute_script(easter_egg_script)
        time.sleep(2)
        
        # Extract the easter egg info
        egg_coupon_code, egg_description = extract_easter_egg_info(driver)
        if egg_coupon_code and egg_description:
            egg_data.append((egg_coupon_code, egg_description))
            print(f"Extracted: Code - {egg_coupon_code}, Description - {egg_description}")
            update_text_file(file_path, [(egg_coupon_code, egg_description)])
        
        # Close the current tab
        print("Closing current tab...")
        driver.close()

# Switch back to the main window
driver.switch_to.window(main_window)

# Print the collected easter egg data
print("\nCollected Easter Egg Codes and Descriptions:")
for code, description in egg_data:
    print(f"Code: {code}, Description: {description}")

# Close the driver
driver.quit()
