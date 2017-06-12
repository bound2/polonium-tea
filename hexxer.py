#!/usr/bin/env python
from subprocess import call
import tempfile
import os
import uuid


class Hexxer:
    def __init__(self, chrome_driver):
        self.chrome_driver = chrome_driver

    def create_image_from_cache(self, file_name, destination_folder=None):
        if destination_folder is not None and os.path.exists(destination_folder) == False:
            os.mkdir(destination_folder)

        file_body_element = self.chrome_driver.find_elements_by_css_selector('pre')[2]
        file_body = file_body_element.text.replace("  ", " ")

        with tempfile.NamedTemporaryFile() as tf:
            tf.write(file_body)
            tf.flush()

            if destination_folder is None:
                call('xxd -r ' + tf.name + ' ' + file_name, shell=True)
            else:
                call('xxd -r ' + tf.name + ' ' + destination_folder + os.sep + file_name, shell=True)

    def get_image_urls_from_cache(self, destination_folder, index=0, image_links=set(), reload_page=True):
        try:
            # prevent empty reload on already parsed image
            if reload_page:
                self.chrome_driver.get('chrome://view-http-cache/')

            element = self.chrome_driver.find_elements_by_css_selector('a')[index]
            url = element.get_attribute('href')
            duplicate = url in image_links

            if not duplicate:
                self.chrome_driver.get(url)
                try:
                    # determine whether it is image at all
                    header_element = self.chrome_driver.find_elements_by_css_selector('pre')[0]
                    file_extension = None
                    if 'content-type: image/jpeg' in header_element.text:
                        file_extension = '.jpg'
                    elif 'content-type: image/png' in header_element.text:
                        file_extension = '.png'

                    if file_extension is not None:
                        file_name = str(uuid.uuid4()) + file_extension
                        self.create_image_from_cache(
                            file_name=file_name,
                            destination_folder=destination_folder
                        )
                        image_links.add(url)

                except Exception as e:
                    print e.message
            return self.get_image_urls_from_cache(
                destination_folder=destination_folder,
                index=index + 1,
                image_links=image_links,
                reload_page=not duplicate
            )
        except IndexError as ie:
            return image_links
