# ISPP-G7-Tonight
Project for ISPP
Para la configuración de este proyecto es necesario disponer en tu equipo de python 3.8, django y mysql.
Para la configuración de la conexión mysql es necesario instalarse mysql-server, por ello usamos el comando:
$sudo apt-get install mysql-server
Para comprobar que se ha installado correctamente usamos el comando 
sudo mysql
Posteriormente procedemos a configurar mysql siguiendo el siguiente tutorial:
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04-es
(Importante la contraseña del usuario root debe ser "password").
Una vez este configurado mysql es necesario installar mysqlclient para ello usamos el comando:
pip install mysqlclient
Para la creación de la base de datos es necesario seguir los pasos del siguiente video:
https://www.youtube.com/watch?v=Anxfp8R5d8w
(Importante usar los parámetros DATABASES del archivo settings.py de la carpeta ToNight).
