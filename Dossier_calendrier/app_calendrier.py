
## ce code sera la partie du code de l'app qui va gérer le calendrier de l'utilisateur.

## bibliothèque utilisée dans ce programme

import sqlite3 as sql
import datetime as dt
import inter_calend as ic
import tkinter as tk
from tkinter import ttk

## code global de l'application du calendrier

app = tk.Tk()
app.title("Calendrier de l'utilisateur")
app.state("zoomed")



### regarder de bas en haut en partant du menu, le code est organisé en 3 parties :
### 1. la page d'accueil du calendrier de l'utilisateur
### 1. la page d'ajout d'événements 
### 2. la page de visualisation des événements
### 3. les fonctions pour naviguer entre les pages
### 4. la barre de menu pour naviguer entre les deux pages

## page d'accueil du calendrier de l'utilisateur
page_accueil = tk.Frame(app)
label_accueil = tk.Label(page_accueil, text="Bienvenue dans le calendrier de l'utilisateur !", font=("Helvetica", 30))
label_accueil.pack(pady=20)


## page afficher lors du choix du menu "tableau des événements"
page_regarder_evenements = tk.Frame(app)



## Fonction pour le menu "accueil"
def aller_accueil():
    page_accueil.pack(fill="both", expand=True)
    page_regarder_evenements.pack_forget()


# Fonction pour le menu "tableau des événements"
def regarder_evenements():
    page_regarder_evenements.pack(fill="both", expand=True)
    page_accueil.pack_forget()

    # --- Nettoyage de la page avant d'afficher le tableau ---
    for widget in page_regarder_evenements.winfo_children():
        widget.destroy()

    # --- Création du tableau ---
    colonnes = ("id", "date", "heure", "description", "delate")
    tableau_regarder_evenements = ttk.Treeview(page_regarder_evenements, columns=colonnes, show="headings")
    

    # --- Titres des colonnes ---
    tableau_regarder_evenements.heading("id", text="ID")
    tableau_regarder_evenements.heading("date", text="Date")
    tableau_regarder_evenements.heading("heure", text="Heure")
    tableau_regarder_evenements.heading("description", text="Description")
    tableau_regarder_evenements.heading("delate", text="Suppression auto après la date (1 pour oui, 0 pour non)")

    # --- Largeur des colonnes ---
    tableau_regarder_evenements.column("id", width=5)
    tableau_regarder_evenements.column("date", width=10)
    tableau_regarder_evenements.column("heure", width=10)
    tableau_regarder_evenements.column("description", width=200)
    tableau_regarder_evenements.column("delate", width=150)

    # --- Ajout de données ---
    donnees_futures, donnees_passe = ic.trier_evenements()

    for ligne in donnees_futures:
        tableau_regarder_evenements.insert("", tk.END, values=ligne)
    
    if len(donnees_passe) > 0:  # Vérifie s'il y a des événements passés
        tableau_regarder_evenements.insert("", tk.END, values=("", "", "", "", ""))  # Ligne de séparation
        tableau_regarder_evenements.insert("", tk.END, values=("", "Événements passés :", "", "", ""))  # Ligne de séparation

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
        regarder_evenements()  
    
    supprimer_bouton = tk.Button(supp_id_frame, text="Supprimer l'événement", command=supprimer_evenement_selectionne)
    supprimer_bouton.pack(pady=10)

    supp_id_frame.grid(row=0, column=1, padx=20, pady=20, sticky="e")



    ## frame pour la suppression d'événements passés

    supp_passes_frame = tk.Frame(gerer_evenements_Frame)

    def supprimer_evenements_passes():
        ic.supprimer_evenements_passés()
        regarder_evenements()

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
        description = description_entree.get()
        description_entree.delete(0, tk.END)  # Efface le champ après récupération
        delate = delate_entree.get()
        delate_entree.delete(0, tk.END)  # Efface le champ après récupération

        if delate not in ['0', '1']:
            delate = '1'

        ic.ajouter_evenement(date, heure, description, int(delate))
        regarder_evenements()  # Rafraîchit la page pour afficher le nouvel événement
        


    enregistrer_bouton = tk.Button(ajout_evenement_frame, text="Enregistrer l'événement", command=enregistrer_evenement)
    enregistrer_bouton.pack(pady=10)

    ajout_evenement_frame.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="w")

    gerer_evenements_Frame.pack(pady=20, padx=20)





# Barre de navigation 
nav_bar = tk.Frame(app, bg="#dddddd")
nav_bar.pack(fill="x")

btn_accueil = tk.Button(nav_bar, text="Accueil", command=aller_accueil)
btn_accueil.pack(side="left", padx=10, pady=10)

btn_tableau = tk.Button(nav_bar, text="Calendrier", command=regarder_evenements)
btn_tableau.pack(side="left", padx=10, pady=10)




## Lancement de l'application
aller_accueil()  # Affiche la page d'accueil par défaut











app.mainloop()