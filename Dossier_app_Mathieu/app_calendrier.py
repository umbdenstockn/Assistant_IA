
## ce code sera la partie du code de l'app qui va gérer le calendrier de l'utilisateur.

## bibliothèque utilisée dans ce programme

import sqlite3 as sql
import datetime as dt
import inter_calend as ic
import tkinter as tk
from tkinter import ttk
import requests




## code global de l'application du calendrier

app = tk.Tk()

app.title("Calendrier de l'utilisateur")
app.state("zoomed")
### app.attributes("-fullscreen", True) 
# pour mettre en fullscreen (sans bouton de fermeture "croix rouge", sans barre de navigation "en bas")


### regarder de bas en haut en partant du menu, le code est organisé en 3 parties :

### 1. la créations des différentes pages.
### 2. les fonctions utile au fonctionnement des pages et qui sont acceder grace aux boutons du menu.
### 3. la barre de menu pour naviguer entre les deux pages avec les boutons.

## page d'accueil du calendrier de l'utilisateur
page_accueil = tk.Frame(app)

## page afficher lors du choix du menu "tableau des événements"
page_regarder_evenements = tk.Frame(app)

## page afficher lors du choix du menu "meteo"
page_regarder_meteo = tk.Frame(app)

        ## données pour la partie meteo


url = url = "https://api.open-meteo.com/v1/forecast?latitude=48.5734&longitude=7.7521&daily=temperature_2m_max,temperature_2m_min,rain_sum,windspeed_10m_max,weathercode&timezone=Europe/Paris&forecast_days=10"
response = requests.get(url)
data = response.json() 

daily = data["daily"]
dates = daily["time"]
temp_max = daily["temperature_2m_max"]
temp_min = daily["temperature_2m_min"]
pluie = daily["rain_sum"]
vent = daily["windspeed_10m_max"]
wethercode = daily["weathercode"]

codes_meteo = {
    0: "Ciel dégagé",

    1: "Principalement dégagé",
    2: "Partiellement nuageux",
    3: "Couvert",

    45: "Brouillard",
    48: "Brouillard givrant",

    51: "Bruine légère",
    53: "Bruine modérée",
    55: "Bruine dense",

    56: "Bruine verglaçante légère",
    57: "Bruine verglaçante dense",

    61: "Pluie faible",
    63: "Pluie modérée",
    65: "Pluie forte",

    66: "Pluie verglaçante légère",
    67: "Pluie verglaçante forte",

    71: "Chute de neige légère",
    73: "Chute de neige modérée",
    75: "Chute de neige forte",

    77: "Grains de neige",

    80: "Averses de pluie légères",
    81: "Averses de pluie modérées",
    82: "Averses de pluie violentes",

    85: "Averses de neige légères",
    86: "Averses de neige fortes",

    95: "Orage",

    96: "Orage avec grêle légère",
    99: "Orage avec forte grêle"
    }





## fonction util au bouton

## fonction qui cache toutes les pages
def cache_page():
    page_accueil.pack_forget()
    page_regarder_evenements.pack_forget()
    page_regarder_meteo.pack_forget()

## fonction qui nous emmene à l'accueil.
def aller_accueil():
    cache_page()

    for widget in page_accueil.winfo_children():
        widget.destroy()

    label_accueil = tk.Label(page_accueil, text="Bienvenue dans le futur assistant personnel !", font=("Helvetica", 30))
    label_accueil.pack(pady=20)

    page_accueil.pack()

## fonction qui nous emmene à la page à la page qui gère les événements.
def aller_evenements():

    cache_page()

    page_regarder_evenements.pack(fill="both", expand=True)

    # --- Nettoyage de la page avant d'afficher le tableau ---
    for widget in page_regarder_evenements.winfo_children():
        widget.destroy()

    # --- Création du tableau ---
    colonnes = ("id", "date", "heure", "duree", "description", "suppr")
    tableau_regarder_evenements = ttk.Treeview(page_regarder_evenements, columns=colonnes, show="headings")
    

    # --- Titres des colonnes ---
    tableau_regarder_evenements.heading("id", text="ID")
    tableau_regarder_evenements.heading("date", text="Date")
    tableau_regarder_evenements.heading("heure", text="Heure")
    tableau_regarder_evenements.heading("duree", text="durée")
    tableau_regarder_evenements.heading("description", text="Description")
    tableau_regarder_evenements.heading("suppr", text="Suppression auto après la date (1 pour oui, 0 pour non)")

    # --- Largeur des colonnes ---
    tableau_regarder_evenements.column("id", width=5)
    tableau_regarder_evenements.column("date", width=10)
    tableau_regarder_evenements.column("heure", width=10)
    tableau_regarder_evenements.column("duree",width=10)
    tableau_regarder_evenements.column("description", width=200)
    tableau_regarder_evenements.column("suppr", width=150)

    # --- Ajout de données ---
    donnees_futures, donnees_passe = ic.trier_evenements()

    for ligne in donnees_futures:
        tableau_regarder_evenements.insert("", tk.END, values=ligne)
    
    if len(donnees_passe) > 0:  # Vérifie s'il y a des événements passés
        tableau_regarder_evenements.insert("", tk.END, values=("", "", "", "", "", ""))  # Ligne de séparation
        tableau_regarder_evenements.insert("", tk.END, values=("", "Événements passés :", "", "", "", ""))  # Ligne de séparation

        for ligne in donnees_passe:
            tableau_regarder_evenements.insert("", tk.END, values=ligne)
    
   

    # --- Placement ---
    tableau_regarder_evenements.pack(pady=30, padx=30, fill="x")
    



    gerer_evenements_Frame = tk.Frame(page_regarder_evenements)

    gerer_evenements_Frame.columnconfigure(0, weight=1)
    gerer_evenements_Frame.columnconfigure(1, weight=1)



    ## frame pour la suppression d'événements par ID
    supp_id_frame = tk.Frame(gerer_evenements_Frame)
    

    id_label = tk.Label(supp_id_frame, text="Entrez l'ID de l'événement à supprimer :")
    id_label.pack(pady=5)

    id_entree = tk.Entry(supp_id_frame, justify="center", width=10)
    id_entree.pack(pady=5)

    def supprimer_evenement_selectionne():
        id_evenement = id_entree.get()
        id_entree.delete(0, tk.END) 
        ic.supprimer_evenement_par_id(id_evenement)
        aller_evenements()  
    
    supprimer_bouton = tk.Button(supp_id_frame, text="Supprimer l'événement", command=supprimer_evenement_selectionne)
    supprimer_bouton.pack(pady=10)

    supp_id_frame.grid(row=0, column=1, padx=20, pady=20, sticky="e")



    ## frame pour la suppression d'événements passés

    supp_passes_frame = tk.Frame(gerer_evenements_Frame)

    def supprimer_evenements_passes():
        ic.supprimer_evenements_passés()
        aller_evenements()

    supprimer_passes_bouton = tk.Button(supp_passes_frame, text="Supprimer les événements passés", command=supprimer_evenements_passes)
    supprimer_passes_bouton.pack(pady=10)

    supp_passes_frame.grid(row=1, column=1, padx=20, pady=20, sticky="e")




    ## Frame pour l'ajout d'événements
    ajout_evenement_frame = tk.Frame(gerer_evenements_Frame)
    explication_ajout_evenement = tk.Label(ajout_evenement_frame, text="Pour ajouter un événement, veuillez remplir les champs ci-dessous :")
    explication_ajout_evenement.pack(pady=5)

    date_frame = tk.Frame(ajout_evenement_frame)
    date_label = tk.Label(date_frame, text="Date (YYYY-MM-DD) :")
    date_label.pack()
    date_entree = tk.Entry(date_frame, justify="center", width=14)
    date_entree.pack()
    date_frame.pack(pady=5, padx=5)

    heure_frame = tk.Frame(ajout_evenement_frame)
    heure_label = tk.Label(heure_frame, text="Heure (HH:MM:SS) :")
    heure_label.pack()
    heure_entree = tk.Entry(heure_frame, justify="center", width=12)
    heure_entree.pack()
    heure_frame.pack(pady=5, padx=5)

    duree_frame = tk.Frame(ajout_evenement_frame)
    duree_label = tk.Label(duree_frame,text="duree (HH:MM:SS) :")
    duree_label.pack()
    duree_entree = tk.Entry(duree_frame, justify="center", width=12)
    duree_entree.pack()
    duree_frame.pack(pady=5, padx=5)

    description_frame = tk.Frame(ajout_evenement_frame)
    description_label = tk.Label(description_frame, text="Description :")
    description_label.pack()
    description_entree = tk.Entry(description_frame, justify="center", width=50)
    description_entree.pack()
    description_frame.pack(pady=5, padx=5)

    delate_frame = tk.Frame(ajout_evenement_frame)
    delate_label = tk.Label(delate_frame, text="Supprimer automatiquement après la date (1 pour oui, 0 pour non, par défaut ce sera 1) :")
    delate_label.pack()
    delate_entree = tk.Entry(delate_frame, justify="center", width=3)
    delate_entree.pack()
    delate_frame.pack(pady=5, padx=5)

    def enregistrer_evenement():
        date = date_entree.get()
        date_entree.delete(0, tk.END)  # Efface le champ après récupération
        heure = heure_entree.get()
        heure_entree.delete(0, tk.END)  # Efface le champ après récupération
        duree = duree_entree.get()
        duree_entree.delete(0, tk.END)  # Efface le champ après récupération
        description = description_entree.get()
        description_entree.delete(0, tk.END)  # Efface le champ après récupération
        delate = delate_entree.get()
        delate_entree.delete(0, tk.END)  # Efface le champ après récupération

        if delate not in ['0', '1']:
            delate = '1'

        ic.ajouter_evenement(date, heure, duree, description, int(delate))
        aller_evenements()  # Rafraîchit la page pour afficher le nouvel événement
        


    enregistrer_bouton = tk.Button(ajout_evenement_frame, text="Enregistrer l'événement", command=enregistrer_evenement)
    enregistrer_bouton.pack(pady=10)

    ajout_evenement_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="w")

    gerer_evenements_Frame.pack(pady=20, padx=20)

## fonction qui nous emmene à la page meteo.
def aller_meteo():
    cache_page()
    
    # --- Nettoyage de la page avant d'afficher le tableau ---
    for widget in page_regarder_meteo.winfo_children():
        widget.destroy()

    page_regarder_meteo.pack()

    
    tk.Label(page_regarder_meteo,text="Météo du jour à Strasbourg").pack()
    tk.Label(page_regarder_meteo,text = "Date :" + str(dates[0]) ).pack()
    tk.Label(page_regarder_meteo,text = (codes_meteo.get(wethercode[0], "Code météo inconnu"))).pack()
    tk.Label(page_regarder_meteo,text = "Température max :" + str(temp_max[0]) + "°C").pack()
    tk.Label(page_regarder_meteo, text = "Température min :" + str(temp_min[0]) + "°C").pack()
    tk.Label(page_regarder_meteo,text = "Pluie :" + str(pluie[0]) + "mm").pack()
    tk.Label(page_regarder_meteo,text = "Vent max :" + str(vent[0]) + "km/h").pack()
    tk.Label(page_regarder_meteo, text = "Prévisions sur les 10 prochains jours").pack()
    tk.Label(page_regarder_evenements, text = "Températures sur 10 jours").pack()

## fcontion qui nous fait quitter la page.
def quitter():
    app.destroy()






# Barre de navigation 
nav_bar = tk.Frame(app, bg="#dddddd")
nav_bar.pack(fill="x")

btn_accueil = tk.Button(nav_bar, text="Accueil", command=aller_accueil)
btn_accueil.pack(side="left", padx=10, pady=10)

btn_evenement = tk.Button(nav_bar, text="Calendrier", command=aller_evenements)
btn_evenement.pack(side="left", padx=10, pady=10)

btn_meteo = tk.Button(nav_bar, text="Meteo", command=aller_meteo)
btn_meteo.pack(side="left", padx=10, pady=10)



btn_quitter = tk.Button(nav_bar, text="Quitter", command=quitter)
btn_quitter.pack(side="right",padx=10, pady=10)




## Lancement de l'application
aller_accueil()  # Affiche la page d'accueil par défaut

app.mainloop()   # démarage du programme (mainloop() est obligatoire pour commencer le programme)