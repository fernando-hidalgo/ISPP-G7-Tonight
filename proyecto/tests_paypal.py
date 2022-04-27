from unicodedata import name
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from .models import Cliente, Empresa, User
import time


class SeleniumTestCase(StaticLiveServerTestCase):

    reset_sequences = True
    
    def setUp(self):
        user_cliente = User(username='thomy', is_staff=False,  is_superuser=False, email='thomyorke@gmail.com') 
        user_cliente.set_password('radiohead')
        user_cliente.save()

        cliente = Cliente(user=User.objects.get(id=1), saldo=0, tlf='+34 666 666 666')
        cliente.save()

        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        super().setUp()    

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
    
    def test_recargar_saldo(self):                    
        self.driver.get(f'{self.live_server_url}')
        self.driver.find_element(By.NAME, "Acceder").click()
        
        self.driver.find_element(By.ID, "id_username").send_keys("thomy")
        self.driver.find_element(By.ID, "id_password").send_keys("radiohead")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)

        user = User.objects.get(username='thomy')
        self.driver.get(f'{self.live_server_url}/cliente/' + str(user.id) +'/saldo')
        self.driver.find_element(By.ID, "id_cantidad").send_keys("30")
        self.driver.find_element(By.ID, "id_cantidad").send_keys(Keys.ENTER)

        self.driver.find_element(By.NAME, "submit").click()

        self.driver.set_window_size(1920, 1080)
        self.driver.find_element(By.ID, "email").send_keys("cliente@tonight.com")
        self.driver.find_element(By.ID, "email").send_keys(Keys.ENTER)
        time.sleep(2)
        self.driver.find_element(By.ID, "password").send_keys("2A=[U#o^")
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)

        element = self.driver.find_element(By.ID, "payment-submit-btn")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        element.click()

        time.sleep(3)
        self.driver.find_element_by_xpath("//*[contains(text(), 'Volver al vendedor')]").click()
        time.sleep(10)

        assert Cliente.objects.get(id=1).saldo != 0