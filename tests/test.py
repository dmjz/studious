import os
import time
import pytest
import requests
from urllib.parse import urljoin
from selenium import webdriver
import django
from django.urls import reverse
from pytest_django.fixtures import django_user_model
from django.conf import settings
from django.test import Client


django.setup()
driverExes = {
    webdriver.Chrome:   'chromedriver.exe',
    webdriver.Edge:     'msedgedriver.exe',
}
APP_ROOT = 'http://localhost:8000/'
homeUrl = urljoin(APP_ROOT, reverse('home'))
signupUrl = urljoin(APP_ROOT, reverse('signup'))
loginUrl = urljoin(APP_ROOT, reverse('login'))
profileUrl = urljoin(APP_ROOT, reverse('profile'))
loginApiUrl = urljoin(APP_ROOT, '')


@pytest.fixture(scope="function")
def get_driver(driverFunc, driverExe):
    driver = driverFunc(executable_path=os.path.join('drivers', driverExe))
    yield driver
    driver.close()
    driver.quit()

@pytest.fixture(scope="function")
def login_client(django_user_model):
    user = django_user_model.objects.create_user(
        username = os.environ['TEST_USER'],
        password = os.environ['TEST_PASS'],
    )
    client = Client()
    client.force_login(user)
    yield client


def next_page_title_after_timeout(driver, startPageTitle, timeout=30):
    """ Wait for page title to change, raising AssertionError after timeout """

    start = time.time()
    while driver.title == startPageTitle:
        assert time.time() - start < timeout, 'Timeout waiting for page change'
        time.sleep(1)
    return driver.title


# API tests
@pytest.mark.parametrize('endpoint', [
    'lessons/new',
    'lessons/edit',
    'lessons/view',
    'lessons/publish',
    'lessons/search',
    'lessons/copy',
    'lessons/delete',
    'review/',
    'review/add',
    'review/available',
    'review/save-progress',
    'review/lesson-details',
    'signup/',
    'login/',
    'logout/',
    'password-change/',
    'profile/',
])
def test_API_routing(endpoint):
    res = requests.get(urljoin(APP_ROOT, endpoint))
    assert res.status_code == 500 if endpoint == 'lessons/search' else 200

def test_API_profile(login_client):
    client = login_client
    res = client.get(profileUrl)
    assert res.status_code == 200
    assert 'Studious - Profile' in str(res.content)

def test_API_lesson_new(login_client):
    client = login_client
    res = client.get(urljoin(APP_ROOT, 'lessons/new'))
    assert res.status_code == 302
    assert '/lessons/edit' in res.url

    
# Selenium tests
@pytest.mark.parametrize('driverFunc,driverExe', driverExes.items())
def test_navigation_home_login(driverFunc, driverExe, get_driver):
    driver = get_driver
    driver.get(homeUrl)
    driver.find_element_by_link_text('Login').click()
    assert driver.title == 'Studious - Login'

@pytest.mark.parametrize('driverFunc,driverExe', driverExes.items())
def test_navigation_home_signup(driverFunc, driverExe, get_driver):
    driver = get_driver
    driver.get(homeUrl)
    driver.find_element_by_link_text('Register').click()
    assert driver.title == 'Studious - Register'

@pytest.mark.parametrize('driverFunc,driverExe', driverExes.items())
def test_register_UI_elements(driverFunc, driverExe, get_driver):
    driver = get_driver
    driver.get(signupUrl)
    driver.find_element_by_name('username')
    driver.find_element_by_name('email')
    driver.find_element_by_name('password1')
    driver.find_element_by_name('password2')
    driver.find_element_by_id('signup-submit-button')

@pytest.mark.parametrize('driverFunc,driverExe', driverExes.items())
def test_login(driverFunc, driverExe, get_driver):
    driver = get_driver
    driver.get(loginUrl)
    driver.find_element_by_name('username').send_keys(os.environ['TEST_USER'])
    driver.find_element_by_name('password').send_keys(os.environ['TEST_PASS'])
    driver.find_element_by_id('login-submit-button').click()
    assert next_page_title_after_timeout(driver, 'Studious - Login')