from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Előre definiált állomások
data = {
    "Bőrgyógyászat": [],
    "Szemészet": [],
    "Urológia": []
}

# Behívott sorszámok
called_numbers = []

# Input oldal - beteg beléptetés
@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        option = request.form['option']
        number = request.form['number']
        if option in data:
            data[option].append(number)
        return redirect('/input')
    return render_template('input.html', options=list(data.keys()))

# Admin oldal - hívásra alkalmas sorszámok
@app.route('/admin')
def admin_page():
    return render_template('admin.html', data=data)

# Kijelző oldal - sorszámok megjelenítése
@app.route('/display')
def display_page():
    return render_template('display.html', data=data, called=called_numbers)

# Behívás - admin oldalról történik
@app.route('/call')
def call_number():
    option = request.args.get('option')
    number = request.args.get('number')
    if number and number not in called_numbers:
        called_numbers.append(number)
    return '', 204

# Fejlesztési mód helyi futtatásra
if __name__ == '__main__':
    app.run(debug=True)
