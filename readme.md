# Prueba

Proyecto de pruebas

## Debian

sudo apt-get install python-virtualenv virtualenv
virtualenv env --python=python3
source env/bin/activate
pip install -r .\requirement.txt
python .\manage.py runserver

## Windows

virtualenv env
.\env\Scripts\activate
pip install -r .\requirement.txt
python .\manage.py runserver

## Endpoints

### Generar token

http://localhost:8000/token-auth

### Listar cambio de dolares a pesos

http://localhost:8000/exchange

### Panel de administración

http://localhost:8000/admin

## Claves de prueba

Usuario: admin
Password: admin
