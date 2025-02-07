/**
 * Classe représentant un film de la saga Star Wars.
 */
import java.util.*;

class Film {
    private String titre;
    private int annee;
    private String realisateur;
    private double cout;
    private double recette;
    private List<Acteur> acteurs;

    public Film(String titre, int annee, String realisateur, double cout, double recette) {
        this.titre = titre;
        this.annee = annee;
        this.realisateur = realisateur;
        this.cout = cout;
        this.recette = recette;
        this.acteurs = new ArrayList<>();
    }

    public void ajouterActeur(Acteur acteur) {
        this.acteurs.add(acteur);
    }

    public int nbActeurs() {
        return acteurs.size();
    }

    public int nbPersonnages() {
        int total = 0;
        for (Acteur acteur : acteurs) {
            total += acteur.nbPersonnages();
        }
        return total;
    }

    public String calculBenefice() {
        double benefice = recette - cout;
        return (benefice >= 0) ? "Bénéfice de " + benefice : "Déficit de " + (-benefice);
    }

    public boolean isBefore(int annee) {
        return this.annee < annee;
    }

    public void triActeurs() {
        Collections.sort(acteurs, Comparator.comparing(Acteur::getNom));
    }

    @Override
    public String toString() {
        return "Film: " + titre + ", Année: " + annee + ", Réalisé par: " + realisateur;
    }
}

class Acteur {
    private String nom;
    private List<Personnage> personnages;

    public Acteur(String nom) {
        this.nom = nom;
        this.personnages = new ArrayList<>();
    }

    public void ajouterPersonnage(Personnage personnage) {
        personnages.add(personnage);
    }

    public int nbPersonnages() {
        return personnages.size();
    }

    public String getNom() {
        return nom;
    }

    @Override
    public String toString() {
        return "Acteur: " + nom + ", Personnages: " + personnages;
    }
}

class Personnage {
    private String nom;
    private boolean coteObscur;

    public Personnage(String nom, boolean coteObscur) {
        this.nom = nom;
        this.coteObscur = coteObscur;
    }

    @Override
    public String toString() {
        return nom + (coteObscur ? " (Côté Obscur)" : " (Côté Lumineux)");
    }
}

public class Main {
    public static void main(String[] args) {
        // Création des objets
        Film film1 = new Film("Un Nouvel Espoir", 1977, "George Lucas", 11000000, 775000000);
        Film film2 = new Film("L'Empire Contre-Attaque", 1980, "Irvin Kershner", 18000000, 538000000);

        Acteur acteur1 = new Acteur("Mark Hamill");
        Acteur acteur2 = new Acteur("Harrison Ford");
        Acteur acteur3 = new Acteur("Carrie Fisher");

        Personnage perso1 = new Personnage("Luke Skywalker", false);
        Personnage perso2 = new Personnage("Han Solo", false);
        Personnage perso3 = new Personnage("Leia Organa", false);

        acteur1.ajouterPersonnage(perso1);
        acteur2.ajouterPersonnage(perso2);
        acteur3.ajouterPersonnage(perso3);

        film1.ajouterActeur(acteur1);
        film1.ajouterActeur(acteur2);
        film1.ajouterActeur(acteur3);

        // Affichage des informations
        System.out.println(film1);
        System.out.println("Nombre d'acteurs : " + film1.nbActeurs());
        System.out.println("Nombre de personnages : " + film1.nbPersonnages());
        System.out.println("Bénéfice : " + film1.calculBenefice());
    }
}
