import asyncio
import random

# Exercice 1: Programmation Immuable
def addToEach(n, lst):
    return [x + n for x in lst]

def removeDuplicates(lst):
    return list(dict.fromkeys(lst))

# Exercice 2: Objets Persistants et Promesses
class Personne:
    def __init__(self, nom, age):
        self.nom = nom
        self.age = age
    
    def __repr__(self):
        return f"Personne(nom={self.nom}, age={self.age})"

def anniversaire(personnes):
    return [Personne(p.nom, p.age + 1) for p in personnes]

async def getRandomNumber():
    await asyncio.sleep(1)
    return random.randint(1, 100)

async def main_async():
    number1 = asyncio.create_task(getRandomNumber())
    number2 = asyncio.create_task(getRandomNumber())
    await number1
    await number2
    print(f"Random numbers: {number1.result()}, {number2.result()}")

# Exercice 3: Système de Gestion d'Inventaire
class Article:
    def __init__(self, nom, prix, quantite):
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
    
    def __repr__(self):
        return f"Article(nom={self.nom}, prix={self.prix}, quantite={self.quantite})"

def ajouterArticle(inventaire, article):
    return inventaire + [article]

def mettreAJourQuantite(inventaire, nom, nouvelle_quantite):
    return [Article(a.nom, a.prix, nouvelle_quantite if a.nom == nom else a.quantite) for a in inventaire]

def supprimerArticle(inventaire, nom):
    return [a for a in inventaire if a.nom != nom]

class Commande:
    def __init__(self, articles):
        self.articles = articles  # Liste de tuples (Article, quantité)

def totalCommande(commande, inventaire):
    return sum(a.prix * q for a, q in commande.articles if any(art.nom == a.nom for art in inventaire))

class Promotion:
    def __init__(self, nom, condition, reduction):
        self.nom = nom
        self.condition = condition  # fonction qui vérifie la condition de la commande
        self.reduction = reduction  # fonction qui calcule la réduction

def appliquerPromotions(commande, inventaire, promotions):
    total = totalCommande(commande, inventaire)
    for promo in promotions:
        if promo.condition(commande):
            total = promo.reduction(total)
    return total

def mettreAJourStocks(commandes, inventaire):
    for commande in commandes:
        for article, quantite in commande.articles:
            inventaire = mettreAJourQuantite(inventaire, article.nom, 
                                             next(a.quantite - quantite for a in inventaire if a.nom == article.nom))
    return inventaire

# Exemples d'utilisation
if __name__ == "__main__":
    # Exercice 1
    print(addToEach(3, [1, 2, 3, 4]))  # [4, 5, 6, 7]
    print(removeDuplicates([1, 2, 2, 3, 4, 4, 5]))  # [1, 2, 3, 4, 5]

    # Exercice 2
    personnes = [Personne("Alice", 30), Personne("Bob", 25)]
    nouvelles_personnes = anniversaire(personnes)
    print(nouvelles_personnes)  # [Personne(nom=Alice, age=31), Personne(nom=Bob, age=26)]
    asyncio.run(main_async())

    # Exercice 3
    inventaire = [Article("pomme", 0.5, 100), Article("banane", 0.3, 50)]
    commande = Commande([(Article("pomme", 0.5, 0), 10)])
    print(totalCommande(commande, inventaire))  # 5.0

    # Exemple de promotion
    def condition(commande):
        return totalCommande(commande, inventaire) > 10
    def reduction(total):
        return total * 0.90  # 10% de réduction
    promo = Promotion("10% sur commande > 10", condition, reduction)
    print(appliquerPromotions(commande, inventaire, [promo]))  # Toujours 5.0 car condition non remplie

    # Mise à jour des stocks
    inventaire_apres_achat = mettreAJourStocks([commande], inventaire)
    print(inventaire_apres_achat)  # [Article(nom=pomme, prix=0.5, quantite=90), Article(nom=banane, prix=0.3, quantite=50)]