from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Szakrendelések és hozzájuk tartozó sorszámok
data = {
    "Bőrgyógyászat": [],
    "Szemészet": [],
    "Urológia": []
}

# Behívott sorszámok
called_numbers = []

# Input oldal – beteg belépés
@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        option = request.form['option']
        number = request.form['number']
        if option in data and number:
            data[option].append(number)
        return redirect('/input')
    return render_template('input.html', options=list(data.keys()))

# Admin oldal – sorszám behívás
@app.route('/admin')
def admin_page():
    return render_template('admin.html', data=data, called=called_numbers)

# Kijelző oldal – megjelenítés
@app.route('/display')
def display_page():
    return render_template('display.html', data=data, called=called_numbers)

# Behívás kezelése
@app.route('/call')
def call_number():
    option = request.args.get('option')
    number = request.args.get('number')
    if number and number not in called_numbers:
        called_numbers.append(number)
    return '', 204

# Lokális futtatáshoz
if __name__ == '__main__':
    app.run(debug=True)
