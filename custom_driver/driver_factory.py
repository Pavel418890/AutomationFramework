import os
from pathlib import Path
from typing import NamedTuple, Union

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from msedge.selenium_tools import Edge
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from msedge.selenium_tools import EdgeOptions

from .custom_driver import SeleniumDriverWrapper


DriverOptionsType = Union[
    ChromeOptions,
    FirefoxOptions,
    OperaOptions,
    EdgeOptions
]


class WebDriverFactory:
    """
    Фабрика, которая оборачивает стандартный селениум драйвер
    в кастомный класс и возвращает его для дальнейшего использования.

    Тип стандартного драйвера определяется посредством
    аргумента командной строки.

    По дефолту использует драйвера, расположенные в папке driver_executables.
    Если по какой-то причине драйвер не может быть найден внутри проекта,
    то поиск драйвера происходит через системные переменные пути.
    """

    DriverConfig = NamedTuple(
        'DriverConfig',
        [('driver_class', type),
         ('options', DriverOptionsType),
         ('driver_executable', str)]
    )

    default_driver = DriverConfig(
        webdriver.Chrome, ChromeOptions(), 'chromedriver.exe'
    )
    browser_to_driver_config_mapping = {
        'Chrome': DriverConfig(
            webdriver.Chrome, ChromeOptions(), 'chromedriver.exe'
        ),
        'Firefox':  DriverConfig(
            webdriver.Firefox, FirefoxOptions(), 'geckodriver.exe'
        ),
        'Opera': DriverConfig(
            webdriver.Opera, OperaOptions(), 'operadriver.exe'
        ),
        'Edge': DriverConfig(
            Edge, EdgeOptions(), 'MicrosoftWebDriver.exe'
        )
    }
    
    def __init__(
            self, browser_type: str, is_headless: bool, base_dir: str,
            implicit_wait_in_seconds: int, maximize_window: bool = True
    ):
        self.browser_type = browser_type
        self.is_headless = is_headless
        self.webdrivers_dir = os.path.join(base_dir, 'driver_executables')
        self.implicit_wait_in_seconds = implicit_wait_in_seconds
        self.maximize_window = maximize_window
        
    def get_webdriver_instance(self) -> SeleniumDriverWrapper:
        self._configure_driver_options(self.driver_config.options)
        driver = self.driver_config.driver_class(
            executable_path=self.executable_path,
            options=self.driver_config.options
        )
        self._configure_driver(driver)
        return SeleniumDriverWrapper(driver)
    
    def _configure_driver(self, driver: WebDriver) -> None:
        driver.implicitly_wait(self.implicit_wait_in_seconds)
        if self.maximize_window:
            driver.maximize_window()

    def _configure_driver_options(
            self, driver_options: DriverOptionsType
    ) -> None:
        if self.is_headless:
            driver_options.use_chromium = True  # для Edge
            driver_options.add_argument('--headless')

    @property
    def driver_config(self) -> DriverConfig:
        return self.browser_to_driver_config_mapping.get(
            self.browser_type, self.default_driver
        )

    @property
    def executable_path(self) -> str:
        local_path = os.path.join(
            self.webdrivers_dir, self.driver_config.driver_executable
        )
        return local_path if Path(local_path).is_file() \
            else self.driver_config.driver_executable
    


    

