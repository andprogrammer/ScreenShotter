from selenium import webdriver
from pathlib import Path
import time
from datetime import datetime

from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

CORONA_VIRUS_URL = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html' \
                   '#/bda7594740fd40299423467b48e9ecf6'
FLIGHT_RADAR_URL = 'https://www.flightradar24.com/33.28,-21.42/3'
CORONA_DECREMENT_BUTTON = 'esriSimpleSliderDecrementButton'
CORONA_VIRUS_IMAGE = 'corona_virus_shots/corona_virus{}.png'
FLIGHT_RADAR_IMAGE = 'flight_radar_shots/flight_radar{}.png'
CORONA_VIRUS_DIR = 'corona_virus_shots'
FLIGHT_RADAR_DIR = 'flight_radar_shots'
FLIGHT_CLOSE_BUTTON = 'btn.btn-blue'
REFRESH_TIME = 8
SLEEP_TIME_AFTER_CLICKING_THE_BUTTON = 8


def run():
    create_dir_if_not_exists(CORONA_VIRUS_DIR)
    create_dir_if_not_exists(FLIGHT_RADAR_DIR)
    counter = 0
    while True:
        driver = webdriver.Chrome()
        driver.set_window_size(2560, 1440)
        driver.fullscreen_window()
        save_screen_shot(CORONA_VIRUS_URL, counter, driver, CORONA_VIRUS_IMAGE)
        save_screen_shot(FLIGHT_RADAR_URL, counter, driver, FLIGHT_RADAR_IMAGE)
        counter += 1
        driver.close()


def create_dir_if_not_exists(directory):
    try:
        Path(directory).mkdir(exist_ok=True)
    except FileNotFoundError:
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        print('{} Not possible to create directory {}'.format(timestamp, directory))


def save_screen_shot(url, counter, driver, output_dir):
    driver.get(url)
    driver.refresh()
    time.sleep(REFRESH_TIME)
    if url in CORONA_VIRUS_URL:
        click_button(driver, CORONA_DECREMENT_BUTTON, counter)
    if url in FLIGHT_RADAR_URL:
        click_button(driver, FLIGHT_CLOSE_BUTTON, counter)
    driver.save_screenshot(output_dir.format(counter))


def click_button(driver, button_to_click, counter):
    try:
        current_button = driver.find_element_by_class_name(button_to_click)
        current_button.click()
        time.sleep(SLEEP_TIME_AFTER_CLICKING_THE_BUTTON)
    except (NoSuchElementException, ElementNotInteractableException) as ex:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('{} No such {} element found [counter={}], {}'.format(current_time, button_to_click, counter, ex))


if __name__ == '__main__':
    run()
