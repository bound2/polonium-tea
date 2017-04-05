#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from detector import Cv2HumanDetector
import wget

DONWLOAD_DIR = 'download'
ACCEPTED_DIR = 'accepted'
DISCARDED_DIR = 'discarded'

if __name__ == "__main__":
    driver = webdriver.Chrome()
    detector = Cv2HumanDetector()
    try:
        driver.get("https://www.instagram.com/explore/tags/tongue/")
        network_entries = driver.execute_script("return window.performance.getEntries();")
        image_set = set()
        for entry_dict in network_entries:
            if entry_dict.get('initiatorType') == 'img':
                image_url = entry_dict.get('name')
                file_name = wget.download(image_url, out = DONWLOAD_DIR)
                image_set.add(file_name)

        #for image in image_set:


        # Download all and check with openCV if human
        # Then clear entries from driver and scroll further

        #sleep(250)
        #driver.execute_script("window.scrollTo(document.body.scrollTop, document.body.scrollHeight)")
    finally:
        driver.close()
