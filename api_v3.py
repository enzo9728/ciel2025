from flask import Flask , jsonify , request
from db import Database

app = Flask(__name__)

db = Database("127.0.0.1", "root", "", "ciel2025")

@app.route('/v3/etudiants/', methods=['GET'])
def getAllEtudiants():
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401

    etudiants = []
    result = db.readAll()
    for row in result:
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4],
            }
        etudiants.append(etudiant)
    
    return jsonify(etudiants), 200

@app.route('/v3/etudiants/<int:id>', methods=['GET'])
def getEtudiants(id):
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401
    try :
        row = db.readOne(id)
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4],
            }
        return jsonify(etudiant), 200
    except TypeError:
        return jsonify({'erreur':'id invalide'}), 404
    

@app.route('/v3/etudiants/', methods=['POST'])
def addEtudiant():
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401
    try:
        nom = request.json['nom']
        prenom = request.json['prenom']
        email = request.json['email']
        telephone = request.json['telephone']
        db.create(nom, prenom, email, telephone)
        if not all([nom, prenom, email, telephone]):
            return jsonify({"erreur": "Tous les champs sont requis."}), 400
        return jsonify({"message": "Étudiant ajouté avec succès."}), 201
    except TypeError:
        return jsonify({"erreur": "Erreur de base de données."}), 500

@app.route('/v3/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    if not db.authorized(request):
        return jsonify({"message": "Accès non autorisé"}), 401
    try :
        data = request.json
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        telephone = data.get('telephone')

        affected_rows = db.update(id, nom, prenom, email, telephone)
        if affected_rows == 0:
            return jsonify({'Erreur': 'Étudiant non trouvé'}), 404
    
        return jsonify({'message': 'Étudiant mis à jour avec succès'}), 200
    
    except TypeError:
        return jsonify({'message': 'Erreur lors de la mise à jour de l\'étudiant'}), 500

@app.route('/v3/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    if not db.authorized(request):
            return jsonify({"message": "Accès non autorisé"}), 401
    try :
        rows_deleted = db.delete(id)
        if rows_deleted == 0:
            return jsonify({'message': 'Étudiant non trouvé'}), 404 

        return jsonify({'message': 'Étudiant supprimé avec succès'}), 200
    
    except TypeError:
        return jsonify({'message': 'Erreur lors de la suppression de l\'étudiant' }), 500

if __name__ == "__main__":
    app.run(host= "0.0.0.0", debug=True)