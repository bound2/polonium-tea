#!/usr/bin/env python
import shutil
import os

from argparse import ArgumentParser
from selenium import webdriver
from time import sleep
from glob import glob

from hexxer import Hexxer
from detector import HaarDetector
from scrap import get_proper_site


DOWNLOAD_DIR = 'download'
ACCEPTED_DIR = 'accepted'
DISCARDED_DIR = 'discarded'
CORRUPTED_DIR = "corrupted"


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


def filter_images(detector, image_set):
    for image_path in image_set:
        try:
            if detector is not None:
                object_found = detector.detect(image_path, min_size=(30, 30), max_object_count=1)
                if object_found:
                    shutil.move(image_path, ACCEPTED_DIR)
                else:
                    shutil.move(image_path, DISCARDED_DIR)
            else:
                shutil.move(image_path, ACCEPTED_DIR)
        except Exception as e:
            print "Exception for image: ", image_path
            print "Moving problematic image to corrupted directory"
            shutil.move(image_path, CORRUPTED_DIR)
            pass


if __name__ == "__main__":
    empty_folders()
    create_folders()

    argument_parser = ArgumentParser()
    argument_parser.add_argument('--url', required=True, help='url to scrape images from')
    argument_parser.add_argument('--cascade', help='path to haarcascade which will be used to filter images')
    argument_parser.add_argument('--count', default=6000, help='maximum image download count')
    argument_parser.add_argument('--query', help='search query if applicable')
    args = argument_parser.parse_args()

    url = args.url
    cascade_path = args.cascade
    max_count = args.count
    query = args.query

    driver = webdriver.Chrome()
    target_site = get_proper_site(driver, url)
    hexxer = Hexxer(chrome_driver=driver)
    detector = HaarDetector(cascade_path) if cascade_path is not None else None

    parsed_image_urls = set()

    try:
        driver.get(url)
        target_site.setup(query)
        # Open another tab to load images from cache
        driver.execute_script("window.open();")

        sleep(2.0)
        target_site.scroll_and_try_load()

        while accepted_count() < max_count:
            initial_count = len(parsed_image_urls)
            sleep(2.0)
            target_site.scroll_and_try_load()
            sleep(2.0)

            # switch to second tab to get data from cache
            driver.switch_to.window(driver.window_handles[1])
            intermediate_parsed_urls = hexxer.get_image_urls_from_cache(
                destination_folder=DOWNLOAD_DIR,
                image_links=parsed_image_urls
            )
            parsed_image_urls.update(intermediate_parsed_urls)

            if len(parsed_image_urls) == initial_count:
                print "No more new files. Quitting early"
                break

            # filter the images with haar cascade
            image_set = glob(DOWNLOAD_DIR + os.sep + '*')
            filter_images(detector, image_set)

            # switch back to first tab to continue fetching images
            driver.switch_to.window(driver.window_handles[0])
            print "Accepted files: ", accepted_count(), "/", max_count
            print "Files parsed: ", total_count()
    finally:
        # Close all tabs
        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            driver.close()
