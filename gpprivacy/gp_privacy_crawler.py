#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import platform
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

WINDOWS = 'Windows'
MAC_OS = 'Darwin'
LINUX = 'Linux'


def _init_chrome_driver(num):
    chrome_options = Options()
    if platform.system() == WINDOWS:
        userdata_path = 'D:\chrome\chromedata{0}'.format(num)
        cache_path = 'D:\chrome\cache{0}'.format(num)
        chrome_options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        driver_path = 'C:\Program Files (x86)\chromedriver_win32\chromedriver'
        chrome_options.add_argument('user-data-dir=' + userdata_path)
        chrome_options.add_argument('--disk-cache-dir=' + cache_path)
        preferences_file = os.path.join(
            userdata_path, 'Default', 'Preferences')

    elif platform.system() == MAC_OS:
        userdata_path = '/Users/lllll/coding/chrome/chromedata{0}'.format(num)
        cache_path = '/Users/lllll/coding/chrome/cache{0}'.format(num)
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        driver_path = '/usr/local/bin/chromedriver'
        chrome_options.add_argument('user-data-dir=' + userdata_path)
        chrome_options.add_argument('--disk-cache-dir=' + cache_path)
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--start-maximized')
        # chrome_options.add_argument('--window-size=1200x1000')
        preferences_file = os.path.join(
            userdata_path, 'Default', 'Preferences')
        #selenium_log_file= '/Users/lllll/coding/chrome/logs/selenium.log'

    elif platform.system() == LINUX:
        userdata_path = '/data/oak/chrome/chromedata{0}'.format(num)
        cache_path = '/data/oak/chrome/cache{0}'.format(num)
        chrome_options.binary_location = '/usr/bin/google-chrome'
        driver_path = '/usr/bin/chromedriver'
        chrome_options.add_argument('user-data-dir=' + userdata_path)
        chrome_options.add_argument('--disk-cache-dir=' + cache_path)
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        # chrome_options.add_argument('--window-size=1200x1000')
        preferences_file = os.path.join(
            userdata_path, 'Default', 'Preferences')

    else:
        print('Unknown OS. Exit')
        return None

    drop_content = ['cookies', 'Cookies-journal']

    if os.path.exists(preferences_file):
        os.remove(preferences_file)

    for content in drop_content:
        cookie_path = os.path.join(userdata_path, 'Default', content)
        if os.path.exists(cookie_path):
            os.remove(cookie_path)

    # if os.path.exists(cache_path):
    #     shutil.rmtree(cache_path)
    #     os.mkdir(cache_path)

    # driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options, service_log_path=selenium_log_file, service_args=["--verbose"])
    driver = webdriver.Chrome(
        executable_path=driver_path,
        chrome_options=chrome_options)
    driver.set_page_load_timeout(3 * 60)
    # driver.delete_all_cookies()
    return driver


def get_privacy(driver, package_name):
    try:
        url = "https://play.google.com/store/apps/details?id={0}".format(package_name)
        driver.get(url)
        driver.maximize_window()
        driver.find_element_by_link_text("查看详情").click()
        tmp = (By.CLASS_NAME, "fnLizd")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(tmp))
        page_source = driver.find_element_by_class_name("fnLizd").get_attribute("innerHTML")
        print(page_source)
        if "SMS" in page_source or "短信" in page_source:
            print("找到含有SMS权限的APP: {0}".format(package_name))
            with open("privacy_with_sms.txt", "a+") as f:
                f.write(package_name + "\n")
            return package_name
        return False
    except Exception as e:
        print(e)
        return False


def main():
    try:
        with open("GooglePlayRank2.txt") as f:
            lines = f.readlines()
        for line in lines:
            driver = _init_chrome_driver(0)
            get_privacy(driver, line.strip())
            driver.quit()
    except Exception as e:
        print(e)
    finally:
        try:
            driver.quit()
        except UnboundLocalError:
            pass


if __name__ == "__main__":
    print("start")
    # driver = _init_chrome_driver(0)
    # pack = get_privacy(driver, "com.halfbrick.fruitninjafree")
    # driver.quit()
    # pack = get_privacy(driver, "com.magnet.torrent.cat")
    main()
    print("done")
