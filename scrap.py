class Scrappable:
    def __init__(self, chrome_driver):
        self.chrome_driver = chrome_driver

    def setup(self, query):
        raise NotImplementedError('Must be implemented')

    def load_more(self):
        raise NotImplementedError('Must be implemented')

    def scroll_bottom(self):
        self.chrome_driver.execute_script("window.scrollTo(document.body.scrollTop, document.body.scrollHeight)")

    def scroll_and_try_load(self):
        self.scroll_bottom()
        try:
            self.load_more()
        except:
            pass


class GoogleImages(Scrappable):
    XPATH_SEARCH_BOX = '//input[@type="text" and @name="q" and @title="Search"]'
    XPATH_SEARCH_BUTTON = '//button[@type="submit" and @value="Search"]'
    XPATH_LOAD_MORE_BUTTON = '//input[@type="button" and @value="Show more results"]'

    def load_more(self):
        element = self.chrome_driver.find_element_by_xpath(GoogleImages.XPATH_LOAD_MORE_BUTTON)
        element.click()

    def setup(self, query):
        if query is None:
            raise ValueError('Search term is required for google image scraping')
        search_box = self.chrome_driver.find_element_by_xpath(GoogleImages.XPATH_SEARCH_BOX)
        search_button = self.chrome_driver.find_element_by_xpath(GoogleImages.XPATH_SEARCH_BUTTON)

        search_box.send_keys(query)
        search_button.click()


class InstagramWeb(Scrappable):
    XPATH_LOAD_MORE_BUTTON = '//*[contains(text(), "Load more")]'

    def load_more(self):
        element = self.chrome_driver.find_element_by_xpath(InstagramWeb.XPATH_LOAD_MORE_BUTTON)
        element.click()

    def setup(self, query):
        pass


def get_proper_site(chrome_driver, url):
    if 'images.google.com' in url:
        return GoogleImages(chrome_driver)
    elif 'instagram.com' in url:
        return InstagramWeb(chrome_driver)
    else:
        raise ValueError('No site parser for: %s' % url)
