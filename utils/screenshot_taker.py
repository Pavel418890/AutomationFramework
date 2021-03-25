import os
import uuid
from datetime import datetime

from custom_driver import SeleniumDriverWrapper
from .general_purpose import Singleton


class ScreenshotTaker(metaclass=Singleton):
    extension = 'png'

    def __init__(self, driver: SeleniumDriverWrapper, base_dir: str):
        self.driver = driver
        self.screenshots_dir = os.path.join(base_dir, 'screenshots')
        self._filepath = None

    def take_screenshot(self, test_name: str, exception_type: str) -> None:
        self.driver.save_screenshot(
            self.get_filename(test_name, exception_type)
        )

    def get_filename(self, test_name: str, exception_type: str) -> str:
        filename = '{0}_{1}_{2}.{3}'.format(
            test_name, exception_type, uuid.uuid4(), self.extension
        )
        return os.path.join(self.filepath, filename)

    @property
    def filepath(self) -> str:
        if not self._filepath:
            self.create_screenshots_dir()
            self._filepath = os.path.join(
                self.screenshots_dir,
                datetime.now().strftime('%d-%m-%Y_%H.%M.%S')
            )
            os.mkdir(self._filepath)

        return self._filepath

    def create_screenshots_dir(self) -> None:
        if not os.path.exists(self.screenshots_dir):
            os.mkdir(self.screenshots_dir)
