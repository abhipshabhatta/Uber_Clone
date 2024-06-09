from flask import Flask, render_template, redirect, request, url_for, flash, session
from forms import LoginForm, RegistrationForm
from flask_session import Session
import redis
from app.json_serializer import JSONSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'azerty'

# Redis configuration for sessions
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.StrictRedis(host='localhost', port=6379, db=0)
app.config['SESSION_INTERFACE'] = JSONSerializer()

# Initialize the Flask-Session extension
server_session = Session(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login logic
        session['user'] = form.username.data 
        return redirect(url_for('booking'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # register logic
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # booking logic
        return redirect(url_for('price_ride'))
    return render_template('booking.html')

@app.route('/price_ride', methods=['GET', 'POST'])
def price_ride():
    if request.method == 'POST':
        # prices for ride logic
        return redirect(url_for('payment'))
    return render_template('price_ride.html')

@app.route('/ride_confirmed')
def ride_confirmed():
    return render_template('ride_confirmed.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
