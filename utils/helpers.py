"""
Fonctions utilitaires pour Fruit Slicer
"""

import json
import os

def sauvegarder_score(score, fichier="data/scores.json"):
    """
    Sauvegarde le score dans un fichier JSON
    
    Args:
        score (int): Le score à sauvegarder
        fichier (str): Chemin du fichier
    
    Returns:
        bool: True si réussi, False sinon
    """
    try:
        # Créer le dossier data s'il n'existe pas
        dossier = os.path.dirname(fichier)
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        
        # Charger les scores existants
        if os.path.exists(fichier):
            with open(fichier, 'r', encoding='utf-8') as f:
                scores = json.load(f)
        else:
            # Créer nouvelle structure
            scores = {
                "meilleur_score": 0,
                "historique": []
            }
        
        # Ajouter le nouveau score
        scores["historique"].append(score)
        
        # Mettre à jour le meilleur score
        if score > scores["meilleur_score"]:
            scores["meilleur_score"] = score
            print(f"🎉 NOUVEAU RECORD! Score: {score}")
        
        # Garder seulement les 10 derniers scores
        if len(scores["historique"]) > 10:
            scores["historique"] = scores["historique"][-10:]
        
        # Sauvegarder
        with open(fichier, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Score sauvegardé: {score}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

#Lit le meilleur score depuis le fichier, retourne 0 si pas de fichier
def charger_meilleur_score(fichier="data/scores.json"):
    """
    Charge le meilleur score
    
    Args:
        fichier (str): Chemin du fichier
    
    Returns:
        int: Le meilleur score, ou 0 si aucun
    """
    try:
        if os.path.exists(fichier):
            with open(fichier, 'r', encoding='utf-8') as f:
                scores = json.load(f)
            return scores.get("meilleur_score", 0)
        else:
            return 0
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 0

#Affiche du texte centré sur l'écran, Utilisé pour "GAME OVER", etc
def afficher_texte_centre(surface, texte, police, couleur, y):
    """
    Affiche un texte centré horizontalement
    
    Args:
        surface: Surface Pygame
        texte (str): Texte à afficher
        police: Police Pygame
        couleur (tuple): Couleur RGB
        y (int): Position verticale
    """
    texte_surface = police.render(texte, True, couleur)
    texte_rect = texte_surface.get_rect()
    texte_rect.centerx = surface.get_width() // 2  # Centre horizontal
    texte_rect.y = y
    surface.blit(texte_surface, texte_rect)
#Affiche du texte à une position précise,utilisé pour le score, les strikes, etc.

def afficher_texte(surface, texte, police, couleur, x, y):
    """
    Affiche un texte à une position donnée
    
    Args:
        surface: Surface Pygame
        texte (str): Texte à afficher
        police: Police Pygame
        couleur (tuple): Couleur RGB
        x (int): Position horizontale
        y (int): Position verticale
    """
    texte_surface = police.render(texte, True, couleur)
    surface.blit(texte_surface, (x, y))