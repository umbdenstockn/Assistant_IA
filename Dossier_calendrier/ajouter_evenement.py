
from inter_calend import ajouter_evenement

## fonction pour ajouter un événement dans le calendrier de l'utilisateur

date = input("Entrez la date de l'événement (YYYY-MM-DD) : ")
heure = input("Entrez l'heure de l'événement (HH:MM:SS) : ")
description = input("Entrez la description de l'événement : ")
delate = input("Entrez si vous souhaitez supprimer automatiquement l'événement après sa date (1 pour oui, 0 pour non) : ")
if delate not in ['0', '1']:
    print("Option invalide pour delate. La valeur par défaut (1) sera utilisée.")
    delate = '1'
ajouter_evenement(date, heure, description, int(delate))
print("Événement ajouté avec succès !")
