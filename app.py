from flask import Flask, request, jsonify, render_template, abort
import sqlite3

app = Flask(__name__)

# Funzione per connettersi al database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Inizializzazione del database e creazione della tabella se non esiste
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS prenotazioni (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nominativo TEXT NOT NULL,
            numero_posti INTEGER NOT NULL,
            data TEXT NOT NULL,
            ora TEXT NOT NULL,
            contatto TEXT NOT NULL,
            fonte TEXT NOT NULL DEFAULT 'form'
        )
    ''')
    conn.commit()
    conn.close()

# Funzione per svuotare le tabelle
def svuota_tabelle():
    conn = get_db_connection()
    conn.execute('DELETE FROM prenotazioni')
    conn.commit()
    conn.close()

# Funzione per validare i dati della prenotazione
def valida_dati(nominativo, numero_posti, data, ora, contatto):
    if not nominativo or not isinstance(nominativo, str) or len(nominativo) < 3:
        abort(400, description="Nominativo non valido. Deve essere almeno di 3 caratteri.")
    if not numero_posti.isdigit() or int(numero_posti) <= 0:
        abort(400, description="Numero posti non valido. Deve essere un numero positivo.")
    if not data or len(data) != 10:  # Formato previsto: YYYY-MM-DD
        abort(400, description="Data non valida. Usa il formato YYYY-MM-DD.")
    if not ora or len(ora) != 5:  # Formato previsto: HH:MM
        abort(400, description="Ora non valida. Usa il formato HH:MM.")
    if not contatto or len(contatto) < 5:
        abort(400, description="Contatto non valido. Deve essere almeno di 5 caratteri.")

# Gestione degli errori globali
@app.errorhandler(400)
def handle_400_error(error):
    return jsonify({'message': str(error.description)}), 400

@app.errorhandler(500)
def handle_500_error(error):
    return jsonify({'message': 'Errore interno del server.'}), 500

# Rotta per ottenere tutte le prenotazioni fatte tramite il form
@app.route('/api/prenotazioni', methods=['GET'])
def get_prenotazioni():
    conn = get_db_connection()
    prenotazioni = conn.execute('SELECT * FROM prenotazioni WHERE fonte = "form"').fetchall()
    conn.close()
    return jsonify([dict(row) for row in prenotazioni])

# Rotta per creare una nuova prenotazione
@app.route('/prenotazione', methods=['POST'])
def create_prenotazione():
    # Recupera i dati dal form o JSON
    nominativo = request.form.get('nominativo') or request.json.get('nominativo')
    numero_posti = request.form.get('numeroPosti') or request.json.get('numeroPosti')
    data = request.form.get('data') or request.json.get('data')
    ora = request.form.get('ora') or request.json.get('ora')
    contatto = request.form.get('contatto') or request.json.get('contatto')

    # Valida i dati
    valida_dati(nominativo, numero_posti, data, ora, contatto)

    try:
        # Inserisce la prenotazione nel database
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO prenotazioni (nominativo, numero_posti, data, ora, contatto, fonte) VALUES (?, ?, ?, ?, ?, ?)',
            (nominativo, numero_posti, data, ora, contatto, 'form')
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Prenotazione creata con successo!'}), 201
    except Exception as e:
        abort(500, description=f'Errore durante la prenotazione: {str(e)}')

# Rotta per cancellare una prenotazione
@app.route('/prenotazione/<int:id>', methods=['DELETE'])
def delete_prenotazione(id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM prenotazioni WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Prenotazione eliminata con successo!'})
    except Exception as e:
        abort(500, description=f'Errore durante l\'eliminazione: {str(e)}')

# Rotta per svuotare le tabelle
@app.route('/svuota_tabelle', methods=['POST'])
def svuota():
    try:
        svuota_tabelle()
        return jsonify({'message': 'Tabelle svuotate con successo!'}), 200
    except Exception as e:
        abort(500, description=f'Errore durante lo svuotamento delle tabelle: {str(e)}')

# Rotta per servire l'index.html
@app.route('/')
def home():
    return render_template('index.html')

# Rotta per servire lista-prenotazioni.html
@app.route('/lista-prenotazioni')
def lista_prenotazioni():
    conn = get_db_connection()
    prenotazioni = conn.execute('SELECT * FROM prenotazioni WHERE fonte = "form"').fetchall()
    conn.close()
    return render_template('lista-prenotazioni.html', prenotazioni=prenotazioni)

# Inizializza il database al primo avvio
with app.app_context():
    init_db()

# Esegui l'applicazione
if __name__ == '__main__':
    app.run(debug=True)
