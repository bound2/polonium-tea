#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from detector import Cv2HumanDetector
from time import sleep
import wget
import shutil
import os

DOWNLOAD_DIR = 'download'
ACCEPTED_DIR = 'accepted'
DISCARDED_DIR = 'discarded'
DESIRED_FILE_COUNT = 6000

def accepted_count():
    return len(os.listdir(ACCEPTED_DIR))

def discarded_count():
    return len(os.listdir(DISCARDED_DIR))

def total_count():
    return accepted_count() + discarded_count()

def empty_folders():
    try:
        shutil.rmtree(DOWNLOAD_DIR)
        shutil.rmtree(ACCEPTED_DIR)
        shutil.rmtree(DISCARDED_DIR)
    except Exception as e:
        pass

def create_folders():
    try:
        os.makedirs(DOWNLOAD_DIR)
        os.makedirs(ACCEPTED_DIR)
        os.makedirs(DISCARDED_DIR)
    except Exception as e:
        pass

def parse_images(driver):
    network_entries = driver.execute_script("return window.performance.getEntries();")
    driver.execute_script("return window.performance.clearResourceTimings();")
    image_set = set()
    for entry_dict in network_entries:
        if entry_dict.get('initiatorType') == 'img':
            image_url = entry_dict.get('name')
            file_name = wget.download(image_url, out = DOWNLOAD_DIR)
            image_set.add(file_name)

    for image_path in image_set:
        is_human = detector.is_potentially_human(image_path, 1)
        if is_human == True:
            shutil.move(image_path, ACCEPTED_DIR)
        else:
            shutil.move(image_path, DISCARDED_DIR)

if __name__ == "__main__":
    empty_folders()
    create_folders()
    driver = webdriver.Chrome()
    detector = Cv2HumanDetector()
    try:
        driver.get("https://www.instagram.com/explore/tags/tongue/")
        parse_images(driver = driver)

        # Load more is present the first time to load more
        driver.find_element_by_xpath("//*[contains(text(), 'Load more')]").click()

        while accepted_count() < DESIRED_FILE_COUNT:
            sleep(1.0)
            driver.execute_script("window.scrollTo(document.body.scrollTop, document.body.scrollHeight)")
            parse_images(driver = driver)
            print "Accepted files: ", accepted_count(), "/", DESIRED_FILE_COUNT
            print "Files parsed: ", total_count()
    finally:
        driver.close()
