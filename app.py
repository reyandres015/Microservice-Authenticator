from flask import Flask, request, jsonify
import jwt
import datetime
import hashlib
import socket
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Simulando una base de datos de usuarios
users_db = []
totalValores = 0  # Variable para almacenar el total de ventas de todos los usuarios

# Función auxiliar para hashear contraseñas


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Ruta para registrar un nuevo usuario


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users_db:
        return jsonify({'message': 'User already exists'}), 409

    new_user = {
        'username': username,
        'password': hash_password(password),
        'ventas': [],
        'total': 0,
    }

    users_db.append(new_user)
    return jsonify({'message': 'User registered successfully'}), 201

# Ruta para autenticar a un usuario y generar un token JWT


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    hashed_password = hash_password(password)

    for user in users_db:
        if user['username'] == username and user['password'] == hashed_password:
            token = jwt.encode({
                'username': username,
                'password': password,
                'ventas': user['ventas'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

# Ruta para validar el token JWT


@app.route('/validate', methods=['POST'])
def validate():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    try:
        data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': 'Token is valid', 'username': data['username']}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


@app.route('/ventas', methods=['POST'])
def registrarVenta():
    venta = request.get_json()
    username = request.headers.get('username')

    for user in users_db:
        if user['username'] == username:
            user['ventas'].append(venta)
            user['total'] += int(venta['valor'])
            return jsonify({'message': 'Venta registrada'}), 200

    return jsonify({'message': 'Usuario no encontrado'}), 404


@app.route('/sumarVentas', methods=['POST'])
def sumarVenta():
    global totalValores
    valor = request.get_json()
    totalValores += int(valor)

    return jsonify({'message': 'Total actualizado: ', 'total': totalValores}), 200

# Función para manejar conexiones TCP


def handle_tcp_connection(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Datos recibidos: {data}")
    client_socket.send("Datos recibidos".encode('utf-8'))
    client_socket.close()

# Servidor TCP


def start_tcp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Servidor TCP en marcha, esperando conexiones...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida con {addr}")
        threading.Thread(target=handle_tcp_connection,
                         args=(client_socket,)).start()


# Iniciar el servidor de sockets TCP en un hilo separado
tcp_thread = threading.Thread(target=start_tcp_server)
tcp_thread.daemon = True
tcp_thread.start()

if __name__ == '__main__':
    app.run(debug=True)
