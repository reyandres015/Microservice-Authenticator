from locust import HttpUser, task, between


class WebsiteUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def registrar(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'ventas': [],
            'total': 0,
        }
        self.client.post(
            "/register", json=user_data)

    @task
    def login(self):
        user_data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.client.post(
            "/login", json=user_data)

    @ task
    def registrarVenta(self):
        self.client.post(
            "/ventas", json={'valor': 100}, headers={'username': 'testuser'})

    @ task
    def sumarVenta(self):
        self.client.post("/sumarVentas", json=100)
