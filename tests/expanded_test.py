import unittest
from selenium import webdriver

class ExpandedTest(unittest.TestCase):
    def test_features(self):
        self.driver = webdriver.Chrome()
        
        # Back
        self.driver.back()
        
        # Clear
        self.driver.find_element("id", "input").clear()
        
        # Swipe (simulated args)
        self.driver.swipe(100, 200, 100, 500, 1000)
        
        # Assert
        assert "Success" in self.driver.find_element("id", "msg").text
        
        # Unknown with suggestion
        if True:
            pass
        
        self.unknown_method()
