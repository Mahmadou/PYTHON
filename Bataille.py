from doctest import master
import tkinter as tk
from tkinter import messagebox
import random
from tkinter import ttk  # Import nécessaire pour les Combobox
import pygame
import os


# Définir un chemin absolu vers le dossier "sounds"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Répertoire de bataille.py
SOUNDS_DIR = os.path.join(BASE_DIR, "sounds")  # Répertoire des sons

# Vérification
print("Chemin des sons :", SOUNDS_DIR)


pygame.mixer.init()


def tester_les_sons():
    """
    Teste tous les fichiers sons dans le dossier 'sounds'.
    """
    print("Test des fichiers sons...")
    for fichier in ["eau.wav", "explosion.wav", "victory.wav", "defeat.wav"]:
        chemin = os.path.join(SOUNDS_DIR, fichier)
        if os.path.exists(chemin):
            print(f"Lecture de {fichier}...")
            pygame.mixer.Sound(chemin).play()
            pygame.time.wait(2000)  # Attendre 2 secondes entre chaque son
        else:
            print(f"Fichier introuvable : {fichier}")




# Classes Navire, Plateau, Joueur (reprendre les classes de base déjà fournies)
class Navire:
    def __init__(self, nom, taille):
        """
        Initialise un navire avec un nom, une taille, et garde en mémoire ses positions.
        """
        self.nom = nom
        self.taille = taille
        self.positions = []  # Positions occupées par le navire
        self.touchees = []  # Positions touchées
        self.est_coule_flag = False  # État du navire (coulé ou non)

    def ajouter_positions(self, positions):
        """
        Définit les positions du navire.
        """
        self.positions = positions
        print(f"[LOG] Navire {self.nom} placé aux positions : {self.positions}")

    def est_touche(self, position):
        """
        Marque une position comme touchée.
        """
        if position in self.positions and position not in self.touchees:
            self.touchees.append(position)
            print(f"[LOG] Navire {self.nom} touché à la position : {position}")
        else:
            print(f"[LOG] Navire {self.nom} déjà touché ou position invalide : {position}")

    def verifier_etat(self):
        """
        Vérifie si le navire est complètement coulé.
        """
        if all(position in self.touchees for position in self.positions):
            self.est_coule_flag = True
            print(f"[LOG] Navire {self.nom} est maintenant coulé avec succès.")
            return True
        return False


class Plateau:
    def __init__(self, taille=10):
        """
        Initialise un plateau de jeu avec une grille.
        """
        self.taille = taille
        self.grille = [[None for _ in range(taille)] for _ in range(taille)]
        self.navires = []  # Liste des navires placés

    def est_position_valide(self, positions):
        """
        Vérifie si toutes les positions sont valides (dans la grille et libres).
        """
        for x, y in positions:
            if not (0 <= x < self.taille and 0 <= y < self.taille) or self.grille[x][y] is not None:
                return False
        return True

    def placer_navire(self, navire, positions):
        """
        Place un navire sur le plateau.
        """
        if self.est_position_valide(positions):
            for x, y in positions:
                self.grille[x][y] = navire
            navire.ajouter_positions(positions)
            self.navires.append(navire)
            return True
        return False

    def tirer(self, position):
        """
        Tente un tir sur une position.
        """
        x, y = position
        if not (0 <= x < self.taille and 0 <= y < self.taille):
            print(f"[LOG] Position {position} invalide pour un tir.")
            return "invalide"

        if self.grille[x][y] is None:
            print(f"[LOG] Tir à la position {position} manqué.")
            return "manqué"
        else:
            navire = self.grille[x][y]
            navire.est_touche(position)
            print(f"[LOG] Positions du navire {navire.nom} : {navire.positions}")
            print(f"[LOG] Positions touchées : {navire.touchees}")

            if navire.verifier_etat():
                print(f"[LOG] Navire {navire.nom} coulé avec succès.")
                return "coulé"
            print(f"[LOG] Tir à la position {position} a touché le navire {navire.nom}.")
            return "touché"




class Joueur:
    def __init__(self, nom, est_humain=True):
        """
        Initialise un joueur (humain ou ordinateur).
        """
        self.nom = nom
        self.plateau = Plateau()
        self.est_humain = est_humain

    def placer_navire_manuellement(self, navire, positions):
        """
        Permet à un joueur humain de placer un navire.
        """
        return self.plateau.placer_navire(navire, positions)

    def placer_navires_aleatoirement(self, navires):
        """
        Place les navires aléatoirement (pour l'ordinateur).
        """
        for navire in navires:
            while True:
                orientation = random.choice(["horizontal", "vertical"])
                if orientation == "horizontal":
                    ligne = random.randint(0, self.plateau.taille - 1)
                    colonne = random.randint(0, self.plateau.taille - navire.taille)
                    positions = [(ligne, colonne + i) for i in range(navire.taille)]
                else:  # Vertical
                    ligne = random.randint(0, self.plateau.taille - navire.taille)
                    colonne = random.randint(0, self.plateau.taille - 1)
                    positions = [(ligne + i, colonne) for i in range(navire.taille)]

                if self.plateau.placer_navire(navire, positions):
                    break

    def tirer(self, adversaire, position):
        """
        Tente un tir sur le plateau de l'adversaire.
        """
        return adversaire.plateau.tirer(position)


    def tirer_sur_ordinateur(self, x, y):
        """
        Gère un tir sur le plateau de l'ordinateur.
        """
        position = (x, y)

        if self.ordinateur.plateau.grille[x][y] is None:
            print(f"[LOG] Tir à la position {position} manqué.")
            self.computer_buttons[x][y].config(bg="blue", state="disabled")
            self.jouer_son("eau.wav")
        else:
            navire = self.ordinateur.plateau.grille[x][y]
            navire.touchees.append(position)
            print(f"[LOG] Tir à la position {position} a touché le navire {navire.nom}.")
            self.computer_buttons[x][y].config(bg="red", state="disabled")
            self.jouer_son("explosion.wav")

            if navire.verifier_etat():
                for px, py in navire.positions:
                    self.computer_buttons[px][py].config(bg="darkred", state="disabled")
                print(f"[LOG] Navire {navire.nom} coulé.")
                self.ordinateur_bateaux_restants -= 1
                self.bateaux_label.config(
                    text=f"Bateaux restants : Joueur 1 = {self.joueur1_bateaux_restants}, Ordinateur = {self.ordinateur_bateaux_restants}"
                )

            self.jouer_son("explosion.wav")

        if self.verifier_fin_de_jeu():
            return

    def tir_ordinateur(self):
        """
        L'ordinateur effectue un tir sur le plateau du joueur.
        """
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if self.joueur1.plateau.grille[x][y] is None or isinstance(self.joueur1.plateau.grille[x][y], Navire):
                break

        position = (x, y)
        resultat = self.ordinateur.tirer(self.joueur1, position)

        if resultat == "manqué":
            self.grille_buttons[x][y].config(bg="blue", state="disabled")
            self.jouer_son("eau.wav")
        elif resultat == "touché":
            self.grille_buttons[x][y].config(bg="red", state="disabled")
            self.jouer_son("explosion.wav")
        elif resultat == "coulé":
            navire = self.joueur1.plateau.grille[x][y]
            for px, py in navire.positions:
                self.grille_buttons[px][py].config(bg="darkred", state="disabled")
            messagebox.showinfo("Navire touché !", "L'ordinateur a coulé un de vos navires.")
            
            # Diminue le compteur de navires restants
            self.joueur1_bateaux_restants -= 1
            self.bateaux_label.config(
                text=f"Bateaux restants : Joueur 1 = {self.joueur1_bateaux_restants}, Ordinateur = {self.ordinateur_bateaux_restants}"
            )
            self.jouer_son("explosion.wav")

        # Vérifie la fin de jeu
        if self.verifier_fin_de_jeu():
            return

        # Passe au tour du joueur
        self.tour_joueur = True
        self.label_tour.config(text="À votre tour de tirer !")

    def disable_grids(self):
        """
        Désactive les grilles après la fin de la partie.
        """
        for row in self.grille_buttons:
            for btn in row:
                btn.config(state="disabled")

        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="disabled")


# Fonction pour générer des positions aléatoires pour les navires
def generer_positions_aleatoires(taille, plateau):
    """
    Génère une liste de positions valides aléatoires pour un navire.
    """
    while True:
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            ligne = random.randint(0, plateau.taille - 1)
            colonne = random.randint(0, plateau.taille - taille)
            positions = [(ligne, colonne + i) for i in range(taille)]
        else:  # Vertical
            ligne = random.randint(0, plateau.taille - taille)
            colonne = random.randint(0, plateau.taille - 1)
            positions = [(ligne + i, colonne) for i in range(taille)]

        # Vérifie que toutes les positions sont valides et libres
        if plateau.est_position_valide(positions):
            return positions


# Interface graphique avec Tkinter
class BatailleNavaleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Jeu de la Bataille Navale")

        # Joueurs
        self.joueur1 = Joueur("Joueur 1")
        self.ordinateur = Joueur("Ordinateur")

        # Phase de placement des navires
        self.navires = [
            Navire("Porte-avions", 5),
            Navire("Croiseur", 4)
        ]
        self.navire_actuel_index = 0
        self.positions_actuelles = []
        self.grille_buttons = []
        self.computer_buttons = []
        self.nombre_tours = 0
        self.tirs_joueur_touches = 0
        self.tirs_joueur_manques = 0
        self.navires_joueur_coules = 0

        self.tirs_ordinateur_touches = 0
        self.tirs_ordinateur_manques = 0
        self.navires_ordinateur_coules = 0

        # Création des grilles
        self.create_player_grid()
        self.create_computer_grid()

        # Placement des navires de l'ordinateur
        self.placer_navires_ordinateur()

        # Indication sous les grilles
        self.player_label_bottom = tk.Label(
            self.master, text="Votre Grille", font=("Arial", 10), bg="black", fg="white"
        )
        self.player_label_bottom.grid(row=10, column=0, columnspan=10)

        self.computer_label_bottom = tk.Label(
            self.master, text="Grille de l'Ordinateur", font=("Arial", 10), bg="black", fg="white"
        )
        self.computer_label_bottom.grid(row=10, column=12, columnspan=10)


        # Indicateur de tour
        self.tour_joueur = True
        self.label_tour = tk.Label(
            self.master,
            text="À votre tour de tirer !",
            font=("Arial", 14, "bold"),
            bg="black",
            fg="white"
        )
        self.label_tour.grid(row=11, column=5, columnspan=10, pady=10)  # Centré entre les grilles


        self.orientation = "horizontal"

        self.orientation_label = tk.Label(self.master, text="Orientation : Horizontal", font=("Arial", 10))
        self.orientation_label.grid(row=13, column=0, columnspan=5)

        self.orientation_button = tk.Button(
            self.master,
            text="Changer Orientation",
            command=self.changer_orientation,
            font=("Arial", 10)
        )
        self.orientation_button.grid(row=13, column=5, columnspan=5)

        self.master.config(bg="black")

                # Cadre pour les grilles
        self.player_frame = tk.Frame(self.master, bg="black")
        self.player_frame.grid(row=0, column=0, rowspan=10, columnspan=10, padx=5, pady=5)

        self.computer_frame = tk.Frame(self.master, bg="black")
        self.computer_frame.grid(row=0, column=12, rowspan=10, columnspan=10, padx=5, pady=5)

        self.joueur1_bateaux_restants = len(self.navires)  # Nombre de navires du joueur 1
        self.ordinateur_bateaux_restants = len(self.navires)  # Nombre de navires de l'ordinateur

        # Label pour afficher le nombre de bateaux restants
        self.bateaux_label = tk.Label(
            self.master,
            text=f"Bateaux restants : Joueur 1 = {self.joueur1_bateaux_restants}, Ordinateur = {self.ordinateur_bateaux_restants}",
            font=("Arial", 12),
            bg="black",
            fg="white"
        )
        self.bateaux_label.grid(row=14, column=0, columnspan=20)
        
    def afficher_menu_accueil(self):
        """
        Affiche un menu d'accueil avec les règles du jeu.
        """
        self.menu_frame = tk.Frame(self.master, bg="black")
        self.menu_frame.grid(row=0, column=0, columnspan=10, rowspan=10)

        # Titre
        titre_label = tk.Label(
            self.menu_frame,
            text="Bienvenue dans la Bataille Navale",
            font=("Arial", 18, "bold"),
            bg="black",
            fg="white",
            pady=20,
        )
        titre_label.pack()

        # Règles du jeu
        regles = (
            "Règles du jeu :\n"
            "- Placez vos navires sur votre grille.\n"
            "- Devinez où se trouvent les navires de l'ordinateur.\n"
            "- Un tir touché est marqué en rouge, manqué en bleu.\n"
            "- Le premier à couler tous les navires adverses gagne.\n\n"
            "Cliquez sur Commencer pour jouer."
        )
        regles_label = tk.Label(
            self.menu_frame,
            text=regles,
            font=("Arial", 12),
            bg="black",
            fg="white",
            justify="left",
            padx=20,
            pady=10,
        )
        regles_label.pack()
        
        # Liste déroulante pour choisir la difficulté
        self.difficulte = tk.StringVar()
        self.difficulte.set("Facile")  # Valeur par défaut

        difficulte_label = tk.Label(
            self.menu_frame,
            text="Choisissez la difficulté :",
            font=("Arial", 12),
            bg="black",
            fg="white",
        )
        difficulte_label.pack(pady=10)

        difficulte_combobox = ttk.Combobox(
            self.menu_frame,
            textvariable=self.difficulte,
            values=["Facile", "Difficile"],
            state="readonly",
        )
        difficulte_combobox.pack()

        # Bouton Commencer
        commencer_button = tk.Button(
            self.menu_frame,
            text="Commencer le jeu",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.lancer_jeu
        )
        commencer_button.pack(pady=20)

    def lancer_jeu(self):
        """
        Ferme le menu d'accueil et affiche la grille du jeu.
        """
        self.menu_frame.destroy()  # Supprime le menu d'accueil

    def create_player_grid(self):
        """
        Création de la grille pour le joueur avec des événements de survol.
        """
        for i in range(10):
            row = []
            for j in range(10):
                btn = tk.Button(
                    self.master,
                    text="",
                    width=4,
                    height=2,
                    bg="#ADD8E6",  # Bleu clair
                    relief="raised",
                    bd=2,
                    activebackground="#5F9EA0",  # Vert foncé
                    font=("Arial", 10),
                    command=lambda x=i, y=j: self.selectionner_case(x, y),
                )
                btn.grid(row=i, column=j, padx=1, pady=1)

                # Ajout des événements pour le survol
                btn.bind("<Enter>", lambda event, x=i, y=j: self.previsualiser_navire(x, y))
                btn.bind("<Leave>", lambda event, x=i, y=j: self.reinitialiser_previsualisation(x, y))

                row.append(btn)
            self.grille_buttons.append(row)

    def previsualiser_navire(self, x, y):
        """
        Colorie les cases en vert pour prévisualiser le placement du navire.
        """
        navire = self.navires[self.navire_actuel_index]
        positions = []

        if self.orientation == "horizontal":
            positions = [(x, y + i) for i in range(navire.taille) if y + i < 10]
        else:  # Vertical
            positions = [(x + i, y) for i in range(navire.taille) if x + i < 10]

        if len(positions) == navire.taille and self.joueur1.plateau.est_position_valide(positions):
            for px, py in positions:
                if self.grille_buttons[px][py].cget("bg") != "green":  # Ignorer les cases déjà validées
                    self.grille_buttons[px][py].config(bg="lightgreen")




    def create_computer_grid(self):
        """
        Création de la grille pour l'ordinateur avec un style amélioré.
        """
        for i in range(10):
            row = []
            for j in range(10):
                btn = tk.Button(
                    self.master,
                    text="",
                    width=4,
                    height=2,
                    bg="#D3D3D3",  # Gris clair
                    relief="raised",
                    bd=2,
                    activebackground="#FF4500",  # Orange foncé
                    font=("Arial", 10),
                    command=lambda x=i, y=j: self.tirer_sur_ordinateur(x, y),
                )
                btn.grid(row=i, column=12 + j, padx=1, pady=1)
                row.append(btn)
            self.computer_buttons.append(row)

    def reinitialiser_previsualisation(self, x, y):
        """
        Réinitialise les couleurs des cases après le survol, sauf pour les cases validées.
        """
        if self.navire_actuel_index >= len(self.navires):  # Vérifie si tous les navires ont été placés
            return

        navire = self.navires[self.navire_actuel_index]
        positions = []

        if self.orientation == "horizontal":
            positions = [(x, y + i) for i in range(navire.taille) if y + i < 10]
        else:  # Vertical
            positions = [(x + i, y) for i in range(navire.taille) if x + i < 10]

        if len(positions) == navire.taille:
            for px, py in positions:
                if self.grille_buttons[px][py].cget("bg") == "lightgreen":  # Réinitialiser uniquement les cases en prévisualisation
                    self.grille_buttons[px][py].config(bg="#ADD8E6")  # Bleu clair




    def selectionner_case(self, x, y):
        """
        Permet au joueur de sélectionner les cases pour placer un navire.
        """
        navire = self.navires[self.navire_actuel_index]
        positions = []

        if self.orientation == "horizontal":
            positions = [(x, y + i) for i in range(navire.taille) if y + i < 10]
        else:  # Vertical
            positions = [(x + i, y) for i in range(navire.taille) if x + i < 10]

        if len(positions) == navire.taille and self.joueur1.plateau.est_position_valide(positions):
            # Place le navire immédiatement
            if self.joueur1.placer_navire_manuellement(navire, positions):
                for px, py in positions:
                    self.grille_buttons[px][py].config(bg="green", state="disabled")  # Vert permanent pour les navires placés
                self.navire_actuel_index += 1
                if self.navire_actuel_index >= len(self.navires):
                    messagebox.showinfo("Placement terminé", "Tous vos navires sont placés.")
                    self.label_tour.config(text="À votre tour de tirer !")
            else:
                messagebox.showerror("Erreur", "Placement invalide. Réessayez.")
        else:
            messagebox.showerror("Erreur", f"Veuillez sélectionner {navire.taille} cases valides pour le {navire.nom}.")
        if self.navire_actuel_index >= len(self.navires):
            messagebox.showinfo("Placement terminé", "Tous vos navires sont placés.")
            self.label_tour.config(text="À votre tour de tirer !")
            
            # Supprime les boutons et labels liés à l'orientation
            self.changer_orientation()




    def valider_placement(self):
        """
        Valide le placement d'un navire.
        """
        navire = self.navires[self.navire_actuel_index]
        if len(self.positions_actuelles) == navire.taille:
            if self.joueur1.placer_navire_manuellement(navire, self.positions_actuelles):
                messagebox.showinfo("Placement validé", f"{navire.nom} placé !")
                self.navire_actuel_index += 1
                self.positions_actuelles = []

                if self.navire_actuel_index >= len(self.navires):
                    messagebox.showinfo("Placement terminé", "Tous vos navires sont placés.")
                    self.validate_button.config(state="disabled")
                    self.label_tour.config(text="À votre tour de tirer !")
            else:
                messagebox.showerror("Erreur", "Placement invalide. Réessayez.")
        else:
            messagebox.showerror("Erreur", f"Veuillez sélectionner {navire.taille} cases pour le {navire.nom}.")


    def placer_navires_ordinateur(self):
        """
        Place les navires de l'ordinateur sans chevauchement et uniquement des navires autorisés.
        """
        self.ordinateur.plateau = Plateau()  # Réinitialise le plateau

        navires_a_placer = [
            Navire("Porte-avions", 5),
            Navire("Croiseur", 4)
        ]

        for navire in navires_a_placer:
            while True:
                positions = generer_positions_aleatoires(navire.taille, self.ordinateur.plateau)
                # Vérifie que toutes les positions sont libres
                if all(self.ordinateur.plateau.grille[x][y] is None for x, y in positions):
                    if self.ordinateur.plateau.placer_navire(navire, positions):
                        print(f"[LOG] Navire {navire.nom} placé aux positions : {positions}")
                        break
                    else:
                        print(f"[LOG] Échec du placement pour {navire.nom}. Réessai...")





    def tirer_sur_ordinateur(self, x, y):
        """
        Gère un tir sur le plateau de l'ordinateur.
        """
        self.nombre_tours += 0.5  # Ajout de 0.5 pour compter un tour complet après le tir du joueur.
        if not self.tour_joueur:
            print("[LOG] Tentative de tir alors que ce n'est pas le tour du joueur.")
            return

        position = (x, y)
        resultat = self.joueur1.tirer(self.ordinateur, position)
        print(f"[LOG] Résultat du tir du joueur sur la position {position} : {resultat}")

        if resultat == "manqué":
            self.computer_buttons[x][y].config(bg="blue", state="disabled")
            self.tirs_joueur_manques += 1
            self.jouer_son("eau.wav")
        elif resultat == "touché":
            self.computer_buttons[x][y].config(bg="red", state="disabled")
            self.tirs_joueur_touches += 1
            self.jouer_son("explosion.wav")
        elif resultat == "coulé":
            navire = self.ordinateur.plateau.grille[x][y]
            for px, py in navire.positions:
                self.computer_buttons[px][py].config(bg="darkred", state="disabled")
                self.tirs_joueur_touches += 1
            print(f"[LOG] Navire coulé : {navire.nom}.")
            self.navires_ordinateur_coules += 1
            self.ordinateur_bateaux_restants -= 1
            self.bateaux_label.config(
                text=f"Bateaux restants : Joueur 1 = {self.joueur1_bateaux_restants}, Ordinateur = {self.ordinateur_bateaux_restants}"
            )
            self.jouer_son("explosion.wav")

        if self.verifier_fin_de_jeu():
            return

        # Passe au tour de l'ordinateur
        self.tour_joueur = False
        self.label_tour.config(text="Tour de l'ordinateur")
        self.master.after(1000, self.tir_ordinateur)


    def tir_ordinateur(self):
        """
        L'ordinateur effectue un tir sur le plateau du joueur, en suivant une logique différente selon la difficulté.
        """
        self.nombre_tours += 0.5  # Ajout de 0.5 pour compter un tour complet après le tir du joueur.
        if not hasattr(self, "cibles_prioritaires"):
            self.cibles_prioritaires = []  # Liste pour stocker les cibles prioritaires

        position = None

        # Mode "Difficile" : Priorité aux cases adjacentes si un navire est en cours d'attaque
        if self.difficulte.get() == "Difficile" and self.cibles_prioritaires:
            position = self.cibles_prioritaires.pop(0)
        else:
            # Sinon, tir aléatoire
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                if self.joueur1.plateau.grille[x][y] is None or isinstance(self.joueur1.plateau.grille[x][y], Navire):
                    position = (x, y)
                    break

        resultat = self.ordinateur.tirer(self.joueur1, position)
        print(f"[LOG] Résultat du tir de l'ordinateur sur la position {position} : {resultat}")

        if resultat == "manqué":
            self.grille_buttons[position[0]][position[1]].config(bg="blue", state="disabled")
            self.tirs_ordinateur_manques += 1
            self.jouer_son("eau.wav")
        elif resultat == "touché":
            self.grille_buttons[position[0]][position[1]].config(bg="red", state="disabled")
            self.tirs_ordinateur_touches += 1
            self.jouer_son("explosion.wav")

            # Si on est en "Difficile", ajouter les cases adjacentes aux priorités
            if self.difficulte.get() == "Difficile":
                x, y = position
                adjacentes = [
                    (x - 1, y), (x + 1, y),  # Haut et Bas
                    (x, y - 1), (x, y + 1)   # Gauche et Droite
                ]
                for adj in adjacentes:
                    if (0 <= adj[0] < 10 and 0 <= adj[1] < 10 and
                            adj not in self.cibles_prioritaires and
                            (self.joueur1.plateau.grille[adj[0]][adj[1]] is None or
                            isinstance(self.joueur1.plateau.grille[adj[0]][adj[1]], Navire))):
                        self.cibles_prioritaires.append(adj)

        elif resultat == "coulé":
            navire = self.joueur1.plateau.grille[position[0]][position[1]]
            for px, py in navire.positions:
                self.grille_buttons[px][py].config(bg="darkred", state="disabled")
                self.tirs_ordinateur_touches += 1
            print(f"[LOG] Navire coulé par l'ordinateur : {navire.nom}.")
            self.joueur1_bateaux_restants -= 1
            self.navires_joueur_coules += 1
            self.bateaux_label.config(
                text=f"Bateaux restants : Joueur 1 = {self.joueur1_bateaux_restants}, Ordinateur = {self.ordinateur_bateaux_restants}"
            )
            self.jouer_son("explosion.wav")

            # Si un navire est coulé, réinitialiser les priorités
            self.cibles_prioritaires = []

        if self.verifier_fin_de_jeu():
            return
        
        self.tour_joueur = True

        # Passe au tour du joueur
        self.tour_joueur = True
        self.label_tour.config(text="À votre tour de tirer !")



    def disable_grids(self):
        """
        Désactive les grilles après la fin de la partie.
        """
        for row in self.grille_buttons:
            for btn in row:
                btn.config(state="disabled")
        for row in self.computer_buttons:
            for btn in row:
                btn.config(state="disabled")

    def jouer_son(self, fichier):
        """
        Joue un son donné.
        """
        try:
            chemin = os.path.join(SOUNDS_DIR, fichier)
            son = pygame.mixer.Sound(chemin)
            son.play()
        except Exception as e:
            print(f"Erreur lors de la lecture du son {fichier}: {e}")




    def changer_orientation(self):
        """
        Change l'orientation entre horizontal et vertical.
        Supprime visuellement les boutons et l'indication après utilisation.
        """
        if self.orientation == "horizontal":
            self.orientation = "vertical"
        else:
            self.orientation = "horizontal"

        # Met à jour le label d'orientation
        self.orientation_label.config(text=f"Orientation : {self.orientation.capitalize()}")

        # Vérifie si tous les navires sont placés et supprime les widgets
        if self.navire_actuel_index >= len(self.navires):
            self.orientation_label.destroy()
            self.orientation_button.destroy()



    def disable_player_grid(self):
        """
        Désactive la grille du joueur après la fin de la partie.
        """
        for row in self.grille_buttons:
            for btn in row:
                btn.config(state="disabled")
                
                

    def verifier_fin_de_jeu(self):
        """
        Vérifie si la partie est terminée et affiche l'écran de fin si nécessaire.
        """
        if self.ordinateur_bateaux_restants == 0:
            statistiques = (
                f"Tours joués : {self.nombre_tours}\n"
                f"Tirs du joueur :\n"
                f"- Touchés : {self.tirs_joueur_touches}\n"
                f"- Manqués : {self.tirs_joueur_manques}\n"
                f"- Navires coulés : {self.navires_ordinateur_coules}\n\n"
                f"Tirs de l'ordinateur :\n"
                f"- Touchés : {self.tirs_ordinateur_touches}\n"
                f"- Manqués : {self.tirs_ordinateur_manques}\n"
                f"- Navires coulés : {self.navires_joueur_coules}"
            )
            self.afficher_ecran_fin("Victoire ! Félicitations !", statistiques)
            return True
        elif self.joueur1_bateaux_restants == 0:
            statistiques = (
                f"Tours joués : {self.nombre_tours}\n"
                f"Tirs du joueur :\n"
                f"- Touchés : {self.tirs_joueur_touches}\n"
                f"- Manqués : {self.tirs_joueur_manques}\n"
                f"- Navires coulés : {self.navires_ordinateur_coules}\n\n"
                f"Tirs de l'ordinateur :\n"
                f"- Touchés : {self.tirs_ordinateur_touches}\n"
                f"- Manqués : {self.tirs_ordinateur_manques}\n"
                f"- Navires coulés : {self.navires_joueur_coules}"
            )
            self.afficher_ecran_fin("Défaite ! L'ordinateur a gagné.", statistiques)
            return True
        return False







    
    def fin_partie(self):
        self.disable_grids()
        for x in range(10):
            for y in range(10):
                # Grille du joueur
                if isinstance(self.joueur1.plateau.grille[x][y], Navire):
                    navire = self.joueur1.plateau.grille[x][y]
                    color = "darkred" if navire.verifier_etat() else ("red" if (x, y) in navire.touchees else "green")
                    self.grille_buttons[x][y].config(bg=color)

                # Grille de l'ordinateur
                if isinstance(self.ordinateur.plateau.grille[x][y], Navire):
                    navire = self.ordinateur.plateau.grille[x][y]
                    color = "darkred" if navire.verifier_etat() else ("red" if (x, y) in navire.touchees else "green")
                    self.computer_buttons[x][y].config(bg=color)


            # Ajout d'un bouton pour recommencer
            bouton_recommencer = tk.Button(
                self.master,
                text="Recommencer une partie",
                font=("Arial", 14),
                bg="blue",
                fg="white",
                command=self.recommencer_partie
            )
            bouton_recommencer.grid(row=15, column=0, columnspan=20, pady=10)


    def recommencer_partie(self):
        self.master.destroy()  # Ferme la fenêtre actuelle
        root = tk.Tk()
        app = BatailleNavaleApp(root)  # Nouvelle instance
        app.afficher_menu_accueil()  # Retour au menu d'accueil
        root.mainloop()
        
        
    def afficher_message_fin(self, message):
        """
        Affiche un message de fin de partie dans une fenêtre popup.
        """
        import tkinter as tk
        from tkinter import messagebox

        # Crée une fenêtre popup
        fin_popup = tk.Toplevel()
        fin_popup.title("Fin de la partie")

        # Texte du message
        label_message = tk.Label(fin_popup, text=message, font=("Helvetica", 14))
        label_message.pack(pady=20)

        # Bouton pour fermer le jeu ou recommencer
        bouton_rejouer = tk.Button(
            fin_popup,
            text="Rejouer",
            command=lambda: [fin_popup.destroy(), self.reinitialiser_jeu()],
            font=("Helvetica", 12)
        )
        bouton_rejouer.pack(pady=10)

        bouton_quitter = tk.Button(
            fin_popup,
            text="Quitter",
            command=self.root.quit,
            font=("Helvetica", 12)
        )
        bouton_quitter.pack(pady=10)

        fin_popup.transient(self.root)  # Centre par rapport à la fenêtre principale
        fin_popup.grab_set()           # Bloque les interactions avec la fenêtre principale
        self.root.wait_window(fin_popup)
        
    def reinitialiser_jeu(self):
        """
        Réinitialise la partie en recréant les grilles et les navires.
        """
        self.joueur1_bateaux_restants = 2
        self.ordinateur_bateaux_restants = 2
        self.creer_grilles()
        self.placer_navires_ordinateur()
        self.rafraichir_interface()
        print("[LOG] Partie réinitialisée.")

        
    def creer_grilles(self):
        """
        Crée ou réinitialise les grilles du joueur et de l'ordinateur.
        """
        # Réinitialiser les grilles
        self.joueur1.grille = [[None for _ in range(10)] for _ in range(10)]
        self.ordinateur.grille = [[None for _ in range(10)] for _ in range(10)]

        # Réinitialiser les navires
        self.joueur1.navires = []
        self.ordinateur.navires = []

        print("[LOG] Grilles réinitialisées.")
        
        
    def rafraichir_interface(self):
        """
        Met à jour l'interface graphique après une réinitialisation.
        """
        # Effacer les grilles existantes
        for widget in self.frame_grille_joueur.winfo_children():
            widget.destroy()
        for widget in self.frame_grille_ordinateur.winfo_children():
            widget.destroy()

        # Recréer les boutons de la grille
        self.creer_interface_grille(self.frame_grille_joueur, self.joueur1, est_joueur=True)
        self.creer_interface_grille(self.frame_grille_ordinateur, self.ordinateur, est_joueur=False)

        print("[LOG] Interface graphique rafraîchie.")

    def creer_interface_grille(self, frame, joueur, est_joueur):
        """
        Crée l'interface graphique pour une grille.
        """
        for i in range(10):
            for j in range(10):
                btn = tk.Button(frame, text=" ", width=2, height=1)
                btn.grid(row=i, column=j)
                
                if est_joueur:
                    # Actions spécifiques pour la grille du joueur
                    pass
                else:
                    # Actions spécifiques pour la grille de l'ordinateur
                    btn.config(command=lambda x=i, y=j: self.tirer_sur_ordinateur(x, y))
                    
                   
                    
    def afficher_ecran_fin(self, message, statistiques=None):
        """
        Affiche l'écran de fin avec un message et les statistiques si disponibles.
        """

        self.ecran_fin = tk.Frame(self.master, bg="black", padx=50, pady=40)
        self.ecran_fin.place(relx=0.5, rely=0.35, anchor=tk.CENTER)  # Ajustement de la hauteur

        if "Victoire" in message:
            self.jouer_son("victory.wav")
        elif "Défaite" in message:
            self.jouer_son("defeat.wav")
            self.ecran_fin = tk.Frame(self.master, bg="black", padx=50, pady=40)
            self.ecran_fin.place(relx=0.5, rely=0.35, anchor=tk.CENTER)  # Ajustement de la hauteur

        # Titre
        titre_label = tk.Label(
            self.ecran_fin,
            text=message,
            font=("Arial", 18, "bold"),
            bg="black",
            fg="white",
            pady=20,
        )
        titre_label.pack()

        if statistiques:
            stats_label = tk.Label(
                self.ecran_fin,
                text=statistiques,
                font=("Arial", 12),
                bg="black",
                fg="white",
                justify="left",
            )
            stats_label.pack()

        bouton_rejouer = tk.Button(
            self.ecran_fin,
            text="Rejouer",
            font=("Arial", 14),
            bg="green",
            fg="white",
            command=self.recommencer_partie,
        )
        bouton_rejouer.pack(pady=20)

        bouton_quitter = tk.Button(
            self.ecran_fin,
            text="Quitter",
            font=("Arial", 14),
            bg="red",
            fg="white",
            command=self.master.quit,
        )
        bouton_quitter.pack(pady=10)







# Lancement de l'application
if __name__ == "__main__":
    #tester_les_sons()
    root = tk.Tk()
    app = BatailleNavaleApp(root)
    app.afficher_menu_accueil()  # Affiche le menu d'accueil
    root.mainloop()
