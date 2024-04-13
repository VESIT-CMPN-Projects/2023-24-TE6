from flask import Flask, render_template, request, redirect, url_for, session
import joblib
from send_sms import send_twilio_sms

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Load the trained model
model = joblib.load('model/model.pkl')

# Dummy login credentials and schemes data
USERS = {
    'admin': {'password': 'admin', 'schemes': ['Ukai', 'Damanganga', 'Watrak', 'Guhai', 'Mazam', 'Hathmati', 'Javanpura', 'Harnav-II', 'Meshwo', 'Wanakbor', 'Panam', 'Hadaf', 'Kadana', 'Karjan', 'Sukhi', 'Mukteshwar', 'Dantiwada', 'Sipu', 'Dharoi', 'Khodiyar', 'Shetrunji', 'Und-I', 'Bhadar', 'Bhadar-II', 'Machchhu-II', 'Machchhu - I', 'Brahmani']},
    'admin1': {'password': 'admin1', 'schemes': ['Ukai', 'Damanganga', 'Watrak', 'Guhai', 'Mazam', 'Hathmati', 'Javanpura', 'Harnav-II', 'Meshwo', 'Wanakbor']},
    'admin2': {'password': 'admin2', 'schemes': ['Panam', 'Hadaf', 'Kadana', 'Karjan', 'Sukhi', 'Mukteshwar', 'Dantiwada', 'Sipu', 'Dharoi', 'Khodiyar', 'Shetrunji', 'Und-I', 'Bhadar', 'Bhadar-II', 'Machchhu-II', 'Machchhu - I', 'Brahmani']}
}


@app.route('/')
def login_page():
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def login():
    if request.method == 'POST':
        # Check login credentials
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS and USERS[username]['password'] == password:
            # Set the user as logged in
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('predictor'))
        else:
            return render_template('index.html', error='Invalid credentials')

@app.route('/predictor')
def predictor():
    # Check if the user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    username = session['username']
    schemes = USERS[username]['schemes']

    return render_template('predictor.html', schemes=schemes)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get data from the form
        features = [
            float(request.form['design-gross-storage']),
            float(request.form['frl']),
            float(request.form['rule-level']),
            float(request.form['present-water-level']),
            float(request.form['present-gross-storage']),
            float(request.form['inflow']),
            float(request.form['outflow-river']),
            float(request.form['ouflow-canal']),
            float(request.form['cumm-rainfall']),
            int(request.form['type-of-gate']),
            float(request.form['gate-position']),
            float(request.form['opening']),
            int(request.form['scheme'])
        ]

        # Make prediction
        prediction = model.predict([features])

        # Determine if it will overflow or not
        result = "OVERFLOW" if prediction > 0.5 else "SAFE"

        # Send SMS only if there is an overflow
        send_twilio_sms(result)

        # Render the corresponding HTML page
        return render_template(f'{result.lower()}.html')

if __name__ == '__main__':
    app.run(debug=True)
