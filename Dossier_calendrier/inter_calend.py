
## ici serons stocker l'ensemble des fonctions qui seront utilisées pour interagir avec le calendrier de l'utilisateur


## bibliothèque utilisée dans ce programme

import sqlite3 as sql
import datetime as dt


## fonction pour ajouter un événement dans le calendrier de l'utilisateur

def ajouter_evenement(date, heure, description, delate=1):
    # 1. Connexion à la base
    connexion = sql.connect("calendrier.db")
    curseur = connexion.cursor()

    # 2. Insertion d'un événement
    curseur.execute("INSERT INTO evenements (date, heure, description, delate) VALUES (?, ?, ?, ?)", (date, heure, description, delate))

    # 3. Sauvegarde
    connexion.commit()

    # 4. Fermeture
    connexion.close()



## fonction pour avoir la liste de tous les événements du calendrier de l'utilisateur triés par date et heure sous le format de liste [[id, date, heure, description, delate], [id, date, heure, description, delate], ...]

def trier_evenements():
    # 1. Connexion à la base
    connexion = sql.connect("calendrier.db")
    curseur = connexion.cursor()

    # 2. Récupération et tri des événements
    curseur.execute("SELECT * FROM evenements ORDER BY date ASC, heure ASC")
    evenements_tries = curseur.fetchall()

    # 3. Fermeture
    connexion.close()

    return evenements_tries



## fonction pour supprimer l'ensemble des événements du calendrier de l'utilisateur qui sont passés

def supprimer_evenements_passés():
    # 1. Connexion à la base
    connexion = sql.connect("calendrier.db")
    curseur = connexion.cursor()

    # 2. Suppression des événements passés
    date_actuelle = dt.date.today().isoformat()
    heure_actuelle = dt.datetime.now().time().isoformat(timespec='seconds')
    curseur.execute("DELETE FROM evenements WHERE (date < ? OR (date = ? AND heure < ?)) and (delate = 1)", (date_actuelle, date_actuelle, heure_actuelle))

    # 3. Sauvegarde
    connexion.commit()

    # 4. Fermeture
    connexion.close()





