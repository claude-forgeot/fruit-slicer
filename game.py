"""
Logique principale du jeu Fruit Slicer
"""

import pygame
import random
from config import *

# ============================================================================
# CLASSE FRUIT - Représente un objet qui tombe
# ============================================================================

class Fruit:
    """Un fruit/bombe/glaçon qui tombe"""
    
    def __init__(self, mot, type_fruit="normal"):
        """
        Initialise un fruit
        
        Args:
            mot (str): Mot à taper
            type_fruit (str): "normal", "bombe", ou "glacon"
        """
        self.mot = mot
        self.type_fruit = type_fruit
        
        # Position aléatoire en X, commence en haut
        self.x = random.randint(50, LARGEUR_ECRAN - 100)
        self.y = -50  # Au-dessus de l'écran
        
        # Vitesse de chute
        if type_fruit == "bombe":
            self.vitesse = random.uniform(0.5, 1.5)  # Bombes plus lentes
        else:
            self.vitesse = random.uniform(VITESSE_FRUIT_MIN, VITESSE_FRUIT_MAX)
        
        self.est_tape = False  # Le joueur a tapé ce fruit?
        
    def tomber(self, multiplicateur_vitesse=1.0):
        """Fait tomber le fruit"""
        self.y += self.vitesse * multiplicateur_vitesse
        
    def dessiner(self, surface, police):
        """Dessine le fruit sur l'écran"""
        # Couleur selon le type
        if self.type_fruit == "bombe":
            couleur = ROUGE
            symbole = "💣 "
        elif self.type_fruit == "glacon":
            couleur = BLEU
            symbole = "❄️ "
        else:
            couleur = VERT
            symbole = "🍎 "
        
        # Afficher symbole + mot
        texte_complet = f"{symbole}{self.mot}"
        texte_surface = police.render(texte_complet, True, couleur)
        
        # Contour noir pour lisibilité
        texte_contour = police.render(texte_complet, True, NOIR)
        surface.blit(texte_contour, (self.x + 2, self.y + 2))
        surface.blit(texte_surface, (self.x, self.y))
        
    def est_hors_ecran(self):
        """Vérifie si le fruit est sorti de l'écran"""
        return self.y > HAUTEUR_ECRAN


# ============================================================================
# CLASSE PRINCIPALE DU JEU
# ============================================================================

class JeuFruitSlicer:
    """Classe qui gère tout le jeu"""
    
    def __init__(self):
        """Initialise le jeu"""
        print("🎮 Initialisation du jeu...")
        
        # Initialiser Pygame
        pygame.init()
        
        # Créer la fenêtre
        self.ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        pygame.display.set_caption(TITRE_JEU)
        
        # Horloge pour contrôler les FPS
        self.horloge = pygame.time.Clock()
        
        # Polices
        self.police_fruit = pygame.font.Font(None, 40)
        self.police_ui = pygame.font.Font(None, 28)
        self.police_titre = pygame.font.Font(None, 72)
        self.police_input = pygame.font.Font(None, 32)
        
        # Charger le meilleur score
        from utils.helpers import charger_meilleur_score
        self.meilleur_score = charger_meilleur_score()
        
        # Initialiser l'état du jeu
        self.reinitialiser()
        
        print("✅ Jeu initialisé!")
        
    def reinitialiser(self):
        """Réinitialise pour une nouvelle partie"""
        print("\n🔄 Nouvelle partie!")
        
        self.fruits = []  # Liste des fruits sur l'écran
        self.score = 0
        self.strikes = 0
        self.combo = 0
        self.dernier_temps_fruit = 0
        self.texte_tape = ""
        self.game_over = False
        self.compteur_frames = 0
        
        # Ralentissement
        self.temps_ralenti_restant = 0
        self.multiplicateur_vitesse = 1.0
        
        # Statistiques
        self.fruits_attrapes = 0
        self.bombes_evitees = 0
        
    def creer_fruit(self, type_fruit="normal"):
        """Crée un nouveau fruit"""
        # Choisir un mot
        if type_fruit == "bombe":
            mot = "bombe"
        elif type_fruit == "glacon":
            mot = "glace"
        else:
            mot = random.choice(MOTS_FRUITS)
        
        # Créer et ajouter le fruit
        fruit = Fruit(mot, type_fruit)
        self.fruits.append(fruit)
        
    def gerer_evenements(self):
        """Gère les événements (clavier, fermeture)"""
        for event in pygame.event.get():
            # Fermeture de la fenêtre
            if event.type == pygame.QUIT:
                return False
            
            # Événements clavier
            if event.type == pygame.KEYDOWN:
                
                if self.game_over:
                    # En mode Game Over
                    if event.key == pygame.K_SPACE:
                        self.reinitialiser()  # Rejouer
                    elif event.key == pygame.K_ESCAPE:
                        return False  # Quitter
                
                else:
                    # En jeu
                    if event.key == pygame.K_RETURN:
                        self.verifier_mot()  # Valider le mot
                        self.texte_tape = ""
                        
                    elif event.key == pygame.K_BACKSPACE:
                        self.texte_tape = self.texte_tape[:-1]  # Effacer
                        
                    elif event.key == pygame.K_ESCAPE:
                        return False  # Quitter
                        
                    else:
                        # Ajouter le caractère (max 15 caractères)
                        if len(self.texte_tape) < 15:
                            self.texte_tape += event.unicode.lower()
        
        return True
    
    def verifier_mot(self):
        """Vérifie si le mot tapé correspond à un fruit"""
        if not self.texte_tape:
            return
        
        # Parcourir tous les fruits
        for fruit in self.fruits:
            if fruit.mot == self.texte_tape and not fruit.est_tape:
                fruit.est_tape = True
                
                # Action selon le type
                if fruit.type_fruit == "normal":
                    self.gerer_fruit_normal()
                    
                elif fruit.type_fruit == "bombe":
                    print("💥 BOOM! Bombe touchée!")
                    self.game_over = True
                    
                elif fruit.type_fruit == "glacon":
                    self.activer_ralentissement()
                
                break
    
    def gerer_fruit_normal(self):
        """Gère la capture d'un fruit normal"""
        temps_actuel = pygame.time.get_ticks()
        
        # Vérifier combo (moins d'1 seconde entre 2 fruits)
        if temps_actuel - self.dernier_temps_fruit < 1000:
            self.combo += 1
            points = 1 + self.combo
            print(f"🔥 COMBO x{self.combo}! +{points} points")
        else:
            self.combo = 0
            points = 1
        
        self.score += points
        self.fruits_attrapes += 1
        self.dernier_temps_fruit = temps_actuel
        
        print(f"✅ Fruit attrapé! Score: {self.score}")
    
    def activer_ralentissement(self):
        """Active l'effet ralentissement"""
        self.temps_ralenti_restant = DUREE_RALENTISSEMENT * FPS
        self.multiplicateur_vitesse = 0.5
        print(f"❄️  RALENTISSEMENT activé pour {DUREE_RALENTISSEMENT}s!")
    
    def mettre_a_jour(self):
        """Met à jour l'état du jeu chaque frame"""
        if self.game_over:
            return
        
        self.compteur_frames += 1
        
        # Apparition de nouveaux fruits
        if self.compteur_frames % FREQUENCE_FRUIT == 0:
            self.creer_fruit("normal")
        
        if self.compteur_frames % FREQUENCE_BOMBE == 0:
            self.creer_fruit("bombe")
        
        if self.compteur_frames % FREQUENCE_GLACON == 0:
            self.creer_fruit("glacon")
        
        # Gérer le ralentissement
        if self.temps_ralenti_restant > 0:
            self.temps_ralenti_restant -= 1
        else:
            self.multiplicateur_vitesse = 1.0
        
        # Mettre à jour les fruits
        fruits_a_retirer = []
        
        for fruit in self.fruits:
            fruit.tomber(self.multiplicateur_vitesse)
            
            # Fruit sorti de l'écran
            if fruit.est_hors_ecran():
                
                # Fruit normal raté = STRIKE
                if fruit.type_fruit == "normal" and not fruit.est_tape:
                    self.strikes += 1
                    print(f"⚠️  STRIKE! ({self.strikes}/{MAX_STRIKES})")
                    
                    if self.strikes >= MAX_STRIKES:
                        print("💀 GAME OVER - Trop de strikes!")
                        self.game_over = True
                
                # Bombe évitée = bien joué!
                elif fruit.type_fruit == "bombe" and not fruit.est_tape:
                    self.bombes_evitees += 1
                
                fruits_a_retirer.append(fruit)
            
            # Fruit tapé = retirer
            elif fruit.est_tape:
                fruits_a_retirer.append(fruit)
        
        # Retirer les fruits de la liste
        for fruit in fruits_a_retirer:
            self.fruits.remove(fruit)
    
    def dessiner(self):
        """Dessine tous les éléments visuels"""
        # Effacer l'écran
        self.ecran.fill(BLANC)
        
        # ÉCRAN DE GAME OVER
        if self.game_over:
            from utils.helpers import afficher_texte_centre
            
            afficher_texte_centre(
                self.ecran,
                TEXTE_GAME_OVER,
                self.police_titre,
                ROUGE,
                HAUTEUR_ECRAN // 2 - 150
            )
            
            afficher_texte_centre(
                self.ecran,
                f"Score final: {self.score}",
                self.police_ui,
                NOIR,
                HAUTEUR_ECRAN // 2 - 50
            )
            
            afficher_texte_centre(
                self.ecran,
                f"Meilleur score: {self.meilleur_score}",
                self.police_ui,
                GRIS,
                HAUTEUR_ECRAN // 2
            )
            
            afficher_texte_centre(
                self.ecran,
                f"Fruits attrapés: {self.fruits_attrapes}",
                self.police_ui,
                VERT,
                HAUTEUR_ECRAN // 2 + 50
            )
            
            afficher_texte_centre(
                self.ecran,
                f"Bombes évitées: {self.bombes_evitees}",
                self.police_ui,
                ORANGE,
                HAUTEUR_ECRAN // 2 + 80
            )
            
            afficher_texte_centre(
                self.ecran,
                TEXTE_REJOUER,
                self.police_ui,
                GRIS,
                HAUTEUR_ECRAN // 2 + 130
            )
            
            afficher_texte_centre(
                self.ecran,
                "ou ÉCHAP pour quitter",
                self.police_ui,
                GRIS,
                HAUTEUR_ECRAN // 2 + 160
            )
        
        # ÉCRAN DE JEU
        else:
            # Dessiner les fruits
            for fruit in self.fruits:
                fruit.dessiner(self.ecran, self.police_fruit)
            
            # Score
            texte_score = self.police_ui.render(
                f"{TEXTE_SCORE}{self.score}",
                True,
                NOIR
            )
            self.ecran.blit(texte_score, (10, 10))
            
            # Strikes
            couleur_strikes = ROUGE if self.strikes >= 2 else ORANGE
            texte_strikes = self.police_ui.render(
                f"{TEXTE_STRIKES}{self.strikes}/{MAX_STRIKES}",
                True,
                couleur_strikes
            )
            self.ecran.blit(texte_strikes, (10, 40))
            
            # Meilleur score
            texte_meilleur = self.police_ui.render(
                f"Record: {self.meilleur_score}",
                True,
                GRIS
            )
            largeur_texte = texte_meilleur.get_width()
            self.ecran.blit(texte_meilleur, (LARGEUR_ECRAN - largeur_texte - 10, 10))
            
            # Zone de saisie (en bas)
            pygame.draw.rect(
                self.ecran,
                GRIS,
                (0, HAUTEUR_ECRAN - 60, LARGEUR_ECRAN, 60)
            )
            
            # Texte tapé
            texte_input = self.police_input.render(
                f"{TEXTE_INPUT}{self.texte_tape}",
                True,
                BLANC
            )
            self.ecran.blit(texte_input, (10, HAUTEUR_ECRAN - 45))
            
            # Curseur clignotant
            if (self.compteur_frames // 30) % 2 == 0:
                pygame.draw.rect(
                    self.ecran,
                    BLANC,
                    (15 + texte_input.get_width(), HAUTEUR_ECRAN - 40, 2, 25)
                )
            
            # Indicateur ralentissement
            if self.temps_ralenti_restant > 0:
                texte_ralenti = self.police_ui.render(
                    f"{TEXTE_RALENTI} ({self.temps_ralenti_restant // FPS}s)",
                    True,
                    BLEU
                )
                self.ecran.blit(texte_ralenti, (LARGEUR_ECRAN - 200, 40))
            
            # Indicateur combo
            if self.combo > 0:
                texte_combo = self.police_ui.render(
                    f"COMBO x{self.combo + 1}",
                    True,
                    JAUNE
                )
                self.ecran.blit(texte_combo, (LARGEUR_ECRAN - 200, 70))
        
        # Rafraîchir l'affichage
        pygame.display.flip()
    
    def lancer(self):
        """Boucle principale du jeu"""
        print("\n🚀 Démarrage du jeu...")
        print("📝 Tapez les mots et appuyez sur ENTRÉE")
        print("💣 Évitez les mots rouges (bombes)!")
        print("❄️  Les mots bleus ralentissent le temps")
        print("=" * 50)
        
        en_cours = True
        
        while en_cours:
            # 1. Gérer les événements
            en_cours = self.gerer_evenements()
            
            # 2. Mettre à jour
            self.mettre_a_jour()
            
            # 3. Dessiner
            self.dessiner()
            
            # 4. Contrôler les FPS
            self.horloge.tick(FPS)
        
        # Sauvegarder le score
        from utils.helpers import sauvegarder_score
        if self.score > 0:
            sauvegarder_score(self.score)
        
        print("\n" + "=" * 50)
        print("👋 Merci d'avoir joué!")
        print(f"📊 Score final: {self.score}")
        print("=" * 50)
        
        pygame.quit()