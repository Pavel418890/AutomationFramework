from dataclasses import dataclass
from typing import Tuple

import requests
from bs4 import BeautifulSoup

from utils import generate_random_string, generate_random_email


class UserFactory:
    """
    Фабрика, которая производит новых валидных юзеров
    (регистрирует через http запросы)
    """

    registration_url = '/Identity/Register'
    csrf_cookie_name = '.AspNetCore.Antiforgery.w5W7x28NAIs'
    registration_token_name = '__RequestVerificationToken'
    
    @dataclass
    class User:
        first_name: str
        last_name: str
        email: str
        password: str
        
        @property
        def full_name(self) -> str:
            return f'{self.first_name} {self.last_name}'
    
    def __init__(self, base_url: str):
        self.url = base_url + self.registration_url
    
    def get_new_user(self) -> User:
        csrf_cookie, registration_token = self.tokens
        user_data = self.user_data
        requests.post(
            url=self.url,
            data={**user_data, self.registration_token_name: registration_token},
            cookies={self.csrf_cookie_name: csrf_cookie}
        )
        return self.User(
            first_name=user_data['FirstName'],
            last_name=user_data['LastName'],
            email=user_data['Email'],
            password=user_data['Password'],
        )
    
    @property
    def tokens(self) -> Tuple[str, ...]:
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        registration_token = \
            soup.find(attrs={'name': self.registration_token_name}).attrs['value']
        csrf_cookie = dict(res.cookies.items())[self.csrf_cookie_name]
        return csrf_cookie, registration_token
    
    @property
    def user_data(self) -> dict:
        return {
            'FirstName': 'Test',
            'LastName': 'User',
            'Email': generate_random_email(
                local_length=5, domain_length=6,
                char_type_local='letters', char_type_domain='letters'
            ),
            'Password': '12345678',
            'PasswordConfirm': '12345678',
        }


def generate_valid_registration_data() -> list:
    return [
        *[generate_random_string(6, 'letters') for _ in range(6)],
        generate_random_string(6, 'digits'),
        generate_random_email(6, 8, 'mix', 'mix'),
        *[*[generate_random_string(8, 'mix')] * 2]
    ]


def generate_invalid_login_data() -> Tuple[str, ...]:
    return (
        generate_random_email(6, 8, 'mix', 'mix'),
        generate_random_string(6, 'letters')
    )

