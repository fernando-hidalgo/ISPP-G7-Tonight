from ast import Try
from itertools import count
from unicodedata import name
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.db.utils import DataError, IntegrityError
from .models import Empresa
# from .base import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os

# Create your tests here.

class EmpresaTestCase(TransactionTestCase):

    def setUp(self):    
        user_admin = User(username='admin', is_staff=True,  is_superuser=True, first_name='admin', last_name='last_name_admin', email='admin@gmail.com') 
        user_admin.set_password('admin')
        user_admin.email = "admin@email.com"
        user_admin.save()
        super().setUp()
        

    def tearDown(self):
        super().tearDown()

    def test_tlf_positivo(self):
        empresa = Empresa(user=User.objects.get(username='admin'), tlf=34)
        empresa.save()
        self.assertEqual(Empresa.objects.count(), 1)   

    def test_usuario_duplicado(self):
        empresa1 = Empresa(user=User.objects.get(username='admin'), tlf=34)
        empresa1.save()
        empresa2 = Empresa(user=User.objects.get(username='admin'), tlf=666)
        try:
            empresa2.save()
        except IntegrityError as e:
            self.assertIn('Duplicate entry', str(e))

    def test_tlf_negativo(self):
        empresa = Empresa(user=User.objects.get(username='admin'), tlf=-34)
        try:
            empresa.save()
        except DataError as e:
        #  print('Hola' + str(e))
         self.assertIn('Out of range value for column', str(e))

    def test_tlf_muy_grande(self):
        empresa = Empresa(user=User.objects.get(username='admin'), tlf=999999999999999999)
        try:
            empresa.save()
        except DataError as e:
         self.assertIn('Out of range value for column', str(e))


    
class SeleniumTestCase(StaticLiveServerTestCase):

    reset_sequences = True
    
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

        # time.sleep(10)

        self.assertEqual(Empresa.objects.count(), 1)
        assert 'Nombre: admin' in self.driver.page_source and 'Correo: admin@email.com' in self.driver.page_source and 'Teléfono: 666999666' in self.driver.page_source