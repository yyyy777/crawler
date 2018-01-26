#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import os
import random
import shutil

import time

import requests
from multiprocessing import Process
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import platform

WINDOWS = 'Windows'
MAC_OS = 'Darwin'
LINUX = 'Linux'


def init_chrome_driver(num):
    chrome_options = Options()
    if platform.system() == WINDOWS:
        userdata_path = 'D:\chrome\chromedata{0}'.format(num)
        cache_path = 'D:\chrome\cache{0}'.format(num)
        chrome_options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
        driver_path = 'C:\Program Files (x86)\chromedriver_win32\chromedriver'
        chrome_options.add_argument('user-data-dir=' + userdata_path)
        chrome_options.add_argument('--disk-cache-dir=' + cache_path)
        chrome_options.add_argument('--no-sandbox')
        preferences_file = os.path.join(
            userdata_path, 'Default', 'Preferences')

    elif platform.system() == MAC_OS:
        userdata_path = '/Users/lllll/coding/chrome/chromedata{0}'.format(
            num)
        cache_path = '/Users/lllll/coding/chrome/cache{0}'.format(num)
        chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        driver_path = '/usr/local/bin/chromedriver'
        chrome_options.add_argument('user-data-dir=' + userdata_path)
        chrome_options.add_argument('--disk-cache-dir=' + cache_path)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1200x1000')
        preferences_file = os.path.join(
            userdata_path, 'Default', 'Preferences')
        # selenium_log_file= '/Users/lllll/coding/chrome/logs/selenium.log'

    elif platform.system() == LINUX:
        userdata_path = '/data/oak/chrome/chromedata{0}'.format(num)
        cache_path = '/data/oak/chrome/cache{0}'.format(num)
        chrome_options.binary_location = '/usr/bin/google-chrome'
        driver_path = '/usr/bin/chromedriver'
        chrome_options.add_argument('user-data-dir=' + userdata_path)
        chrome_options.add_argument('--disk-cache-dir=' + cache_path)
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1200x1000')
        preferences_file = os.path.join(
            userdata_path, 'Default', 'Preferences')

    else:
        print('Unknown OS. Exit')
        return None

    # if os.path.exists(preferences_file):
    #     os.remove(preferences_file)

    # driver = webdriver.Chrome(executable_path=driver_path, chrome_options=chrome_options, service_log_path=selenium_log_file, service_args=["--verbose"])
    driver = webdriver.Chrome(
        executable_path=driver_path,
        chrome_options=chrome_options)
    driver.set_page_load_timeout(3 * 60)
    return driver


def download(driver, num):
    try:
        gp_file = "GooglePlayRank_{num}.txt".format(num=num)
        gp_file_tmp = "GooglePlayRankTmp_{num}.txt".format(num=num)
        with open(gp_file) as f_in:
            pkg = f_in.readline().replace('\n', '').strip()
        url = "https://apps.evozi.com/apk-downloader/?id={pkg}"
        _url = url.format(pkg=pkg)
        driver.maximize_window()
        driver.get(_url)
        driver.find_element_by_class_name("btn-lg").click()
        time.sleep(5)
        down_link = driver.find_element_by_class_name("btn-success").get_attribute("href")
        print(down_link)
        apk_stream = requests.get(down_link, stream=True)
        file_name = pkg + '.apk'
        file_path = os.path.join(os.getcwd(), "apk", file_name)
        with open(file_path, 'wb') as f:
            for chunk in apk_stream.iter_content(chunk_size=512):
                if chunk:
                    f.write(chunk)
    except Exception as e:
        print("download:", e)
    finally:
        with open(gp_file) as f_in:
            with open(gp_file_tmp, 'w') as f_tmp:
                for line in f_in.readlines():
                    if pkg not in line:
                        f_tmp.write(line)
        shutil.move(gp_file_tmp, gp_file)
        print("download:", pkg)


def run(num):
    driver = init_chrome_driver(num)
    try:
        if not driver:
            return False
        return download(driver, num)
    except Exception as e:
        print("down error:", e)
    finally:
        if driver:
            driver.quit()


def main(num):
    while True:
        print("start", num)
        run(num)
        time.sleep(1)


if __name__ == "__main__":
    process_num = 4
    for i in range(process_num):
        p = Process(target=main, args=(i,))
        p.start()
