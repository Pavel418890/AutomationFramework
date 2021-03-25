from dataclasses import dataclass

from custom_driver.custom_driver import SeleniumDriverWrapper
from .login_page import LoginPage
from .registration_page import RegistrationPage
from .home_page import HomePage
from .navigation_bar import NavigationBar


@dataclass
class PageObjectModels:
    login_page: LoginPage = None
    registration_page: RegistrationPage = None
    home_page: HomePage = None
    navigation_bar: NavigationBar = None
    
    @classmethod
    def get_initialized_instance(
        cls, driver: SeleniumDriverWrapper, base_url: str
    ) -> 'PageObjectModels':
        instance = cls()
        instance._set_up(driver, base_url)
        return instance
        
    def _set_up(self, driver: SeleniumDriverWrapper, base_url: str) -> None:
        for page_name, page_model in self.__annotations__.items():
            setattr(self, page_name, page_model(driver, base_url))



