from flask import Flask, render_template, request, redirect, session
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = 'invites.xlsx'
UN_ADMIN = 'admin'
PWD_ADMIN = 'admin1'
app.config['SECRET_KEY'] = 'aekWWFrq98c342y59nc2345!@9c812n3q40)cr2q3yri9fh'  # Remplace avec une clé unique et secrète

# Crée le fichier Excel s'il n'existe pas
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Nom", "Nombre d'invités", "Timestamp"])
    df.to_excel(EXCEL_FILE, index=False)


# Vérifie si l'utilisateur est connecté
def is_logged_in():
    return 'logged_in' in session and session['logged_in']


# Déconnecter l'utilisateur
@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Supprime la session de connexion
    return redirect('/login')


# Page de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect('/admin')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérification simple des identifiants
        if username == UN_ADMIN and password == PWD_ADMIN:
            session['logged_in'] = True  # Enregistrer la session comme connectée
            return redirect('/admin')
        else:
            return render_template('login.html', error="שם משתמש או סיסמא לא נכונה.")

    return render_template('login.html')


@app.route('/admin')
def admin():
    if not is_logged_in():
        return redirect('/login')

    df = pd.read_excel(EXCEL_FILE)
    invites = df.to_dict(orient='records')
    return render_template('admin.html', invites=invites)


@app.route('/', methods=['GET', 'POST'])
def index_hebrew():
    if request.method == 'POST':
        nom = request.form.get('nom')
        nb_invites = request.form.get('nb_invites')

        if nom and nb_invites:
            df = pd.read_excel(EXCEL_FILE)
            df.loc[len(df.index)] = [nom, nb_invites, datetime.now().strftime("%d/%m %H:%M")]
            df.to_excel(EXCEL_FILE, index=False)

        return redirect('/')

    return render_template('index_hebrew.html')


@app.route('/french', methods=['GET', 'POST'])
def index_french():
    if request.method == 'POST':
        nom = request.form.get('nom')
        nb_invites = request.form.get('nb_invites')

        if nom and nb_invites:
            df = pd.read_excel(EXCEL_FILE)
            df.loc[len(df.index)] = [nom, nb_invites, datetime.now().strftime("%d/%m %H:%M")]
            df.to_excel(EXCEL_FILE, index=False)

        return redirect('/french')

    return render_template('index_french.html')


if __name__ == '__main__':
    #app.run(host='127.0.0.1', port=5000, debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
