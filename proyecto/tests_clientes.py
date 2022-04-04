# from django.db.utils import DataError, IntegrityError
# from django.test import TransactionTestCase
# from django.contrib.auth.models import User
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# import time
# import os
# from .models import Cliente, Empresa

# # Create your tests here.

# class ClienteTestCase(StaticLiveServerTestCase):
#     reset_sequences = True

#     def setUp(self):
#         user_admin = User(username='admin', is_staff=True,  is_superuser=True, first_name='admin', last_name='last_name_admin', email='admin@gmail.com') 
#         user_admin.set_password('admin')
#         user_admin.email = "admin@email.com"
#         user_admin.save()
#         super().setUp()

#     def tearDown(self):
#         super().tearDown()
    
#     def test_cliente_positivo(self):
#         cliente= Cliente(user=User.objects.get(username='admin'),tlf=44,saldo=1000)
#         cliente.save()
#         self.assertEqual(Cliente.objects.count(),1)

#     def test_cliente_con_usuario_duplicado(self):
#         cliente1= Cliente(user=User.objects.get(username='admin'),tlf=44,saldo=1000)
#         cliente1.save()
#         cliente2= Cliente(user=User.objects.get(username='admin'),tlf=88,saldo=1000)
#         try:
#             cliente2.save()
#         except IntegrityError as e:
#             self.assertIn('Duplicate entry',str(e))
    

#     def test_negative_tlf(self):
#         cliente = Cliente(user=User.objects.get(username='admin'), tlf=-44,saldo=1000)
#         try:
#             cliente.save()
#         except DataError as e:
#          self.assertIn('Out of range value for column', str(e))

#     def test_tlf_muy_grande(self):
#         cliente = Cliente(user=User.objects.get(username='admin'), tlf=444444444444444444,saldo=1000)
#         try:
#             cliente.save()
#         except DataError as e:
#          self.assertIn('Out of range value for column', str(e))

#     def test_saldo_negativo(self):
#         cliente=Cliente(user=User.objects.get(username='admin'),tlf=44,saldo=-1000)
#         try:
#             cliente.save()
#         except DataError as e:
#          self.assertIn('Out of range value for column', str(e))


#     def test_no_hay_saldo(self):
#         cliente= Cliente(user=User.objects.get(username='admin'),tlf=44)
#         try:
#             cliente.save()
#         except IntegrityError as e:
#             self.assertIn("Column 'saldo' cannot be null",str(e))

#     def test_no_hay_tlf(self):
#         cliente= Cliente(user=User.objects.get(username='admin'),saldo=1000)
#         try:
#             cliente.save()
#         except IntegrityError as e:
#             self.assertIn("Column 'tlf' cannot be null",str(e))
    
#     def test_no_hay_user(self):
#         cliente= Cliente(tlf=44,saldo=1000)
#         try:
#             cliente.save()
#         except IntegrityError as e:
#             self.assertIn("Column 'user_id' cannot be null",str(e))

# class SeleniumClienteTestCase(StaticLiveServerTestCase):
#     reset_sequences = True
    
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
    
#     def test_crear_cliente(self):                    
#         self.driver.get(f'{self.live_server_url}/admin/')
#         self.driver.find_element(By.ID, "id_username").send_keys("admin")
#         self.driver.find_element(By.ID, "id_password").send_keys("admin")
#         self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
        
#         self.driver.find_element(By.LINK_TEXT, "Clientes").click()
#         self.driver.find_element_by_xpath("//*[contains(text(), 'Add cliente')]").click()
#         select = Select(self.driver.find_element_by_id('id_user'))
#         select.select_by_value('1')
#         self.driver.find_element(By.ID, "id_tlf").send_keys("666999666")
#         self.driver.find_element(By.ID, "id_saldo").send_keys("1000")
#         self.driver.find_element_by_name("_save").click()

#         self.driver.get(f'{self.live_server_url}/welcome_client/')
#         self.driver.find_element_by_xpath("//*[contains(text(), 'Perfil')]").click()

#         self.assertEqual(Cliente.objects.count(), 1)
#         assert 'Nombre: admin' in self.driver.page_source and 'Correo: admin@email.com' in self.driver.page_source and 'Teléfono: 666999666' in self.driver.page_source