import unittest

import pytest
from ddt import ddt

from page_object_models import LoginPage
from data_source import generate_invalid_login_data, UserFactory


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.usefixtures('page_models', 'user_factory')
@ddt
class LoginTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.login_page: LoginPage = self.page_models.login_page

    def test_invalid_login(self) -> None:
        self.login_page.load()
        self.login_page.login(*generate_invalid_login_data())
        assert self.login_page.login_button.is_displayed()

    def test_valid_login(self) -> None:
        self.login_page.load()
        user: UserFactory.User = self.user_factory.get_new_user()
        self.login_page.login(email=user.email, password=user.password)
        assert self.login_page.user_icon.is_displayed()
        assert self.login_page.user_icon.text == user.full_name
        

