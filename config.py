"""
Configuration du jeu Fruit Slicer
Tous les paramètres du jeu sont ici
"""

# ============================================================================
# FENÊTRE DU JEU
# ============================================================================
LARGEUR_ECRAN = 800      # Largeur en pixels
HAUTEUR_ECRAN = 600      # Hauteur en pixels

# ============================================================================
# COULEURS (Rouge, Vert, Bleu)
# ============================================================================
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)       # Pour les bombes
VERT = (0, 255, 0)        # Pour les fruits
BLEU = (0, 100, 255)      # Pour les glaçons
JAUNE = (255, 255, 0)
ORANGE = (255, 165, 0)
GRIS = (128, 128, 128)

# ============================================================================
# VITESSE DU JEU
# ============================================================================
FPS = 60                  # Images par seconde (60 = fluide)
MAX_STRIKES = 3           # 3 fruits ratés = Game Over
VITESSE_FRUIT_MIN = 1     # Vitesse minimum de chute
VITESSE_FRUIT_MAX = 3     # Vitesse maximum de chute

# ============================================================================
# FRÉQUENCE D'APPARITION (en frames)
# 60 frames = 1 seconde
# ============================================================================
FREQUENCE_FRUIT = 60      # 1 fruit toutes les 1 seconde
FREQUENCE_BOMBE = 300     # 1 bombe toutes les 5 secondes
FREQUENCE_GLACON = 180    # 1 glaçon toutes les 3 secondes

# ============================================================================
# EFFETS SPÉCIAUX
# ============================================================================
DUREE_RALENTISSEMENT = 3  # Durée du ralentissement (secondes)

# ============================================================================
# MOTS DU JEU (ce que le joueur doit taper)
# ============================================================================
MOTS_FRUITS = [
    # Fruits simples
    "pomme", "poire", "kiwi", "melon", "prune",
    "banane", "orange", "fraise", "raisin", "cerise",
    "peche", "citron", "mangue", "ananas",
    
    # Fruits plus difficiles
    "abricot", "framboise", "myrtille", "pasteque"
]

# ============================================================================
# TEXTES DE L'INTERFACE
# ============================================================================
TITRE_JEU = "FRUIT SLICER"
TEXTE_GAME_OVER = "GAME OVER"
TEXTE_SCORE = "Score: "
TEXTE_STRIKES = "Strikes: "
TEXTE_RALENTI = "RALENTI!"
TEXTE_REJOUER = "Appuyez sur ESPACE pour rejouer"
TEXTE_INPUT = "Tapez: "