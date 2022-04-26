from django.db.utils import DataError, IntegrityError
from django.test import TransactionTestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from psycopg2.errors import CheckViolation
import time
import os
from .models import Cliente, Empresa

# Create your tests here.

class ClienteTestCase(StaticLiveServerTestCase):
    
    reset_sequences = True

    def setUp(self):
        user_admin = User(username='admin', is_staff=True,  is_superuser=True, first_name='admin', last_name='last_name_admin', email='admin@gmail.com') 
        user_admin.set_password('admin')
        user_admin.email = "admin@email.com"
        user_admin.save()
        super().setUp()

    def tearDown(self):
        super().tearDown()
    
    def test_cliente_positivo(self):
        cliente= Cliente(user=User.objects.get(username='admin'),tlf='+41689864699',saldo=1000)
        cliente.save()
        self.assertEqual(Cliente.objects.count(),1)

    def test_cliente_con_usuario_duplicado(self):
        cliente1= Cliente(user=User.objects.get(username='admin'),tlf='+41689864699',saldo=1000)
        cliente1.save()
        cliente2= Cliente(user=User.objects.get(username='admin'),tlf='+41689864696',saldo=1000)
        try:
            cliente2.save()
        except IntegrityError as e:
            self.assertIn('duplicate key value violates unique constraint "proyecto_cliente_user_id_key"',str(e))
    

    def test_negative_tlf(self):
        cliente = Cliente(user=User.objects.get(username='admin'), tlf='-41689864699',saldo=1000)
        try:
            cliente.save()
        except DataError as e:
         self.assertIn('Out of range value for column', str(e))

    def test_tlf_muy_grande(self):
        cliente = Cliente(user=User.objects.get(username='admin'), tlf='+41689864699494694694',saldo=1000)
        try:
            cliente.save()
        except DataError as e:
         self.assertIn('Out of range value for column', str(e))

    def test_saldo_negativo(self):
        cliente=Cliente(user=User.objects.get(username='admin'),tlf='+41689864699',saldo=-1000)
        try:
            cliente.save()
        except IntegrityError as e:
            self.assertIn('violates check constraint "proyecto_cliente_saldo_check"', str(e))


    def test_no_hay_saldo(self):
        cliente= Cliente(user=User.objects.get(username='admin'),tlf='+41689864699')
        try:
            cliente.save()
        except IntegrityError as e:
            self.assertIn('null value in column "saldo" violates not-null constraint',str(e))

    def test_no_hay_tlf(self):
        cliente= Cliente(user=User.objects.get(username='admin'),saldo=1000)
        try:
            cliente.save()
        except IntegrityError as e:
            self.assertIn("Column 'tlf' cannot be null",str(e))
    
    def test_no_hay_user(self):
        cliente= Cliente(tlf='+41689864699',saldo=1000)
        try:
            cliente.save()
        except IntegrityError as e:
            self.assertIn('null value in column "user_id" violates not-null constraint',str(e))

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
    
    def test_crear_cliente(self):                    
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        
        self.driver.find_element(By.LINK_TEXT, "Clientes").click()
        self.driver.find_element_by_xpath("//*[contains(text(), 'Añadir cliente')]").click()
        select = Select(self.driver.find_element_by_id('id_user'))
        select.select_by_value('1')
        self.driver.find_element(By.ID, "id_tlf").send_keys("+41524204242")
        self.driver.find_element(By.ID, "id_saldo").send_keys("1000")
        absolute_file_path = os.path.abspath("media/media/test.jpg")
        self.driver.find_element(By.ID, "id_imagen").send_keys(absolute_file_path)
        self.driver.find_element_by_name("_save").click()
        
        self.driver.get(f'{self.live_server_url}')

        self.driver.find_element(By.NAME, "Acceder").click()
        self.driver.find_element(By.ID, "id_username").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys("admin")
        self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)

        self.driver.get(f'{self.live_server_url}/cliente/')

        self.assertEqual(Cliente.objects.count(), 1)
#         #assert 'Nombre: admin' in self.driver.page_source and 'Correo: admin@email.com' in self.driver.page_source and 'Teléfono: 524204242' in self.driver.page_source