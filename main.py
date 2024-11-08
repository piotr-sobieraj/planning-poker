from flask import Flask, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = 'team42'  # Klucz do sesji 

# Lista do przechowywania wyników
results = []

# Formularz dla klientów
@app.route('/', methods=['GET', 'POST'])
def client_form():
  if request.method == 'POST':
    name = request.form.get('name')
    points = request.form.get('points')

    if name:
      session['name'] = name  # Zapisanie imienia w sesji

    if name and points:
      results.append({'name': name, 'points': points})

    return redirect(url_for('client_form'))

  # Pobranie imienia z sesji, jeśli jest
  name_in_session = session.get('name', '')
  return render_template('client_form.html', name=name_in_session)

# Widok do zbierania wyników
@app.route('/results', methods=['GET'])
def results_view():
  return render_template('results.html')

# Endpoint do pobierania wyników w formacie JSON
@app.route('/get_results', methods=['GET'])
def get_results():
  return jsonify(results)

# Endpoint do resetowania wyników
@app.route('/reset', methods=['POST'])
def reset():
  global results
  results = []
  return redirect(url_for('results_view'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
