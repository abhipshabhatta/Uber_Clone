from flask import Flask, render_template, request, redirect, url_for, session, flash
from app.mongodb_client import MongoDBClient
from app.ride_model import RideModel
from app.driver_model import DriverModel
from app.user_model import UserModel
from app.price_model import PriceModel
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from redis import Redis  # Correct import for Redis client

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'azerty'

# Redis client setup
redis_client = Redis(host='localhost', port=6380, db=0)  # Corrected Redis client initialization

# MongoDB client setup
username = 'abhipshabhatta'
password = '@bheeps@123'
mongo_client = MongoDBClient(username=username, password=password)
ride_model = RideModel(db_client=mongo_client)
driver_model = DriverModel(db_client=mongo_client)
user_model = UserModel(db_client=mongo_client)
price_model = PriceModel(db_client=mongo_client)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_driver', methods=['GET', 'POST'])
def add_driver():
    if request.method == 'POST':
        driver_data = {
            "name": request.form['name'],
            "license_number": request.form['license_number']
        }
        driver_id = driver_model.create_driver(driver_data)
        return redirect(url_for('driver_added', driver_id=driver_id))
    return render_template('add_driver.html')

@app.route('/driver_added')
def driver_added():
    driver_id = request.args.get('driver_id')
    return f"Driver added with ID: {driver_id}"

@app.route('/update_driver/<driver_id>', methods=['GET', 'POST'])
def update_driver(driver_id):
    if request.method == 'POST':
        driver_data = {
            "name": request.form['name'],
            "license_number": request.form['license_number']
        }
        driver_model.update_driver(driver_id, driver_data)
        return redirect(url_for('driver_updated', driver_id=driver_id))
    driver = driver_model.get_driver(driver_id)
    return render_template('update_driver.html', driver=driver, driver_id=driver_id)

@app.route('/driver_updated')
def driver_updated():
    driver_id = request.args.get('driver_id')
    return f"Driver updated with ID: {driver_id}"

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        pickup_location = request.form['pickup_location']
        dropoff_location = request.form['dropoff_location']
        # Redirect to price_ride with locations
        return redirect(url_for('price_ride', pickup_location=pickup_location, dropoff_location=dropoff_location))
    return render_template('booking.html')

@app.route('/price_ride', methods=['GET', 'POST'])
def price_ride():
    price = None
    pickup_location = request.args.get('pickup_location')
    dropoff_location = request.args.get('dropoff_location')
    if pickup_location and dropoff_location:
        price = get_cached_price(pickup_location, dropoff_location)
    return render_template('price_ride.html', price=price)

def get_cached_price(start_location, end_location):
    cache_key = f"price:{start_location}:{end_location}"
    cached_price = redis_client.get(cache_key)
    if cached_price:
        return float(cached_price)

    # If not in cache, calculate the price
    price = price_model.calculate_price(start_location, end_location)

    # Store the calculated price in cache with an expiry time (e.g., 10 minutes)
    redis_client.setex(cache_key, 600, price)
    return price

@app.route('/request_ride', methods=['POST'])
def request_ride():
    pickup_location = request.form.get('pickup_location')
    dropoff_location = request.form.get('dropoff_location')
    ride_type = request.form.get('ride_type')
    price = request.form.get('price')

    print(f"pickup_location: {pickup_location}, dropoff_location: {dropoff_location}, ride_type: {ride_type}, price: {price}")

    ride_data = {
        "pickup_location": pickup_location,
        "dropoff_location": dropoff_location,
        "ride_type": ride_type,
        "price": price,
        "status": "requested"
    }
    ride_id = ride_model.create_ride(ride_data)
    return redirect(url_for('show_route', pickup_location=pickup_location, dropoff_location=dropoff_location, ride_type=ride_type, price=price))

@app.route('/show_route')
def show_route():
    pickup_location = request.args.get('pickup_location')
    dropoff_location = request.args.get('dropoff_location')
    ride_type = request.args.get('ride_type')
    price = request.args.get('price')
    return render_template('show_route.html', pickup_location=pickup_location, dropoff_location=dropoff_location, ride_type=ride_type, price=price)

@app.route('/ride_confirmed')
def ride_confirmed():
    ride_id = request.args.get('ride_id')
    return render_template('ride_confirmed.html', ride_id=ride_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"User Login Attempt: {email}")
        user = user_model.get_user_by_email(email)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            flash('Login successful', 'success')
            return redirect(url_for('booking'))  # Redirect to booking page
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data = {
            "name": request.form['fullName'],
            "email": request.form['email'],
            "password": generate_password_hash(request.form['password'])
        }
        print(f"Registering user: {user_data}")
        user_id = user_model.create_user(user_data)
        return redirect(url_for('login'))
    return render_template('Register.html')

@app.route('/register_driver', methods=['GET', 'POST'])
def register_driver():
    if request.method == 'POST':
        driver_data = {
            "name": request.form['name'],
            "email": request.form['email'],
            "password": generate_password_hash(request.form['password']),
            "phone": request.form['phone'],
            "license": request.form['license']
        }
        print(f"Registering driver: {driver_data}")
        driver_id = driver_model.create_driver(driver_data)
        return redirect(url_for('login_driver'))  # Redirect to driver login
    return render_template('register_driver.html')

@app.route('/login_driver', methods=['GET', 'POST'])
def login_driver():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Driver Login Attempt: {email}")
        driver = driver_model.get_driver_by_email(email)
        print(f"Fetched Driver: {driver}")
        if driver and check_password_hash(driver['password'], password):
            session['driver_id'] = str(driver['_id'])
            flash('Driver login successful', 'success')
            return redirect(url_for('driver_dashboard'))  # Redirect to driver dashboard
        else:
            flash('Invalid email or password', 'danger')
    return render_template('login_driver.html')

@app.route('/driver_dashboard')
def driver_dashboard():
    if 'driver_id' not in session:
        return redirect(url_for('login_driver'))
    rides = ride_model.get_requested_rides()
    return render_template('driver_dashboard.html', rides=rides)

@app.route('/accept_ride/<ride_id>', methods=['POST'])
def accept_ride(ride_id):
    ride = ride_model.get_ride_by_id(ride_id)
    ride_model.update_ride_status(ride_id, 'accepted')
    return redirect(url_for('show_route', pickup_location=ride['pickup_location'], dropoff_location=ride['dropoff_location'], ride_type=ride['ride_type'], price=ride['price']))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
