from __future__ import annotations

from typing import Union

from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException

from page_object_models.base_page import BasePage


class ElementNotFoundException(Exception):
    """
    Кастомный эксепшион,
    который заменяет selenium NoSuchElementException
    """


class SeleniumElement:
    """
    Non-data дескриптор для page object моделей,
    который на этапе инициализации принимает значение локатора
    и по какому методу его искать.

    При обращении через инстанц page object модели ищет и возвращает элемент
    при помощи драйвера, который присутсвует в каждом инстанце page object
    модели данного проекта.

    Если элемент не может быть найден, ловит selenium ElementNotFoundException
    и мьютит весь предыдущий стэк трэйс, после чего рэйзит кастомный эксепшион
    с информацией о ненайденном элементе.
    """
    not_found_message = 'Unable to locate element {0} using {1} method'
    
    def __init__(self, locator: str, locator_type: str):
        self.locator = locator
        self.locator_type = locator_type
    
    def __get__(
        self, instance: BasePage, owner_class: type
    ) -> Union[WebElement, SeleniumElement]:
        if instance is None:
            return self
        try:
            return instance.driver.get_element(self.locator, self.locator_type)
        except NoSuchElementException:
            # мьютим предыдущий стэк трэйс и рэйзим кастомный эксепшион
            raise ElementNotFoundException(
                self.not_found_message.format(self.locator, self.locator_type)
            ) from None
