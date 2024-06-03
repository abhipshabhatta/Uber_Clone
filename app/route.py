from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # login
        return redirect(url_for('booking'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # registration
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # Here, you can add any logic needed for processing the booking
        return redirect(url_for('price_ride'))
    return render_template('booking.html')


@app.route('/price_ride', methods=['GET', 'POST'])
def price_ride():
    if request.method == 'POST':
        # Here, add any logic needed for processing the ride pricing
        return redirect(url_for('payment'))
    return render_template('price_ride.html')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Payment processing logic goes here
        return redirect(url_for('ride_confirmed'))
    return render_template('payment.html')

@app.route('/ride_confirmed')
def ride_confirmed():
    return render_template('ride_confirmed.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

def run_app():
    app.run(debug=True)
    

if __name__ == '__main__':
    app.run(debug=True)
