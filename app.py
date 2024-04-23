from flask import Flask, render_template, request, redirect, url_for
from model import Estate

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/start', methods=['POST'])
def start():
    estate_name = request.form['estate_name']
    estate = Estate(estate_name)
    estate.start_campaign()

    # Handle start logic here
    return redirect(url_for('home'))

@app.route('/load', methods=['POST'])
def load():
    # Handle load logic here
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
