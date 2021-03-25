import json
import os
import pathlib
from dataclasses import dataclass
from typing import Union, Any, Generator

import attr
import pytest
from pytest import Item, Collector
from _pytest._code import ExceptionInfo
from _pytest.reports import CollectReport, TestReport
from _pytest.runner import CallInfo
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest


from custom_driver import SeleniumDriverWrapper, WebDriverFactory
from data_source.data_factories import UserFactory
from page_object_models import PageObjectModels
from utils import ScreenshotTaker

BASE_DIR = pathlib.Path(__file__).parents[1]


@dataclass
class Config:
    base_url: str


def pytest_addoption(parser: Parser) -> None:
    parser.addoption('--browser', help='Type of browser')
    parser.addoption('--headless', action='store_true', help='')


def pytest_exception_interact(
        node: Union[Item, Collector, ExceptionInfo, Any],
        call: CallInfo[Any],
        report: Union[CollectReport, TestReport]
) -> None:
    # при возникновении эксепшионов, в том числе и AssertionError,
    # делаем и сохраняем скриншоты
    screenshot_taker: ScreenshotTaker = node.funcargs.get('screenshot_taker')
    if screenshot_taker:
        exc: Union[attr.ib, ExceptionInfo] = call.excinfo
        truncated_test_name = node.location[-1] if len(node.location[-1]) < 50 \
            else node.location[-1][:50]
        screenshot_taker.take_screenshot(
            test_name=truncated_test_name,
            exception_type=exc.typename
        )


@pytest.fixture(scope='session')
def browser(request: FixtureRequest) -> str:
    return request.config.getoption('--browser')


@pytest.fixture(scope='session')
def is_headless(request: FixtureRequest) -> str:
    return request.config.getoption('--headless')


@pytest.fixture(scope='session')
def driver(
        browser: str, is_headless: bool
) -> Generator[SeleniumDriverWrapper, None, None]:
    wdf = WebDriverFactory(
        browser_type=browser,
        is_headless=is_headless,
        base_dir=BASE_DIR,
        implicit_wait_in_seconds=10
    )
    driver = wdf.get_webdriver_instance()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def config() -> Config:
    path_to_config = os.path.join(BASE_DIR, 'configfiles', 'config.json')
    with open(path_to_config) as config_file:
        return Config(**json.load(config_file))


@pytest.fixture(autouse=True)
def tear_down(driver: SeleniumDriverWrapper) -> Generator[None, None, None]:
    yield
    driver.delete_all_cookies()


@pytest.fixture(scope='class')
def page_models(
        driver: SeleniumDriverWrapper, config: Config, request
) -> PageObjectModels:
    poms = PageObjectModels.get_initialized_instance(
        driver=driver,
        base_url=config.base_url,
    )
    request.cls.page_models = poms
    return poms


@pytest.fixture(autouse=True)
def screenshot_taker(driver: SeleniumDriverWrapper) -> ScreenshotTaker:
    return ScreenshotTaker(driver=driver, base_dir=BASE_DIR)


@pytest.fixture(scope='class')
def user_factory(request, config: Config) -> UserFactory:
    uf = UserFactory(base_url=config.base_url)
    request.cls.user_factory = uf
    return uf
