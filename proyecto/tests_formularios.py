from ast import Try
from itertools import count
from unicodedata import name
from django.contrib.auth.models import User
from django.db.utils import DataError, IntegrityError
from .models import Empresa, Cliente
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os


class SeleniumTestCase(StaticLiveServerTestCase):

    reset_sequences = True
    
    def setUp(self):
        user_admin = User(username='admin', is_staff=True,  is_superuser=True, first_name='admin', last_name='last_name_admin', email='admin@gmail.com') 
        user_admin.set_password('admin')
        user_admin.save()


        options = webdriver.ChromeOptions()
        options.headless = False
        self.driver = webdriver.Chrome(options=options)

        super().setUp()    

    def tearDown(self):
        super().tearDown()
        self.driver.quit()
        
    def test_crear_cliente(self):                    
        self.driver.get(f'{self.live_server_url}')
        self.driver.find_element(By.NAME, "registro_cliente").click()

        self.driver.find_element(By.ID, "id_username").send_keys("james_bond")
        self.driver.find_element(By.ID, "id_email").send_keys("bond@007.com")
        self.driver.find_element(By.ID, "id_password1").send_keys("asdkfioe1")
        self.driver.find_element(By.ID, "id_password2").send_keys("asdkfioe1")
        self.driver.find_element(By.ID, "id_tlf_1").send_keys("666999666")
        absolute_file_path = os.path.abspath("media/media/test.jpg")
        self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
        self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

        message = self.driver.find_element_by_id('id_username').get_attribute('validationMessage')
        

        assert User.objects.count() == 2

    def test_crear_cliente_sin_nombre(self):                    
        self.driver.get(f'{self.live_server_url}')
        self.driver.find_element(By.NAME, "registro_cliente").click()

        self.driver.find_element(By.ID, "id_email").send_keys("taylor@hawkins.com")
        self.driver.find_element(By.ID, "id_password1").send_keys("asdkfioe1")
        self.driver.find_element(By.ID, "id_password2").send_keys("asdkfioe1")
        self.driver.find_element(By.ID, "id_tlf_1").send_keys("666999666")
        absolute_file_path = os.path.abspath("media/media/test.jpg")
        self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
        self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

        message = self.driver.find_element_by_id('id_username').get_attribute('validationMessage')
        

        assert "Completa este campo" in message

    def test_crear_cliente_sin_mail(self):                    
        self.driver.get(f'{self.live_server_url}')
        self.driver.find_element(By.NAME, "registro_cliente").click()

        self.driver.find_element(By.ID, "id_username").send_keys("maynard_keenan")
        self.driver.find_element(By.ID, "id_password1").send_keys("asdkfioe1")
        self.driver.find_element(By.ID, "id_password2").send_keys("asdkfioe1")
        self.driver.find_element(By.ID, "id_tlf_1").send_keys("666999666")
        absolute_file_path = os.path.abspath("media/media/test.jpg")
        self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
        self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

        assert User.objects.count() == 2
    
    def test_crear_cliente_sin_password1(self):                    
            self.driver.get(f'{self.live_server_url}')
            self.driver.find_element(By.NAME, "registro_cliente").click()

            self.driver.find_element(By.ID, "id_username").send_keys("palpatine")
            self.driver.find_element(By.ID, "id_email").send_keys("viva@elimperio.com")
            self.driver.find_element(By.ID, "id_password2").send_keys("quemalvadosoy")
            self.driver.find_element(By.ID, "id_tlf_1").send_keys("666999666")
            absolute_file_path = os.path.abspath("media/media/test.jpg")
            self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
            self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

            message = self.driver.find_element_by_id('id_password1').get_attribute('validationMessage')
            

            assert "Completa este campo" in message

    def test_crear_cliente_sin_password2(self):                    
            self.driver.get(f'{self.live_server_url}')
            self.driver.find_element(By.NAME, "registro_cliente").click()

            self.driver.find_element(By.ID, "id_username").send_keys("palpatine")
            self.driver.find_element(By.ID, "id_email").send_keys("viva@elimperio.com")
            self.driver.find_element(By.ID, "id_password1").send_keys("quemalvadosoy")
            self.driver.find_element(By.ID, "id_tlf_1").send_keys("666999666")
            absolute_file_path = os.path.abspath("media/media/test.jpg")
            self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
            self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

            message = self.driver.find_element_by_id('id_password2').get_attribute('validationMessage')
            

            assert "Completa este campo" in message

    def test_crear_cliente_sin_tlf(self):                    
            self.driver.get(f'{self.live_server_url}')
            self.driver.find_element(By.NAME, "registro_cliente").click()

            self.driver.find_element(By.ID, "id_username").send_keys("palpatine")
            self.driver.find_element(By.ID, "id_email").send_keys("viva@elimperio.com")
            self.driver.find_element(By.ID, "id_password1").send_keys("quemalvadosoy")
            self.driver.find_element(By.ID, "id_password2").send_keys("quemalvadosoy")
            absolute_file_path = os.path.abspath("media/media/test.jpg")
            self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
            self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

            message = self.driver.find_element_by_id('id_tlf_1').get_attribute('validationMessage')
            

            assert "Completa este campo" in message

    def test_crear_cliente_sin_imagen(self):                    
            self.driver.get(f'{self.live_server_url}')
            self.driver.find_element(By.NAME, "registro_cliente").click()

            self.driver.find_element(By.ID, "id_username").send_keys("palpatine")
            self.driver.find_element(By.ID, "id_email").send_keys("viva@elimperio.com")
            self.driver.find_element(By.ID, "id_password1").send_keys("quemalvadosoy")
            self.driver.find_element(By.ID, "id_password2").send_keys("quemalvadosoy")
            self.driver.find_element(By.ID, "id_tlf_1").send_keys("666999666")
            self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

            message = self.driver.find_element_by_id('id_imagen').get_attribute('validationMessage')
            

            assert "Selecciona un archivo" in message
        
    def test_crear_cliente_email_repetido(self):                    
        self.driver.get(f'{self.live_server_url}')
        self.driver.find_element(By.NAME, "registro_cliente").click()

        self.driver.find_element(By.ID, "id_username").send_keys("dave_grohl")
        self.driver.find_element(By.ID, "id_email").send_keys("admin@gmail.com")
        self.driver.find_element(By.ID, "id_password1").send_keys("asdkfioe1")
        self.driver.find_element(By.ID, "id_password2").send_keys("asdkfioe1")
        self.driver.find_element(By.ID, "id_tlf_1").send_keys("666999666")
        absolute_file_path = os.path.abspath("media/media/test.jpg")
        self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
        self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

        assert 'Ya existe Usuario con este Dirección de correo electrónico.' in self.driver.page_source

    def test_crear_cliente_passwords_no_coinciden(self):                    
        self.driver.get(f'{self.live_server_url}')
        self.driver.find_element(By.NAME, "registro_cliente").click()

        self.driver.find_element(By.ID, "id_username").send_keys("matt_bellamy")
        self.driver.find_element(By.ID, "id_email").send_keys("matt@muse.com")
        self.driver.find_element(By.ID, "id_password1").send_keys("unacosa1")
        self.driver.find_element(By.ID, "id_password2").send_keys("otracosa2")
        self.driver.find_element(By.ID, "id_tlf_1").send_keys("666999666")
        absolute_file_path = os.path.abspath("media/media/test.jpg")
        self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
        self.driver.find_element(By.ID, "id_email").send_keys(Keys.ENTER)

        assert 'Los dos campos de contraseña no coinciden.' in self.driver.page_source