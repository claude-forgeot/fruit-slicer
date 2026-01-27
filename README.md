## Structure du projet

- assets/ : ressources (images, sons, polices)
  - images/ : images des fruits, bombes, background
  - sounds/ : bruitages + musique
  - fonts/  : polices

- data/ : données du jeu
  - scores.json : sauvegarde des scores

- utils/ : fonctions utilitaires
  - __init__.py : permet d'utiliser utils comme package Python
  - helpers.py  : fonctions d'aide (lecture/écriture scores, etc.)

- config.py : constantes (taille écran, vitesse, difficulté)
- game.py : logique principale (boucle du jeu)
- main.py : point d’entrée (lance le jeu)
- requirements.txt : dépendances (pygame)
