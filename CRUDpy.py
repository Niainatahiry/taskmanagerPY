from flask import Flask, render_template, request, redirect
import mysql.connector
import base64
from config import db
app = Flask(__name__)

db_host, db_username, db_password, db_name = db()
@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Récupérer les données du formulaire
    name = request.form['name']
    email = request.form['email']
    adresse = request.form['adresse']
    image = request.files['image']

    # Vérifier si un fichier a été sélectionné
    if image.filename == '':
        return "Aucun fichier sélectionné."

    # Convertir l'image en base64
    image_data = image.read()
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # Établir une connexion avec la base de données
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        database=db_name
    )

    # Insérer les données dans la base de données
    cursor = mydb.cursor()
    sql = "INSERT INTO user (name, email, adresse, image) VALUES (%s, %s, %s, %s)"
    val = (name, email, adresse, image_base64)
    cursor.execute(sql, val)
    mydb.commit()

    # Fermer la connexion à la base de données
    mydb.close()

    return redirect('/result')

@app.route('/result')
def result():
    # Établir une connexion avec la base de données
    mydb = mysql.connector.connect(
        host=db_host,
        user=db_username,
        password=db_password,
        database=db_name
    )

    # Récupérer les données depuis la base de données
    cursor = mydb.cursor()
    sql = "SELECT * FROM user"
    cursor.execute(sql)
    data = cursor.fetchall()

    # Fermer la connexion à la base de données
    mydb.close()

    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run()
