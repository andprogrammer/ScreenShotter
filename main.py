import time
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException

CORONA_VIRUS_URL = 'https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html' \
                   '#/bda7594740fd40299423467b48e9ecf6'
FLIGHT_RADAR_URL = 'https://www.flightradar24.com/33.28,-21.42/3'
CORONA_DECREMENT_BUTTON = 'esriSimpleSliderDecrementButton'
CORONA_VIRUS_DIR = 'corona_virus_shots'
FLIGHT_RADAR_DIR = 'flight_radar_shots'
CORONA_VIRUS_IMAGE = CORONA_VIRUS_DIR + '/corona_virus-{}.png'
FLIGHT_RADAR_IMAGE = FLIGHT_RADAR_DIR + '/flight_radar-{}.png'
FLIGHT_CLOSE_BUTTON = 'btn.btn-blue'
REFRESH_TIME = 8
NEXT_SCREENSHOT_DURATION = 3600


def run():
    create_dir_if_not_exists(CORONA_VIRUS_DIR)
    create_dir_if_not_exists(FLIGHT_RADAR_DIR)
    while True:
        driver = webdriver.Chrome()
        driver.set_window_size(2560, 1440)
        driver.fullscreen_window()
        save_screen_shot(CORONA_VIRUS_URL, driver, CORONA_VIRUS_IMAGE)
        save_screen_shot(FLIGHT_RADAR_URL, driver, FLIGHT_RADAR_IMAGE)
        driver.close()
        time.sleep(NEXT_SCREENSHOT_DURATION)


def create_dir_if_not_exists(directory):
    try:
        Path(directory).mkdir(exist_ok=True)
    except FileNotFoundError:
        print('{} Not possible to create directory {}'.format(get_timestamp(), directory))


def get_timestamp():
    t = time.localtime()
    current_time = time.strftime("%d_%m_%Y-%H_%M_%S", t)
    return current_time


def save_screen_shot(url, driver, image_name):
    driver.get(url)
    driver.refresh()
    time.sleep(REFRESH_TIME)
    if url in CORONA_VIRUS_URL:
        click_button(driver, CORONA_DECREMENT_BUTTON)
    if url in FLIGHT_RADAR_URL:
        click_button(driver, FLIGHT_CLOSE_BUTTON)
    current_image_name = image_name.format(get_timestamp())
    driver.save_screenshot(current_image_name)
    print('{} screenshot {}'.format(get_timestamp(), current_image_name))


def click_button(driver, button_to_click):
    try:
        current_button = driver.find_element_by_class_name(button_to_click)
        current_button.click()
        time.sleep(REFRESH_TIME)
    except (NoSuchElementException, ElementNotInteractableException) as ex:
        print('{} No such {} element found {}'.format(get_timestamp(), button_to_click, ex))


if __name__ == '__main__':
    print('{} Starting screenshotter...'.format(get_timestamp()))
    run()
    print('{} Stopping screenshotter...'.format(get_timestamp()))
