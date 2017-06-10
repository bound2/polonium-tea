class Site:
    def __init__(self, web_driver):
        self.web_driver = web_driver

    def setup(self, extras=None):
        raise NotImplementedError('Must be implemented')

    def load_more(self):
        raise NotImplementedError('Must be implemented')

    def scroll_bottom(self):
        self.web_driver.execute_script("window.scrollTo(document.body.scrollTop, document.body.scrollHeight)")


class GoogleImages(Site):

    XPATH_SEARCH_BOX = '//input[@type="text" and @name="q" and @title="Search"]'
    XPATH_SEARCH_BUTTON = '//button[@type="submit" and @value="Search"]'

    def load_more(self):
        pass

    def setup(self, search_term=None, **kwargs):
        if search_term is None:
            raise ValueError('Search term is required for google image scraping')
        search_box = self.web_driver.find_element_by_xpath(GoogleImages.XPATH_SEARCH_BOX)
        search_button = self.web_driver.find_element_by_xpath(GoogleImages.XPATH_SEARCH_BUTTON)

        search_box.send_keys(search_term)
        search_button.click()


class InstagramWeb(Site):

    XPATH_LOAD_MORE_BUTTON = '//*[contains(text(), "Load more")]'

    def load_more(self):
        element = self.web_driver.find_element_by_xpath(InstagramWeb.XPATH_LOAD_MORE_BUTTON)
        element.click()

    def setup(self, **kwargs):
        pass
