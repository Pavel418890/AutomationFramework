from .base_page import BasePage
from custom_driver.custom_element import SeleniumElement as Element


class NavigationBar(BasePage):
    logout_button = Element(locator='input[value="Logout"]', locator_type='css')

