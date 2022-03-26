from django.test import TestCase
from django.contrib.auth.models import User
# from .base import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os

# Create your tests here.

class SeleniumTestCase(StaticLiveServerTestCase):
    
    def setUp(self):
        user_admin = User(username='admin', is_staff=True,  is_superuser=True, first_name='admin', last_name='last_name_admin', email='admin@gmail.com') 
        user_admin.set_password('admin')
        user_admin.email = "admin@email.com"
        user_admin.save()


        options = webdriver.ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)

        super().setUp()    

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
    
    def test_crear_empresa(self):                    
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        
        self.driver.find_element(By.LINK_TEXT, "Empresas").click()
        self.driver.find_element_by_xpath("//*[contains(text(), 'Add empresa')]").click()
        select = Select(self.driver.find_element_by_id('id_user'))
        select.select_by_value('1')
        self.driver.find_element(By.ID, "id_tlf").send_keys("666999666")
        self.driver.find_element_by_name("_save").click()

        self.driver.get(f'{self.live_server_url}/welcome_bussiness/')
        self.driver.find_element_by_xpath("//*[contains(text(), 'Perfil')]").click()

        time.sleep(10)

        assert 'Nombre: admin' in self.driver.page_source and 'Correo: admin@email.com' in self.driver.page_source and 'Teléfono: 666999666' in self.driver.page_source