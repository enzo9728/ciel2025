from flask import Flask, request, jsonify
import mysql.connector
import re
from mysql.connector import errors

class DatabaseConnectionError(Exception):
    """Erreur personnalisée pour les problèmes de connexion à la base de données."""
    pass
def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",  # Adresse de la base de données
            user="root",
            password="",
            database="ciel2025"
        )
        print("Connexion réussie à la base de données.")
        return mydb
    except mysql.connector.errors.InterfaceError as e:
        raise DatabaseConnectionError(
            "Erreur: Impossible de se connecter au serveur MySQL. "
            "Vérifiez que le serveur est accessible et que les informations de connexion sont correctes."
        ) from e
    except errors.InterfaceError as e:
        print(f"Erreur de connexion : {e}")
        print(f"Connexion interrompue. Assurez-vous que le serveur MySQL est actif et accessible.")
    except errors.OperationalError as e:
        print(f"Erreur opérationelle : {e}")
        print(f"Le serveur MySQL semble injoignable. Vérifiez la connexion réseau.")
    except Exception as e:
        raise DatabaseConnectionError(
            f"Erreur inattendue lors de la connexion à la base de données : {e}"
            ) from e

class DatabaseDisconnectionError(Exception):
    """Erreur personnalisée pour la déconnexion de la base de données."""
    pass
def check_database_connection():
    try:
        if not mydb.is_connected():
            raise DatabaseDisconnectionError(
                "Erreur: La connexion à la base de données a été perdue."
            )
        else:
            print("Connexion à la base de données toujours active.")
    except mysql.connector.errors.OperationalError as e:
        raise DatabaseDisconnectionError(
            "Erreur: La connexion à la base de données a été perdue."
        ) from e

class IDInvalide(Exception):
    pass
def idInvalide(idetudiant):
    if not isinstance(idetudiant, int):
        raise IDInvalide("La valeur entrée pour l'id de l'étudiants est invalide.")

class PostError(Exception):
    pass
def Posterror(nom, prenom, email, telephone):
    if not isinstance(nom, str):
        raise PostError("Le nom est invalide !")
    if not isinstance(prenom, str):
        raise PostError("Le prénom est invalide !")
    if not isinstance(email, str):
        raise PostError("L'email est invalide !")
    if not isinstance(telephone, str):
        raise PostError("Le numéro de téléphone est invalide !")
    
try:
    # Tenter la connexion dès le lancement
    mydb = connect_to_database()
    cursor = mydb.cursor()
except DatabaseConnectionError as e:
    print(str(e))
    exit(1)
except DatabaseDisconnectionError as e:
    print(str(e))
    exit(1)


app = Flask(__name__)

@app.route('/v2/etudiants/', methods=['GET'])
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
    return jsonify(etudiants),201
        
@app.route('/v2/etudiants/<idetudiant>', methods=['GET'])
def getEtudiant(idetudiant):
    try:

        if not idetudiant.isdigit():
            raise IDInvalide("La valeur entrée pour l'id de l'étudiant est invalide.")
        
        idetudiant = int(idetudiant)

        req = "SELECT * FROM etudiant WHERE idetudiant = " + str(idetudiant)
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
        return jsonify(etudiant)
    except IDInvalide as e:
        return jsonify({
            "Erreur": str(e)
        }),400
    except Exception as e:
        return jsonify({
            "Erreur": f"Une erreur s'est produite : {e}"
        }),500

@app.route('/v2/etudiants/', methods=['POST'])
def postEtudiant():
    try:
        # Obtenir les données de la requête JSON
        data = request.get_json()
        nom = data.get("nom")
        prenom = data.get("prenom")
        email = data.get("email")
        telephone = data.get("telephone")

        # Vérification des valeurs
        if not isinstance(nom, str) or not re.match(r'^[A-Za-zÀ-ÿ\-]+$', nom):
            raise PostError("Le nom est invalide !")
        if not isinstance(prenom, str) or not re.match(r'^[A-Za-zÀ-ÿ\-]+$', prenom):
            raise PostError("Le prénom est invalide !")
        if not isinstance(email, str) or " " in email:
            raise PostError("L'email est invalide !")
        if not isinstance(telephone, str) or not re.match(r'^\+?[0-9]+$', telephone):
            raise PostError("Le numéro de téléphone est invalide !")
        
        req = f"INSERT INTO `etudiant` (`nom`, `prenom`, `email`, `telephone`) VALUES ('{nom}', '{prenom}', '{email} ', '{telephone}');"
        cursor.execute(req)
        mydb.commit()
        if cursor.rowcount > 0:
            return jsonify({
                "Message": "L'étudiant a bien été rajouté.",
                "nom": nom,
                "prenom": prenom,
                "email": email,
                "telephone": telephone
            }),201
    except PostError as e:
        return jsonify({
            "Erreur": str(e),
        }),400
    
    except Exception as e:
        return jsonify({
            "Erreur": f"Une erreur s'est produite : {e}"
        }),500
    
@app.route('/v2/etudiants/<idetudiant>', methods=['DELETE'])
def deleteEtudiant(idetudiant):
    try:
        # Valider manuellement si idetudiant est un entier
        if not idetudiant.isdigit():
            raise IDInvalide("La valeur entrée pour l'id de l'étudiant est invalide.")

        idetudiant = int(idetudiant)  # Convertir en entier après validation
        
        # Requête de suppression
        req = f"DELETE FROM etudiant WHERE idetudiant = {idetudiant}"
        cursor.execute(req)
        mydb.commit()
        
        if cursor.rowcount > 0:
            return jsonify({
                "Message": "L'étudiant a bien été supprimé de la base de données.",
            }), 200
        else:
            return jsonify({
                "Message": "L'étudiant avec cet ID n'existe pas.",
                "status": 404
            }), 404
    
    except IDInvalide as e:
        return jsonify({
            "Erreur": str(e),
        }), 400
    
    except Exception as e:
        return jsonify({
            "Erreur": f"Une erreur s'est produite : {str(e)}",
        }), 500

@app.route('/v2/etudiants/<id>', methods=['PUT'])
def updateEtudiant(id):
    try:
        # Valider manuellement si idetudiant est un entier
        if not id.isdigit():
            raise IDInvalide("La valeur entrée pour l'id de l'étudiant est invalide.")

        id = int(id)  # Convertir en entier après validation
        
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
    except IDInvalide as e:
        return jsonify({
            "Erreur": str(e),
        }),400
    
    except Exception as e:
        return jsonify({
            "Erreur": f"Une erreur s'est produite : {e}",
            "status": 500
        }),500

if __name__ == '__main__':
    app.run(debug=True)