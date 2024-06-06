import unittest
from tests import create_app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()

    #  home route
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home Page', response.data)

    # login route
    def test_login_get(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login Page', response.data)

    #  login route with POST
    def test_login_post(self):
        response = self.client.post('/login', data=dict(
            username="testuser",
            password="testpassword"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # booking on login
        self.assertIn(b'Booking Page', response.data)

    # register route
    def test_register_get(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration Page', response.data)

    # register route with POST
    def test_register_post(self):
        response = self.client.post('/register', data=dict(
            username="newuser",
            email="newuser@example.com",
            password="newpassword"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # redirect to login on successful registration
        self.assertIn(b'Login Page', response.data)

    # booking route
    def test_booking_get(self):
        response = self.client.get('/booking')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Booking Page', response.data)

    # price_ride route
    def test_price_ride_get(self):
        response = self.client.get('/price_ride')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Price Ride Page', response.data)


    # ride_confirmed route
    def test_ride_confirmed(self):
        response = self.client.get('/ride_confirmed')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ride Confirmed Page', response.data)

if __name__ == '__main__':
    unittest.main()
