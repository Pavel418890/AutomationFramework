from .base_page import BasePage
from custom_driver.custom_element import SeleniumElement as Element


class RegistrationPage(BasePage):
    relative_url = '/Identity/Register'
    
    first_name_field = Element(locator='FirstName', locator_type='id')
    last_name_field = Element(locator='LastName', locator_type='id')
    country_field = Element(locator='Country', locator_type='id')
    city_field = Element(locator='City', locator_type='id')
    street_field = Element(locator='Street', locator_type='id')
    house_field = Element(locator='House', locator_type='id')
    index_field = Element(locator='Index', locator_type='id')
    email_field = Element(locator='Email', locator_type='id')
    password_field = Element(locator='Password', locator_type='id')
    register_button = Element(locator='btn-primary', locator_type='class')
    logout_button = Element(locator='input[value="Logout"]', locator_type='css')
    password_confirmation_field = Element(
        locator='PasswordConfirm',
        locator_type='id'
    )

    def register(
        self, first_name: str, last_name: str, country: str,
        city: str, street: str, house: str, index: str,
        email: str, password: str, password_confirm: str
    ) -> None:
        self.first_name_field.send_keys(first_name)
        self.last_name_field.send_keys(last_name)
        self.country_field.send_keys(country)
        self.city_field.send_keys(city)
        self.street_field.send_keys(street)
        self.house_field.send_keys(house)
        self.index_field.send_keys(index)
        self.email_field.send_keys(email)
        self.password_field.send_keys(password)
        self.password_confirmation_field.send_keys(password_confirm)
        self.scroll_to_element(self.register_button)
        self.register_button.click()


   


