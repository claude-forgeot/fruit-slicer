"""
Fruit Slicer - Typing Game inspiré de Fruit Ninja
Point d'entrée principal du jeu

Auteur: Nelly A
Date: Janvier 2026
Version: 1.0
"""

from game import JeuFruitSlicer
import sys

#Affiche les règles
def afficher_instructions():
    """Affiche les instructions du jeu"""
    print("=" * 60)
    print("         🍎 FRUIT SLICER - TYPING GAME 🍎")
    print("=" * 60)
    print("\n📖 RÈGLES DU JEU:")
    print("   1. Des mots apparaissent et tombent du haut de l'écran")
    print("   2. Tapez le mot et appuyez sur ENTRÉE pour l'attraper")
    print("   3. Fruits verts (🍎) = +1 point")
    print("   4. Bombes rouges (💣) = Game Over si touchées!")
    print("   5. Glaçons bleus (❄️ ) = Ralentissent le temps")
    print("   6. 3 fruits ratés = Game Over")
    print("\n⌨️  CONTRÔLES:")
    print("   • Tapez les lettres pour former le mot")
    print("   • ENTRÉE = Valider le mot")
    print("   • RETOUR = Effacer un caractère")
    print("   • ÉCHAP = Quitter")
    print("   • ESPACE = Rejouer (après Game Over)")
    print("\n💡 ASTUCES:")
    print("   • Tapez rapidement plusieurs mots pour faire des combos")
    print("   • Les combos donnent des points bonus!")
    print("   • Utilisez les glaçons stratégiquement")
    print("=" * 60)
    print()

#Lance le jeu avec gestion d'erreurs
def main():
    """
    Fonction principale
    Lance le jeu et gère les erreurs
    """
    try:
        # Afficher les instructions
        afficher_instructions()
        
        # Demander confirmation avant de lancer
        print("Appuyez sur ENTRÉE pour commencer...")
        input()
        
        # Créer et lancer le jeu
        print("\n🎮 Chargement du jeu...\n")
        jeu = JeuFruitSlicer()
        jeu.lancer()
        
    except KeyboardInterrupt:
        # Si l'utilisateur fait Ctrl+C
        print("\n\n⚠️  Jeu interrompu par l'utilisateur")
        sys.exit(0)

 #Lance main() quand on exécute ce fichier       
    except Exception as e:
        # En cas d'erreur imprévue
        print(f"\n❌ ERREUR: {e}")
        print("Veuillez vérifier que Pygame est installé:")
        print("  pip install pygame")
        sys.exit(1)

if __name__ == "__main__":
    main()