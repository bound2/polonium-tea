#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from subprocess import call
from time import sleep
import tempfile
import os

class Hexxer:

    image_extensions = ['.png', '.jpg', '.jpeg']
    image_extension_tuple = tuple(image_extensions)

    def __init__(self, chrome_driver):
        self.chrome_driver = chrome_driver

    def create_image_from_cache(self, url, destination_folder = None):
        if destination_folder is not None and os.path.exists(destination_folder) == False:
            os.mkdir(destination_folder)
        self.chrome_driver.get(url)

        url_parts = url.split('/')
        image_name = url_parts.pop()

        file_body_element = self.chrome_driver.find_elements_by_css_selector('pre')[2]
        file_body = file_body_element.text.replace("  ", " ")

        with tempfile.NamedTemporaryFile() as tf:
            tf.write(file_body)
            tf.flush()

            if destination_folder is None:
                call('xxd -r ' + tf.name + ' ' + image_name, shell=True)
            else:
                call('xxd -r ' + tf.name + ' ' + destination_folder + os.sep + image_name, shell=True)

    def get_image_urls_from_cache(self):
        self.chrome_driver.get('chrome://view-http-cache/')
        links = self.chrome_driver.find_elements_by_css_selector('a')
        image_links = set()

        for element in links:
             url = element.get_attribute('href')
             if url.endswith(Hexxer.image_extension_tuple):
                 image_links.add(url)

        return image_links


# driver = webdriver.Chrome()
# hexxer = Hexxer(chrome_driver = driver)
# try:
#     driver.get('https://python.org')
#     driver.execute_script("window.open();")
#     driver.switch_to_window(driver.window_handles[1])
#     image_urls = hexxer.get_image_urls_from_cache()
#     for url in image_urls:
#         hexxer.create_image_from_cache(url, destination_folder = 'test')
#
#     sleep(5.0)
# finally:
#     for handle in driver.window_handles:
#         driver.switch_to_window(handle)
#         driver.close()
