from flask import Flask, render_template, redirect, url_for, jsonify, stream_with_context, Response, request
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
screenshots_dir = 'screenshots'
coupons_file = 'coupons.txt'
logs = []

# Ensure the screenshots directory exists
if not os.path.exists(screenshots_dir):
    os.makedirs(screenshots_dir)

# Initialize visited links and coupon data
visited_links = set()
egg_data = []

def log(message):
    logs.append(message)
    print(message)

def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

def extract_easter_egg_info(driver):
    try:
        easter_egg_main = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'easterEggMain'))
        )
        driver.execute_script("arguments[0].click();", easter_egg_main)

        popup_eggs = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'popup-eggs'))
        )

        egg_coupon_code = popup_eggs.find_element(By.NAME, 'coupon_code').get_attribute('value')
        egg_congrats_div = popup_eggs.find_element(By.CLASS_NAME, 'egg-coupon-congrats')
        egg_congrats_text = egg_congrats_div.get_attribute('innerText').strip()
        form = popup_eggs.find_element(By.CLASS_NAME, 'saveeggcus')
        form_content = form.get_attribute('outerHTML')

        return egg_coupon_code, egg_congrats_text, form_content
    except Exception as e:
        log(f"Error extracting easter egg info: {e}")
        return None, None, None

def append_text_file(file_path, data):
    with open(file_path, 'a') as file:
        for code, congrats_text, form_content in data:
            details_discount = f"{congrats_text} {form_content}".strip()
            file.write(f"Cod discount: {code}\nDetalii discount: {details_discount}\n\n")

@app.route('/')
def index():
    return render_template('index.html', coupons=egg_data)

@app.route('/run_script')
def run_script():
    num_discounts = int(request.args.get('num_discounts', 10))
    def generate():
        global egg_data
        egg_data = []
        logs.clear()
        driver = initialize_driver()
        driver.get('https://www.cupio.ro/')

        main_window = driver.current_window_handle
        product_counter = 0

        while product_counter < num_discounts:
            products = driver.find_elements(By.CLASS_NAME, 'product-item-info')
            products = [product for product in products if product.find_element(By.TAG_NAME, 'a').get_attribute('href') not in visited_links]

            if not products:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                products = driver.find_elements(By.CLASS_NAME, 'product-item-info')
                products = [product for product in products if product.find_element(By.TAG_NAME, 'a').get_attribute('href') not in visited_links]

            if not products:
                log("Nu au fost găsite produse noi. Ieșire.")
                yield "data: Nu au fost găsite produse noi. Ieșire.\n\n"
                break

            for product in products:
                if product_counter >= num_discounts:
                    break

                product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
                visited_links.add(product_link)
                log(f"Deschidere link produs într-o filă nouă: {product_link}")
                yield f"data: Deschidere link produs într-o filă nouă: {product_link}\n\n"
                driver.execute_script("window.open(arguments[0]);", product_link)
                product_counter += 1
                progress = (product_counter / num_discounts) * 100
                yield f"data: Progres: {progress}%\n\n"
                time.sleep(1)

            if product_counter >= num_discounts:
                break

        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                egg_coupon_code, egg_congrats_text, form_content = extract_easter_egg_info(driver)
                if egg_coupon_code and egg_congrats_text and form_content:
                    egg_data.append((egg_coupon_code, egg_congrats_text, form_content))
                    log(f"Extras: Cod discount - {egg_coupon_code}, Detalii discount - {form_content}")
                    append_text_file(coupons_file, [(egg_coupon_code, egg_congrats_text, form_content)])
                    yield f"data: Extras: Cod discount - {egg_coupon_code}, Detalii discount - {form_content}\n\n"
                driver.close()

        driver.switch_to.window(main_window)
        driver.quit()

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/get_coupons')
def get_coupons():
    return jsonify(egg_data)

@app.route('/get_previous_coupons')
def get_previous_coupons():
    if os.path.exists(coupons_file):
        with open(coupons_file, 'r') as file:
            previous_coupons = file.read().strip().split("\n\n")
            return jsonify(previous_coupons)
    return jsonify([])

@app.route('/reset_coupons', methods=['GET'])
def reset_coupons():
    try:
        if os.path.exists(coupons_file):
            with open(coupons_file, 'w') as file:
                file.write('')  # Clear contents of coupons.txt
            return 'coupons.txt reset successfully.'
        else:
            return 'coupons.txt does not exist.'
    except Exception as e:
        return f'Error resetting coupons.txt: {str(e)}'
    
if __name__ == '__main__':
    app.run(debug=True)
