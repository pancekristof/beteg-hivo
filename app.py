# Tárolók
data = {
    "Bőrgyógyászat": [],
    "Szemészet": [],
    "Urológia": []
}
called_numbers = []

@app.route('/input', methods=['GET', 'POST'])
def input_page():
    if request.method == 'POST':
        option = request.form['option']
        number = request.form['number']
        if option in data:
            data[option].append(number)
        return redirect('/input')
    return render_template('input.html', options=list(data.keys()))

@app.route('/admin')
def admin_page():
    return render_template('admin.html', data=data)

@app.route('/display')
def display_page():
    return render_template('display.html', data=data, called=called_numbers)

@app.route('/call')
def call_number():
    option = request.args.get('option')
    number = request.args.get('number')
    if number and number not in called_numbers:
        called_numbers.append(number)
    return '', 204
