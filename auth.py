import requests
import json

# URL base de la API
base_url = 'http://localhost:5000'

# Datos del usuario
user_data = {
    'username': 'your_username',
    'password': 'your_password'
}

# funcion para registrar un usuario
def register_user():
    # set de user_data con input
    user_data['username'] = input('Ingrese un nuevo nombre de usuario: ')
    user_data['password'] = input('Ingrese su  nueva contraseña: ')
    response = requests.post(f'{base_url}/register', json=user_data)
    print('Registro:', response.json())
    
# funcion para iniciar sesion
def login_user():
    # set user_data con input
    user_data['username'] = input('Ingrese su nombre de usuario: ')
    user_data['password'] = input('Ingrese su contraseña: ')
    response = requests.post(f'{base_url}/login', json=user_data)
    validate_token(response.json().get('token'))

# funcion para validar el token
def validate_token(token):
    headers = {'Authorization': token}
    response = requests.post(f'{base_url}/validate', headers=headers)
    print('Validación:', response.json())

# menu de opciones
token = None
while True:
    print('1. Registrar usuario')
    print('2. Iniciar sesión')
    print('3. Salir')
    option = input('Seleccione una opción: ')
    if option == '1':
        register_user()
    elif option == '2':
        token = login_user()
    elif option == '3':
        break
    else:
        print('Opción inválida')