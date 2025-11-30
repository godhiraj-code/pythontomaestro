import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_login_success(self):
        self.driver.get("https://example.com/login")
        
        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys("myuser")
        
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("mypassword")
        
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        welcome_msg = self.driver.find_element(By.CLASS_NAME, "welcome")
        assert "Welcome" in welcome_msg.text

    def tearDown(self):
        self.driver.quit()
