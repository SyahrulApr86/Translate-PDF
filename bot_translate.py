import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import undetected_chromedriver as uc
import contextlib
import os


def create_download_directory(file_path):
    """Membuat direktori 'Translated' di direktori yang sama dengan file_path."""
    base_dir = os.path.dirname(file_path)
    download_dir = os.path.join(base_dir, "Translated")
    download_dir = os.path.join(download_dir, os.path.splitext(os.path.basename(file_path))[0])

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    return download_dir


def initialize_undetected_chrome(download_dir):
    """Initialize the undetected Chrome webdriver with a specified download directory."""
    options = uc.ChromeOptions()

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    driver = uc.Chrome(options=options)
    return driver


def upload_file(driver, file_path, wait):
    """Click the 'Browse your files' button and upload the specified file."""
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='ucj-19']")))
    input_file = wait.until(EC.presence_of_element_located((By.ID, "ucj-19")))
    input_file.send_keys(file_path)
    print(f"File {file_path} uploaded successfully.")


def click_translate_button(driver, wait):
    """Wait for the 'Translate' button to be clickable and click it."""
    translate_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[jsname='vSSGHe']")))
    translate_button.click()
    wait.until(EC.invisibility_of_element((By.CSS_SELECTOR, "button[jsname='vSSGHe'][disabled]")))
    print("Translation button clicked.")


def download_translation(driver):
    """Wait for the 'Translating...' text to disappear and then click the 'Download translation' button."""
    print("Waiting for the translation to complete...")

    # Wait until the "Translating..." text is no longer present
    while True:
        try:
            # Check if the 'Translating...' element is still visible
            driver.find_element(By.XPATH, "//span[contains(text(), 'Translating...')]")
            time.sleep(1)
        except NoSuchElementException:
            # If the element is no longer found, break from the loop
            break

    # Find and click the download button
    download_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Download translation')]")
    driver.execute_script("arguments[0].click();", download_button)
    print("Download button clicked.")
    time.sleep(2)  # Wait for the file to download


def translate(file_path, driver):
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://translate.google.com/?sl=en&tl=id&op=docs")

        upload_file(driver, file_path, wait)
        click_translate_button(driver, wait)
        download_translation(driver)

    except TimeoutException as e:
        print("An error occurred:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)
    finally:
        print("Exiting the main function.")
        driver = None


if __name__ == "__main__":
    file_path = r"test.pdf"
    download_dir = create_download_directory(file_path)
    driver = initialize_undetected_chrome(download_dir=download_dir)
    translate(file_path, driver)
