from typing import List, Optional, Any

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement


class SeleniumDriverWrapper:
    """
    Кастомный селениум драйвер,
    который дополняет ф-ционал стандартного селениум драйвера.

    Использует скрытое делигирование через __getattr__ вместо наследования,
    так как тип селениум драйвера (chrome, firefox и т.д.)
    определяется в рантайме через аргумент командной строки.
    """

    default_locator_type = By.CSS_SELECTOR
    locator_type_constants_mapping = {
       'id': By.ID,
       'name': By.NAME,
       'class': By.CLASS_NAME,
       'css': By.CSS_SELECTOR,
       'xpath': By.XPATH,
       'text': By.PARTIAL_LINK_TEXT,
    }

    def __init__(self, driver: WebDriver):
        self.original_driver = driver
    
    def __getattr__(self, name: str) -> Any:
        # ипользуем скрытое делигирование,
        # которое позволяет нам обращаться к аттрибутам и методам
        # стандартного селениум драйвера напрямую через наш кастомный класс
        return getattr(self.original_driver, name)

    def get_locator_type(self, locator_type: str) -> str:
        return self.locator_type_constants_mapping.get(
            locator_type.lower(), self.default_locator_type
        )

    def get_element(
            self, locator: str, locator_type: Optional[str] = None
    ) -> WebElement:
        return self.find_element(
            self.get_locator_type(locator_type),
            locator
        )

    def get_element_list(
            self, locator: str, locator_type: Optional[str] = None
    ) -> List[WebElement]:
        return self.find_elements(
            self.get_locator_type(locator_type), locator
        )

    def get_element_attribute(
            self, attribute: str, locator: str,
            locator_type: Optional[str] = None
    ) -> str:
        return self.get_element(locator, locator_type).get_attribute(attribute)

    def get_input_value(
            self, locator: str, locator_type: Optional[str] = None
    ) -> str:
        return self.get_element_attribute('value', locator, locator_type)

    def is_element_present(
            self, locator: str, locator_type: Optional[str] = None
    ) -> bool:
        is_present = True
        try:
            self.get_element(locator, locator_type)
        except NoSuchElementException:
            is_present = False

        return is_present

    def page_scroll(self, x_axis: int, y_axis: int) -> None:
        self.execute_script(
            'window.scrollBy(arguments[0], arguments[1])', x_axis, y_axis
        )

    def scroll_to_element(self, element: WebElement) -> dict:
        return element.location_once_scrolled_into_view
    
    def clear_input_fields(self) -> None:
        for element in self.get_element_list(
            locator='input', locator_type='css'
        ):
            element.clear()
    

