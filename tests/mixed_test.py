import unittest
from selenium import webdriver

class MixedTest(unittest.TestCase):
    def test_mixed_content(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://example.com")
        
        # Convertible
        self.driver.find_element("id", "foo").click()
        
        # Unconvertible
        print("This is a print statement")
        import time
        time.sleep(5)
        
        # Convertible
        self.driver.find_element("id", "bar").send_keys("baz")
