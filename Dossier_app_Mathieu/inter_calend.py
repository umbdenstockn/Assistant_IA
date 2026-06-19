
## ici serons stocker l'ensemble des fonctions qui seront utilisées pour interagir avec le calendrier de l'utilisateur


## bibliothèque utilisée dans ce programme

import sqlite3 as sql
import datetime as dt


## fonction pour ajouter un événement dans le calendrier de l'utilisateur

def ajouter_evenement(date, heure, duree, description, suppr=1):
    # 1. Connexion à la base
    connexion = sql.connect("calendrier_base_de_donnee_NE_PAS_TOUCHER.db")
    curseur = connexion.cursor()

    # 2. Insertion d'un événement
    curseur.execute("INSERT INTO evenements (date, heure, duree, description, suppr) VALUES (?, ?, ?, ?, ?)", (date, heure, duree, description, suppr))

    # 3. Sauvegarde
    connexion.commit()

    # 4. Fermeture
    connexion.close()


## fonction pour avoir la liste de tous les événements du calendrier de l'utilisateur triés par date et heure sous le format de liste [[id, date, heure, description, delate], [id, date, heure, description, delate], ...]

def trier_evenements():
    # 1. Connexion à la base
    connexion = sql.connect("calendrier_base_de_donnee_NE_PAS_TOUCHER.db")
    curseur = connexion.cursor()

    # 2. Récupération et tri des événements
    curseur.execute("SELECT * FROM evenements  WHERE date >= ? ORDER BY date ASC, heure ASC", (dt.date.today().isoformat(),))
    evenements_tries = curseur.fetchall()
    curseur.execute("SELECT * FROM evenements WHERE date < ? ORDER BY date DESC, heure DESC", (dt.date.today().isoformat(),))
    evenements_tries_passe = curseur.fetchall()

    # 3. Fermeture
    connexion.close()

    return evenements_tries,evenements_tries_passe



## fonction pour supprimer l'ensemble des événements du calendrier de l'utilisateur qui sont passés

def supprimer_evenements_passés():
    # 1. Connexion à la base
    connexion = sql.connect("calendrier_base_de_donnee_NE_PAS_TOUCHER.db")
    curseur = connexion.cursor()

    # 2. Suppression des événements passés
    date_actuelle = dt.date.today().isoformat()
    heure_actuelle = dt.datetime.now().time().isoformat(timespec='seconds')
    curseur.execute("DELETE FROM evenements WHERE (date < ? OR (date = ? AND heure < ?)) and (suppr = 1)", (date_actuelle, date_actuelle, heure_actuelle))

    # 3. Sauvegarde
    connexion.commit()

    # 4. Fermeture
    connexion.close()


# fonction qui supprime les événements grace à leur id

def supprimer_evenement_par_id(id_evenement):
    # 1. Connexion à la base
    connexion = sql.connect("calendrier_base_de_donnee_NE_PAS_TOUCHER.db")
    curseur = connexion.cursor()

    # 2. Suppression de l'événement par ID
    curseur.execute("DELETE FROM evenements WHERE id = ?", (id_evenement,))

    # 3. Sauvegarde
    connexion.commit()

    # 4. Fermeture
    connexion.close()


# fonction qui renvoie une listes des prochains jours fériés

def jours_feries_france(annee):
    # Jours fixes
    jf = {
        dt.date(annee, 1, 1),   # Jour de l'an
        dt.date(annee, 5, 1),   # Fête du travail
        dt.date(annee, 5, 8),   # Victoire 1945
        dt.date(annee, 7, 14),  # Fête nationale
        dt.date(annee, 8, 15),  # Assomption
        dt.date(annee, 11, 1),  # Toussaint
        dt.date(annee, 11, 11), # Armistice
        dt.date(annee, 12, 25), # Noël
    }

    # Calcul de Pâques (algorithme de Meeus)
    a = annee % 19
    b = annee // 100
    c = annee % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    mois = (h + l - 7*m + 114) // 31
    jour = ((h + l - 7*m + 114) % 31) + 1
    paques = dt.date(annee, mois, jour)

    jf.update({
        paques + dt.timedelta(days=1),   # Lundi de Pâques
        paques + dt.timedelta(days=39),  # Ascension
        paques + dt.timedelta(days=50),  # Lundi de Pentecôte
    })

    return jf


# fonction qui ajoute 50 jours à la table jours dans la base de données

def ajouter_50_jours():
    # Connexion
    connexion = sql.connect("calendrier_base_de_donnee_NE_PAS_TOUCHER.db")
    curseur = connexion.cursor()

    # 1. Récupérer la dernière date enregistrée
    curseur.execute("SELECT date FROM jours ORDER BY date DESC LIMIT 1")
    resultat = curseur.fetchone()

    if resultat is None:
        # Si la table est vide, on commence aujourd'hui
        derniere_date = dt.date.today()
    else:
        derniere_date = dt.datetime.strptime(resultat[0], "%Y-%m-%d")

    # 2. Liste des jours de la semaine
    jours_semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


    # 3. Ajouter les 50 jours suivants
    for i in range(1, 51):
        nouvelle_date = derniere_date + dt.timedelta(days=i)
        jour_nom = jours_semaine[nouvelle_date.weekday()]
        date_str = nouvelle_date.strftime("%Y-%m-%d")

        # 4. Vérification si la date est un jour férié ou un week-end
        est_weekend = nouvelle_date.weekday() >= 5
        jf = jours_feries_france(nouvelle_date.year)

        curseur.execute(
            "INSERT OR IGNORE INTO jours (date, jour, férier) VALUES (?, ?, ?)",
            (date_str, jour_nom, "oui" if est_weekend or nouvelle_date in jf else "non")
        )

    # 5. Sauvegarde
    connexion.commit()
    connexion.close()



# fonction qui permet de récuperer les évènement sur les 7 prochains jour à partir de aujourd'hui

def recup_sept():

    # récupération de la date du jour et de celle qui sera 6 jour plus tard (total 7 jours = 1 semaine)
    date_ajd = dt.date.today()
    date_7_jour = dt.date.today() + dt.timedelta(days=6)
    
    # 1. Connexion à la base
    connexion = sql.connect("calendrier_base_de_donnee_NE_PAS_TOUCHER.db")
    curseur = connexion.cursor()

    # 2. Récupération et tri des événements
    curseur.execute("SELECT * FROM evenements  WHERE date >= ? AND date <= ? ORDER BY date ASC, heure ASC", (date_ajd,date_7_jour,))
    evenements_tries = curseur.fetchall()

    # 3. Fermeture
    connexion.close()

    return evenements_tries

