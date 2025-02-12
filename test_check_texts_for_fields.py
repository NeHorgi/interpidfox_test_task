import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Config:
    base_url = "https://www.intrepidfox.tech"
    form_url = "https://www.intrepidfox.tech/blank-2"


class Constants:
    email_field_expected_text = 'Enter an email address like example@mysite.com.'
    message_field_expected_text = 'Enter an answer.'
    check_box_expected_text = 'Check the box to continue.'


consts = Constants()
config = Config()


@pytest.fixture(scope='session')
def chrome_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()


def test_check_texts_for_required_fields(chrome_driver):
    """
    Test checks that all support texts for all required fields in the form of ordering Demo are correct.
    """
    chrome_driver.get(config.base_url)
    demo_button = chrome_driver.find_element(By.XPATH, "//span[@class='w4Vxx6 wixui-button__label']")
    demo_button.click()
    time.sleep(2)

    assert config.base_url in chrome_driver.current_url, "Form was not opened."

    submit_button = chrome_driver.find_element(By.XPATH, "//button[@data-hook='submit-button']")
    submit_button.click()
    time.sleep(3)

    required_email_field_message = chrome_driver.find_element(By.XPATH, "//div[@data-hook='field-error-email']")
    required_email_field_message_text = required_email_field_message.text
    required_message_field_message = chrome_driver.find_element(By.XPATH,
                                                                "//div[@data-hook='field-error-long_answer']")
    required_message_field_message_text = required_message_field_message.text
    required_check_box_field_message = chrome_driver.find_element(By.XPATH,
                                                                  "//div[@data-hook='form-field-form_field_cea7']")
    required_check_box_field_message_text = required_check_box_field_message.text.split('\n')[-1]

    assert (required_email_field_message_text ==
            consts.email_field_expected_text), (f'Wrong text for the email field, expected: '
                                                f'{consts.email_field_expected_text}, '
                                                f'got: {required_email_field_message}')

    assert (required_message_field_message_text ==
            consts.message_field_expected_text), (f'Wrong text for the message field, expected: '
                                                  f'{consts.message_field_expected_text}, '
                                                  f'got: {required_message_field_message_text}')

    assert (required_check_box_field_message_text ==
            consts.check_box_expected_text), (f'Wrong text for the check box, expected: '
                                              f'{consts.check_box_expected_text}, '
                                              f'got: {required_check_box_field_message_text}')
