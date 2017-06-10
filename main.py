#!/usr/bin/env python
from selenium import webdriver
from detector import HaarDetector
from time import sleep
from glob import glob
from hexxer import Hexxer
import shutil
import os

DOWNLOAD_DIR = 'download'
ACCEPTED_DIR = 'accepted'
DISCARDED_DIR = 'discarded'
CORRUPTED_DIR = "corrupted"
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
        shutil.rmtree(CORRUPTED_DIR)
    except Exception as e:
        pass


def create_folders():
    try:
        os.makedirs(DOWNLOAD_DIR)
        os.makedirs(ACCEPTED_DIR)
        os.makedirs(DISCARDED_DIR)
        os.makedirs(CORRUPTED_DIR)
    except Exception as e:
        pass


def apply_haar_cascade(detector, image_set):
    for image_path in image_set:
        try:
            object_found = detector.detect(image_path, min_size=(30, 30), max_object_count=1)
            if object_found == True:
                shutil.move(image_path, ACCEPTED_DIR)
            else:
                shutil.move(image_path, DISCARDED_DIR)
        except Exception as e:
            print "Exception for image: ", image_path
            print "Moving problematic image to corrupted directory"
            shutil.move(image_path, CORRUPTED_DIR)
            pass


if __name__ == "__main__":
    empty_folders()
    create_folders()

    driver = webdriver.Chrome()
    hexxer = Hexxer(chrome_driver=driver)
    detector = HaarDetector("cascades/haarcascade_frontalface_default.xml")

    parsed_image_urls = set()

    try:
        driver.get("https://www.instagram.com/explore/tags/tongue/")
        driver.execute_script("window.open();")
        sleep(2.0)
        # Load more is present the first time to load more
        driver.execute_script("window.scrollTo(document.body.scrollTop, document.body.scrollHeight)")
        element = driver.find_element_by_xpath("//*[contains(text(), 'Load more')]")
        element.click()

        while accepted_count() < DESIRED_FILE_COUNT:
            sleep(2.0)
            driver.execute_script("window.scrollTo(document.body.scrollTop, document.body.scrollHeight)")
            sleep(2.0)

            # switch to second tab to get data from cache
            driver.switch_to_window(driver.window_handles[1])
            image_urls = hexxer.get_image_urls_from_cache()
            for url in image_urls:
                if url not in parsed_image_urls:
                    hexxer.create_image_from_cache(url, destination_folder=DOWNLOAD_DIR)
                    parsed_image_urls.add(url)

            # filter the images with haar cascade
            image_set = glob(DOWNLOAD_DIR + os.sep + '*')
            apply_haar_cascade(detector, image_set)

            # switch back to first tab to continue fetching images
            driver.switch_to_window(driver.window_handles[0])
            print "Accepted files: ", accepted_count(), "/", DESIRED_FILE_COUNT
            print "Files parsed: ", total_count()
    finally:
        # Close all tabs
        for handle in driver.window_handles:
            driver.switch_to_window(handle)
            driver.close()
