import requests
import json
import threading


# URL base de la API
base_url = 'http://localhost:5000'

# Datos del usuario
user_data = {
    'username': '',
    'password': '',
    'token': '',
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
    user_data['token'] = response.json().get('token')
    return validate_token(user_data['token'])

# funcion para validar el token


def validate_token(token):
    headers = {'Authorization': token}
    response = requests.post(f'{base_url}/validate', headers=headers)
    if response.json().get('message') == 'Invalid token':
        print('Token inválido')
        return False
    elif response.json().get('message') == 'Token has expired':
        print('Token expirado')
        return False
    elif response.json().get('message') == 'Token is valid':
        return True


def postVenta(venta):
    headers = {'username': user_data['username']}
    response = requests.post(f'{base_url}/ventas', headers=headers, json=venta)
    print('Venta registrada:', response.json())


def postValorTotal(valor):
    print(valor)
    response = requests.post(f'{base_url}/sumarVentas', json=valor)
    print('Valor total de venta por usuario:', response.json())


def registerVenta(venta):
    if (validate_token(user_data['token'])):
        tcp_thread = threading.Thread(target=postVenta, args=(venta,))
        tcp_thread.daemon = True

        tcp_thread2 = threading.Thread(
            target=postValorTotal, args=(venta['valor'],))
        tcp_thread2.daemon = True

        tcp_thread.start()
        tcp_thread2.start()

        # Esperar a que los hilos terminen
        tcp_thread.join()
        tcp_thread2.join()


def menu2():
    while True:
        print('1. Registrar venta')
        print('2. Cerrar sesión')
        option = input('Seleccione una opción: ')
        if option == '1':
            venta = {
                'detalle': str(input('Ingrese el detalle de la venta: ')),
                'valor': int(input('Ingrese el valor de la venta: ')),
            }
            registerVenta(venta)
        elif option == '2':
            break
        else:
            print('Opción inválida')


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
        if (login_user()):
            menu2()
    elif option == '3':
        break
    else:
        print('Opción inválida')
