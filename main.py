from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from replit import db

app = Flask(__name__)
app.secret_key = 'team42'  # Klucz do sesji 


# Zainicjalizowanie bazy danych
if 'no_voters' not in db:
    db['no_voters'] = 0  # Liczba głosujących
if 'results' not in db:
    db['results'] = []  # Wyniki głosowania


# Formularz dla klientów
@app.route('/', methods=['GET', 'POST'])
def client_form():
  if request.method == 'POST':
      name = request.form.get('name')
      points = request.form.get('points')

      if name:
          session['name'] = name  # Zapisanie imienia w sesji

      if name and points:
          results = db['results']
          results.append({'name': name, 'points': points})
          db['results'] = results  # Zapisanie wyników w bazie

      return redirect(url_for('client_form'))

  # Tylko GET - pobranie imienia z sesji, jeśli jest
  name_in_session = session.get('name', '')
  return render_template('client_form.html', name=name_in_session)


# Widok do ustawienia liczby uczestników
@app.route('/set_voters', methods=['GET', 'POST'])
def set_voters():
    global no_voters
    if request.method == 'POST':
        no_voters = int(request.form.get('no_voters'))
        db['no_voters'] = no_voters  # Zapisanie liczby uczestników w bazie
    return render_template('set_voters.html', no_voters=db['no_voters'])


# Widok do zbierania wyników
@app.route('/results', methods=['GET'])
def results_view():
    no_voters = db['no_voters']  # Liczba uczestników
    results = db['results']  # Wyniki głosowania

    # Sprawdzanie, czy wszyscy zagłosowali
    all_votes_in = len(results) >= no_voters and no_voters > 0
    return render_template('results.html', results=results if all_votes_in else None, no_voters=no_voters)


# Endpoint tylko do pobierania wyników 
@app.route('/get_results', methods=['GET'])
def get_results():
    no_voters = db.get('no_voters', 0)  # Wymagana liczba głosów
    results = db.get('results', [])  # Wyniki głosowania

    # Konwersja ObservedList i ObservedDict na standardowe listy i słowniki
    normalized_results = [dict(result) for result in results]

    votes = len(normalized_results)  # Aktualna liczba głosów

    return jsonify({
        'no_voters': no_voters,
        'votes': votes,
        'results': normalized_results
    })
    

# Endpoint do resetowania wyników
@app.route('/reset', methods=['POST'])
def reset():
    db['results'] = []
    return redirect(url_for('results_view'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)