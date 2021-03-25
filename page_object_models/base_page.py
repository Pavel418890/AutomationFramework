from typing import List

from custom_driver.custom_driver import SeleniumDriverWrapper
from selenium.webdriver.remote.webelement import WebElement


class BasePage:
    relative_url: str = None
    
    def __init__(self, driver: SeleniumDriverWrapper, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.url = self.base_url + (self.relative_url or '')
    
    def load(self) -> None:
        self.driver.get(self.url)
    
    def scroll(self, x_axis: int, y_axis: int) -> None:
        self.driver.page_scroll(x_axis, y_axis)

    def scroll_to_element(self, element: WebElement) -> None:
        self.driver.scroll_to_element(element)
        
    def clear_all_input_fields(self) -> None:
        self.driver.clear_input_fields()
        
    def get_all_input_fields(self) -> List[WebElement]:
        return self.driver.get_element_list('input', 'css')


