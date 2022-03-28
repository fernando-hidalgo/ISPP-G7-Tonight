from ast import Try
from datetime import datetime
from itertools import count
from unicodedata import name
from xmlrpc.client import DateTime, _datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import DataError, IntegrityError
from .models import Empresa, Evento
# from .base import BaseTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import os

class EventosTestCase(StaticLiveServerTestCase):

    def setUp(self):    
        user_admin = User(username='admin', is_staff=True,  is_superuser=True, first_name='admin', last_name='last_name_admin', email='admin@gmail.com') 
        user_admin.set_password('admin')
        user_admin.email = "admin@email.com"
        user_admin.save()
        empresa = Empresa(user=User.objects.get(username='admin'), tlf=34)
        empresa.save()
        super().setUp()
        

    def tearDown(self):
        super().tearDown()

    def test_evento_positivo(self):
        evento = Evento(fecha=datetime(2022, 4, 16, 21, 00), precioEntrada=10, totalEntradas=50, nombre='Fiesta1', descripcion='Fiesta1', ubicacion='sevilla',salt= '1', empresa=Empresa.objects.get(id=1))
        evento.save()
        self.assertEqual(Evento.objects.count(), 1)  

    def test_fecha_anterior(self):
        evento = Evento(fecha=datetime(2020, 4, 16, 21, 00), precioEntrada=10, totalEntradas=50, nombre='Fiesta1', descripcion='Fiesta1', ubicacion='sevilla',salt= '1', empresa=Empresa.objects.get(id=1))
        try:
            evento.save()
        except DataError as e:
            self.assertIn('Ensure this value is greater than or equal',str(e))

    def test_precio_negativo(self):
        evento = Evento(fecha=datetime(2022, 4, 16, 21, 00), precioEntrada=-10, totalEntradas=50, nombre='Fiesta1', descripcion='Fiesta1', ubicacion='sevilla',salt= '1', empresa=Empresa.objects.get(id=1))
        try:
            evento.save()
        except DataError as e:
            self.assertIn('Out of range value for column',str(e))

    def test_totalEntradas_negativo(self):
        evento = Evento(fecha=datetime(2022, 4, 16, 21, 00), precioEntrada=10, totalEntradas=-5, nombre='Fiesta1', descripcion='Fiesta1', ubicacion='sevilla',salt= '1', empresa=Empresa.objects.get(id=1))
        try:
            evento.save()
        except DataError as e:
            self.assertIn('Out of range value for column',str(e))

# class SeleniumTestCase(StaticLiveServerTestCase):
    
#     def setUp(self):
#         user_admin = User(username='admin', is_staff=True,  is_superuser=True, first_name='admin', last_name='last_name_admin', email='admin@gmail.com') 
#         user_admin.set_password('admin')
#         user_admin.email = "admin@email.com"
#         user_admin.save()

#         options = webdriver.ChromeOptions()
#         options.headless = False
#         self.driver = webdriver.Chrome(options=options)

#         super().setUp()    

#     def tearDown(self):
#         super().tearDown()
#         self.driver.quit()

#     def test_crear_evento(self):                    
#         self.driver.get(f'{self.live_server_url}/admin/')
#         self.driver.find_element(By.ID, "id_username").send_keys("admin")
#         self.driver.find_element(By.ID, "id_password").send_keys("admin")
#         self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        
#         self.driver.find_element(By.LINK_TEXT, "Empresas").click()
#         self.driver.find_element_by_xpath("//*[contains(text(), 'Add empresa')]").click()
#         select = Select(self.driver.find_element_by_id('id_user'))
#         select.select_by_value('1')
#         self.driver.find_element(By.ID, "id_tlf").send_keys("666999666")
#         self.driver.find_element_by_name("_save").click()

#         self.driver.get(f'{self.live_server_url}/welcome_bussiness/')
#         self.driver.find_element_by_xpath("//*[contains(text(), 'Perfil')]").click()

#         self.driver.find_element_by_xpath("//*[contains(text(), 'Crear evento')]").click()
        
#         self.driver.find_element(By.ID, "id_fecha").send_keys("2022-06-12 21:00")
#         self.driver.find_element(By.ID, "id_precioEntrada").send_keys("12")
#         self.driver.find_element(By.ID, "id_totalEntradas").send_keys("50")
#         self.driver.find_element(By.ID, "id_nombre").send_keys("occo")
#         self.driver.find_element(By.ID, "id_descripcion").send_keys("Fiesta en occo")
#         self.driver.find_element(By.ID, "id_ubicacion").send_keys("Sevilla")
#         self.driver.find_element(By.ID, "id_salt").send_keys("1")
#         self.driver.find_element_by_name("save").click()

#         time.sleep(10)

#         self.assertEqual(Evento.objects.count(), 1)
