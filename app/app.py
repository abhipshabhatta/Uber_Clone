from flask import Flask, render_template, redirect, request, url_for, flash
from forms import LoginForm, RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'azerty'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # login
        return redirect(url_for('booking'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # register
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # booking
        return redirect(url_for('price_ride'))
    return render_template('booking.html')


@app.route('/price_ride', methods=['GET', 'POST'])
def price_ride():
    if request.method == 'POST':
        # prices for ride
        return redirect(url_for('payment'))
    return render_template('price_ride.html')


@app.route('/ride_confirmed')
def ride_confirmed():
    return render_template('ride_confirmed.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)




