from flask import Flask, request, jsonify
import mysql.connector

mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    password = "",
    database = "ciel2025"
)

cursor = mydb.cursor()


app = Flask(__name__)

@app.route('/v1/etudiants/', methods=['GET'])
def getEtudiants():
    etudiants = []
    req = "SELECT * FROM etudiant"
    cursor.execute(req)
    result = cursor.fetchall()
    for row in result:
        etudiant = {
            "idetudiants": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
            }
        etudiants.append(etudiant)
    return jsonify(etudiants),200
        
@app.route('/v1/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
    print(req)
    cursor.execute(req)
    row = cursor.fetchone()
    etudiant = {
        "idetudiant": row[0],
        "nom": row[1],
        "prenom": row[2],
        "email": row[3],
        "telephone": row[4]
    }
    return jsonify(etudiant),200

@app.route('/v1/etudiants/', methods=['POST'])
def postEtudiant():
    data = request.get_json()
    nom = data.get("nom")
    prenom = data.get("prenom")
    email = data.get("email")
    telephone = data.get("telephone")
    req = f"INSERT INTO `etudiant` (`nom`, `prenom`, `email`, `telephone`) VALUES ('{nom}', '{prenom}', '{email} ', '{telephone}');"
    cursor.execute(req)
    mydb.commit()
    if cursor.rowcount > 0:
        return jsonify({
            "Message": "L'étudiant a bien été rajouté. 200",
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "telephone": telephone,
        }),201
    else :
        return jsonify({
            "Message": "La création de l'étudiant a échouée. 400"
        })

@app.route('/v1/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    req = f"DELETE FROM etudiant WHERE `etudiant`.`idetudiant` = {id}"
    cursor.execute(req)
    mydb.commit()
    if cursor.rowcount > 0:
        return jsonify({
            "Message": "L'étudiant a bien été supprimé de la base de donnée. 200"
        }),200
    else:
        return jsonify({
            "Message": "La suppression de l'étudiant a échoué. 400"
        }) 


@app.route('/v1/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    data = request.get_json()
    nom = data.get("nom")
    prenom = data.get("prenom")
    email = data.get("email")
    telephone = data.get("telephone")
    
    req = f"UPDATE etudiant SET nom = '{nom}', prenom = '{prenom}', email = '{email}', telephone = '{telephone}' WHERE idetudiant = '{id}'"

    cursor.execute(req)
    mydb.commit()
    
    if cursor.rowcount > 0:
        return jsonify({
            "Message": "Mise à jour réussie.",
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "telephone": telephone
        }),200
    else:
        return jsonify({
            "Message": "La modification de l'étudiant a échouée."
        }),400

if __name__ == '__main__':
    app.run(host = '0.0.0.0' ,debug=True)