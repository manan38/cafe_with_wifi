from flask import Flask, render_template, jsonify, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(app)

conn = sqlite3.connect('cafes.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS cafes
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                location NOT NULL,
                wifi BOOLEAN NOT NULL,
                coffee_quality TEXT NOT NULL)''')
conn.commit()

# class Cafe(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     location = db.Column(db.string(100), nullable=False)
#     wifi = db.Column(db.Boolean, nullable=False)
#     coffee_quality = db.Column(db.String(50), nullable=False)
#
# db.create_all()

@app.route('/')
def index():
    # cafes = Cafe.query.filter_by(wifi=True, coffee_quality='good').all()
    return render_template('index.html')

@app.route('/cafes', methods=['GET'])
def get_cafes():
    cursor.execute("SELECT * FROM cafes WHERE wifi = 1 AND coffee_quality = 'good'")
    cafes = cursor.fetchall()
    return jsonify({'cafes': cafes})

@app.route('/cafes', methods=['POST'])
def add_cafe():
    if not request.form or not 'name' in request.form or not 'location' in request.form or not 'wifi' in request.form or not 'coffee_quality' in request.form:
        return redirect(url_for('index'))
    new_cafe = (request.form['name'], request.form['location'], request.form['wifi'], request.form['coffee_quality'])
    cursor.execute("INSERT INTO cafes (name, location, wifi, coffee_quality) VALUES (?, ?, ?, ?)", new_cafe)
    conn.commit()

    # name = request.form['name']
    # location = request.form['location']
    # wifi = request.form['wifi']
    # coffee_quality = request.form['coffee_quality']
    #
    # new_cafe = Cafe(name=name, location=location, wifi=bool(wifi), coffee_quality=coffee_quality)
    # db.session.add(new_cafe)
    # db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

