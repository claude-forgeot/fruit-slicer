import random
import time
import os
import pygame 

# liste de fruits (chaque fruit est un petit dictionnaire)
# On y met le nom, le symbole et la touche à taper
modeles_fruits = [
    {"nom": "Pomme", "symbole": "🍎", "touche": "p"},
    {"nom": "Banane", "symbole": "🍌", "touche": "b"},
    {"nom": "Orange", "symbole": "🍊", "touche": "o"},
    {"nom": "Bombe", "symbole": "💣", "touche": "x"}, 
    {"nom": "Glaçon", "symbole": "❄️", "touche": "g"}
]

print("BIENVENUE DANS FRUIT TYPER")
print("Appuyez sur Ctrl+C pour arrêter.")
time.sleep(2)

try:
    while True:
        
        fruit_choisi = random.choice(modeles_fruits)
        
        #Créer un décalage aléatoire (pour l'aspect visuel)
        espaces = " " * random.randint(0, 30)
        
        # Afficher le fruit
        print(f"{espaces}{fruit_choisi['symbole']}  (Tapez '{fruit_choisi['touche']}')")
        
        # Attendre un peu avant le prochain fruit
        # Plus le temps est court, plus c'est difficile !
        time.sleep(1.0) 

except KeyboardInterrupt:
    print("\nPartie terminée")