import os
import pytest
from urllib.parse import urljoin
from selenium import webdriver
import django
from django.urls import reverse


django.setup()
APP_ROOT = 'http://localhost:8000/'
driverExes = {
    webdriver.Chrome:   'chromedriver.exe',
    webdriver.Edge:     'msedgedriver.exe',
}

@pytest.mark.parametrize('driverFunc,driverExe', driverExes.items())
def test_navigation_home_login(driverFunc, driverExe):
    driver = driverFunc(executable_path=os.path.join('drivers', driverExe))
    homeUrl = urljoin(APP_ROOT, reverse('home'))
    driver.get(homeUrl)
    driver.find_element_by_link_text('Login').click()
    assert driver.title == 'Studious - Login'
    driver.close()
    driver.quit()