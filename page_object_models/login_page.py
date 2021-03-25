from .base_page import BasePage
from custom_driver.custom_element import SeleniumElement as Element


class LoginPage(BasePage):
    relative_url = '/Identity/Login'
    
    login_field = Element(locator='Login', locator_type='name')
    password_field = Element(locator='Password', locator_type='name')
    email_field = Element(locator='Name', locator_type='name')
    login_button = Element(
        locator='button[class="btn btn-primary"]',
        locator_type='css'
    )
    user_icon = Element(
        locator='/html/body/div[1]/div[2]/form/a/b',
        locator_type='xpath'
    )
    
    def login(self, email: str, password: str) -> None:
        self.email_field.send_keys(email)
        self.password_field.send_keys(password)
        self.login_button.click()
    

