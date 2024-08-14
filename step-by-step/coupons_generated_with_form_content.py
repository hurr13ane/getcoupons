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

# Function to extract easter egg info from a tab
def extract_easter_egg_info(driver):
    try:
        print("Waiting for the Easter Egg to appear...")
        easter_egg_main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'easterEggMain'))
        )
        driver.execute_script("arguments[0].click();", easter_egg_main)
        print("Easter Egg clicked.")

        print("Waiting for the popup to appear...")
        popup_eggs = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'popup-eggs'))
        )

        # Extract the coupon code
        egg_coupon_code = popup_eggs.find_element(By.NAME, 'coupon_code').get_attribute('value')

        # Extract the congrats message
        egg_congrats_div = popup_eggs.find_element(By.CLASS_NAME, 'egg-coupon-congrats')
        egg_congrats_h2 = egg_congrats_div.find_element(By.TAG_NAME, 'h2').text
        egg_congrats_span = egg_congrats_div.find_element(By.TAG_NAME, 'span').text

        # Extract the content from saveeggcus form
        form = popup_eggs.find_element(By.CLASS_NAME, 'saveeggcus')
        form_content = form.get_attribute('outerHTML')

        return egg_coupon_code, egg_congrats_h2, egg_congrats_span, form_content
    except Exception as e:
        print(f"Error extracting easter egg info: {e}")
        return None, None, None, None

# Function to append the text file with new data
def append_text_file(file_path, data):
    with open(file_path, 'a') as file:
        for code, h2, span, form_content in data:
            file.write(f"Coupon Code: {code}\nCongrats H2: {h2}\nCongrats Span: {span}\nForm Content: {form_content}\n\n")

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
    file.write("Coupon Code\tCongrats H2\tCongrats Span\tForm Content\n")

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
        
        # Extract the easter egg info
        egg_coupon_code, egg_congrats_h2, egg_congrats_span, form_content = extract_easter_egg_info(driver)
        if egg_coupon_code and egg_congrats_h2 and egg_congrats_span and form_content:
            egg_data.append((egg_coupon_code, egg_congrats_h2, egg_congrats_span, form_content))
            print(f"Extracted: Coupon Code - {egg_coupon_code}, Congrats H2 - {egg_congrats_h2}, Congrats Span - {egg_congrats_span}, Form Content - {form_content}")
            append_text_file(file_path, [(egg_coupon_code, egg_congrats_h2, egg_congrats_span, form_content)])
        
        # Print the extracted information before closing the tab
        print(f"Coupon Code: {egg_coupon_code}")
        print(f"Congrats H2: {egg_congrats_h2}")
        print(f"Congrats Span: {egg_congrats_span}")
        print(f"Form Content: {form_content}")
        
        # Close the current tab
        print("Closing current tab...")
        driver.close()

# Switch back to the main window
driver.switch_to.window(main_window)

# Print the collected easter egg data
print("\nCollected Easter Egg Codes and Congrats:")
for code, h2, span, form_content in egg_data:
    print(f"Coupon Code: {code}")
    print(f"Congrats H2: {h2}")
    print(f"Congrats Span: {span}")
    print(f"Form Content: {form_content}")
    print("\n")

# Close the driver
driver.quit()
