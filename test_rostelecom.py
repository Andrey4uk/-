import pytest
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://b2c.passport.rt.ru/account_b2c/page'
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(10)

class element_has_css_class(object):
    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False

@pytest.fixture(autouse=True)
def driver():
    service = ChromeService(executable_path=ChromeDriverManager().install())
    pytest.driver = webdriver.Chrome(service=service)
    pytest.driver.maximize_window()
    pytest.driver.get(url)
    yield
    pytest.driver.quit()

def test_first():
    pytest.driver = webdriver.Chrome('C:/Users/andre/Downloads/chromedriver.exe')
    pytest.driver.get(url)
    yield
    pytest.driver.quit()

def test_successful_tab():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-phone')))
    assert pytest.driver.find_element(By.ID, 't-btn-tab-phone').text != 'Номер'
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    assert pytest.driver.find_element(By.ID, 't-btn-tab-mail').text == 'Почта'
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-login')))
    assert pytest.driver.find_element(By.ID, 't-btn-tab-login').text == 'Логин'
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-ls')))
    assert pytest.driver.find_element(By.ID, 't-btn-tab-ls').text == 'Лицевой счёт'

#Номер телефона

#Корректный ввод номера
def test_successful_authorization_by_phone():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('9159777726')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'user-name__first-patronymic').text == "Андрей"

#Некорректный ввод номера
def test_unsuccessful_unregistered_number():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89159777727')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Некорректный пароль
def test_incorrect_password_by_phone():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89159777726')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('sdd323rh')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Проверка успешной авторизации без кода страны
def test_successful_authorization_by_phone_without_code():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('9159777726')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'user-name__first-patronymic').text == "Андрей"
#Буквы вместо номера телефона
def test_unsuccessful_entering_letters_by_phone():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('dsgesgejd')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Почта

#Корректный ввод почты
def test_successful_authorization_by_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('andrey92russ@mail.ru')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'user-name__first-patronymic').text == "Андрей"

#Некорректный ввод почты
def test_unsuccessful_authorization_by_invalid_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('andreyka92russ@mail.ru')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Почта без домена
def test_unsuccessful_by_incorrect_email_without_code():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('andrey92ruu@mail')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Почта без @
def test_unsuccessful_by_incorrect_email_without_server_address():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('andrey92russ.ru')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Некорректный пароль
def test_incorrect_password_by_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-mail').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('andrey92russ@mail.ru')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('dfepov12j')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Лицевой счет

#Корректный лицевой счет
def test_successful_authorization_by_login():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('rtkid_1697549778905')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.CLASS_NAME, 'user-name__first-patronymic').text == "Андрей"

#Некорректный личевой счет
def test_unsuccessful_authorization_by_invalid_login():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('rrtkid_1697549778905')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Некорректный пароль
def test_incorrect_password_by_login():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-mail')))
    pytest.driver.find_element(By.ID, 't-btn-tab-login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('rtkid_1697549778905')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('dkjdfe4fd')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Успешный тест некорректного ЛС
def test_successful_authorization_by_invalid_ls():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-ls')))
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('069754977890')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('fdbdlkn32kl')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#Некорректный пароль ЛС
def test_incorrect_password_by_ls():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 't-btn-tab-ls')))
    pytest.driver.find_element(By.ID, 't-btn-tab-ls').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('1697549778905')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('dfsdfl32l')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    assert pytest.driver.find_element(By.ID, 'form-error-message').text == 'Неверный логин или пароль'

#По временному коду
def test_authorization_by_code_with_phone():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89159777726')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'lk-btn')))
    pytest.driver.find_element(By.ID, 'lk-btn').click()
    element = WebDriverWait(pytest.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'iqOiiv')))
    pytest.driver.find_element(By.CLASS_NAME, 'iqOiiv').click()

    element = WebDriverWait(pytest.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span')))
    pytest.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'address')))
    pytest.driver.find_element(By.ID, 'address').send_keys('89159777726')
    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'otp_get_code')))
    pytest.driver.find_element(By.ID, 'otp_get_code').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == 'Код подтверждения отправлен'

def test_authorization_by_code_change_number():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89159777726')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'lk-btn')))
    pytest.driver.find_element(By.ID, 'lk-btn').click()
    element = WebDriverWait(pytest.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'iqOiiv')))
    pytest.driver.find_element(By.CLASS_NAME, 'iqOiiv').click()

    element = WebDriverWait(pytest.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span')))
    pytest.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'address')))
    pytest.driver.find_element(By.ID, 'address').send_keys('89159777726')
    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'otp_get_code')))
    pytest.driver.find_element(By.ID, 'otp_get_code').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'otp-code-form__back-btn')))
    pytest.driver.find_element(By.CLASS_NAME, 'otp-code-form__back-btn').click()

#По коду на почту
def test_authorization_by_code_with_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89159777726')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'lk-btn')))
    pytest.driver.find_element(By.ID, 'lk-btn').click()
    element = WebDriverWait(pytest.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'iqOiiv')))
    pytest.driver.find_element(By.CLASS_NAME, 'iqOiiv').click()

    element = WebDriverWait(pytest.driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span')))
    pytest.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'address')))
    pytest.driver.find_element(By.ID, 'address').send_keys('andrey92russ@mail.ru')
    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'otp_get_code')))
    pytest.driver.find_element(By.ID, 'otp_get_code').click()
    assert pytest.driver.find_element(By.TAG_NAME, 'h1').text == 'Код подтверждения отправлен'
#Изменение почты
def test_authorization_by_code_change_email():
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
    pytest.driver.find_element(By.ID, 'username').send_keys('89159777726')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
    pytest.driver.find_element(By.ID, 'password').send_keys('240792Ab')
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    pytest.driver.find_element(By.NAME, 'login').click()
    element = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, 'lk-btn')))
    pytest.driver.find_element(By.ID, 'lk-btn').click()
    element = WebDriverWait(pytest.driver, 40).until(EC.presence_of_element_located((By.CLASS_NAME, 'iqOiiv')))
    pytest.driver.find_element(By.CLASS_NAME, 'iqOiiv').click()

    element = WebDriverWait(pytest.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span')))
    pytest.driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[3]/button/span').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'address')))
    pytest.driver.find_element(By.ID, 'address').send_keys('andrey92russ@mail.ru')
    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.ID, 'otp_get_code')))
    pytest.driver.find_element(By.ID, 'otp_get_code').click()

    element = WebDriverWait(pytest.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'otp-code-form__back-btn')))
    pytest.driver.find_element(By.CLASS_NAME, 'otp-code-form__back-btn').click()