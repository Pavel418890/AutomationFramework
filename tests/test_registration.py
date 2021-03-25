import os
import unittest

import pytest
from ddt import ddt, data, unpack

from page_object_models import RegistrationPage, NavigationBar
from data_source import generate_valid_registration_data
from utils import load_csv_data_as_nested_list
from tests.conftest import BASE_DIR


@pytest.mark.smoke
@pytest.mark.registration
@pytest.mark.usefixtures('page_models')
@ddt
class RegistrationTest(unittest.TestCase):
    invalid_input_class_name = 'input-validation-error'
    csv_data_path = os.path.join(
        BASE_DIR, 'data_source', 'files', 'registration_data.csv'
    )

    def setUp(self):
        self.registration_page: RegistrationPage = \
            self.page_models.registration_page
        self.navigation_bar: NavigationBar = self.page_models.navigation_bar

    def test_valid_registration(self):
        self.registration_page.load()
        self.registration_page.register(*generate_valid_registration_data())
        assert self.navigation_bar.logout_button.is_displayed()

    @data(*load_csv_data_as_nested_list(csv_data_path))
    @unpack
    def test_invalid_registration(
            self, first_name: str, last_name: str, country: str,
            city: str, street: str, house: str, index: str, email: str,
            password: str, password_confirm: str
    ):
        self.registration_page.load()
        self.registration_page.register(
            first_name=first_name, last_name=last_name, country=country,
            city=city, street=street, house=house, index=index, email=email,
            password=password, password_confirm=password_confirm
        )
        assert self.registration_page.register_button.is_displayed()
