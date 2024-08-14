
# Easter Egg Coupon Extractor

This is a Flask web application that automates the process of extracting coupon codes hidden as Easter eggs on a specified website. The application uses Selenium to navigate the website, interact with the Easter eggs, and extract coupon codes and related details.

## Table of Contents

1. [Easter Egg Coupon Extractor](#easter-egg-coupon-extractor)
2. [Story 1 - Running the Script for a Fixed Number of Discounts](#story-1---running-the-script-for-a-fixed-number-of-discounts)
3. [Story 2 - Resetting the Extracted Coupons](#story-2---resetting-the-extracted-coupons)
4. [Story 3 - Retrieving Previously Extracted Coupons](#story-3---retrieving-previously-extracted-coupons)
5. [Functionality](#functionality)
   - [initialize_driver()](#initialize_driver)
   - [extract_easter_egg_info(driver)](#extract_easter_egg_info-driver)
   - [append_text_file(file_path, data)](#append_text_filefile_path-data)
   - [log(message)](#logmessage)
6. [Endpoints](#endpoints)
   - [/](#)
   - [/run_script](#run_script)
   - [/get_coupons](#get_coupons)
   - [/get_previous_coupons](#get_previous_coupons)
   - [/reset_coupons](#reset_coupons)
7. [How Does it Work?](#how-does-it-work)
8. [Requirements](#requirements)
9. [Usage](#usage)
10. [Dependencies](#dependencies)
11. [Support](#support)
12. [License](#license)

## Story 1 - Running the Script for a Fixed Number of Discounts

This example shows how to run the script to extract a specified number of discounts.


# Access the application at the root endpoint, and start the script to extract 10 discounts:
http://localhost:5000/run_script?num_discounts=10
\`\`\`

The script will navigate through the products on the website, extract the Easter eggs until the specified number of discounts is reached, and then terminate.

## Story 2 - Resetting the Extracted Coupons

You can reset the list of extracted coupons by accessing the following endpoint:


# Reset the coupons file:
http://localhost:5000/reset_coupons
\`\`\`

This will clear the contents of the \`coupons.txt\` file where the coupons are stored.

## Story 3 - Retrieving Previously Extracted Coupons

To retrieve the previously extracted coupons, you can use the following endpoint:


# Retrieve previous coupons:
http://localhost:5000/get_previous_coupons
\`\`\`

This will return the contents of the \`coupons.txt\` file as a JSON array.

## Functionality

The application has several core functions:

### initialize_driver()

This function initializes the Selenium WebDriver with Chrome options to run in headless mode, making it suitable for a server environment.

### extract_easter_egg_info(driver)

This function is responsible for interacting with the website to extract coupon codes from the Easter eggs. It waits for specific elements on the page and retrieves the coupon code, congratulatory text, and form content.

### append_text_file(file_path, data)

This function appends extracted data (coupon codes and details) to a specified text file, ensuring that the extracted information is persistent.

### log(message)

This function logs messages for debugging purposes. It appends messages to a list and also prints them to the console.

## Endpoints

### /

The root endpoint renders the index page, displaying the extracted coupon codes.

### /run_script

Starts the script to extract a specified number of discounts. It streams live progress updates to the client as the script runs.

- **Query Parameters**: 
  - \`num_discounts\`: Specifies the number of discounts to extract.

### /get_coupons

Returns the currently extracted coupon codes in JSON format.

### /get_previous_coupons

Returns the coupons stored in the \`coupons.txt\` file in JSON format, allowing retrieval of past extractions.

### /reset_coupons

Resets the \`coupons.txt\` file by clearing its contents.

## How Does it Work?

1. **Initialization**: When the script is started via the \`/run_script\` endpoint, a new Selenium WebDriver instance is initialized.
2. **Page Navigation**: The driver navigates through product pages on the website, opening them in new tabs.
3. **Easter Egg Extraction**: For each product, the script attempts to find and extract Easter egg coupon codes.
4. **Data Storage**: The extracted data is appended to a text file and also stored in memory for display on the web interface.
5. **Cleanup**: After extracting the required number of discounts, the driver is closed.

## Requirements

- Python 3.6 or later
- Flask
- Selenium
- ChromeDriver

To install the required packages, run the following command:


pip install -r requirements.txt
\`\`\`

## Usage

To run the Flask application, use the following command:


python app.py
\`\`\`

Once the application is running, you can navigate to the endpoints described above to interact with the script.

## Dependencies

The application uses the following Python modules:

- \`Flask\`: Web framework for building the web application.
- \`Selenium\`: Automates web browser interaction for extracting data.
- \`os\`, \`time\`: Utility modules for file operations and time management.

## Contributors ✨

<table>
  <tbody>
    <tr>
      <td align="center"><a href="https://hurr13ane.com"><img src="https://avatars.githubusercontent.com/u/76591840?v=4" width="100px;" alt="Jeroen Engels"/><br /><sub><b>Diana-Maria Iercosan</b></sub></a><br />
      </td>
    </tr>
  </tbody>
</table>

## Support
For any questions or support, please contact me via https://hurr13ane.com/contact/

# License
This project is licensed under the MIT License.