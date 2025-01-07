from functools import reduce

# Exercice 1 : Utilisation de map
prix_en_euros = [50, 20, 35, 100, 80]
prix_en_dollars = list(map(lambda x: x * 1.10, prix_en_euros))
prix_en_dollars_avec_symbole = list(map(lambda x: f"${x * 1.10:.2f}", prix_en_euros))

# Exercice 2 : Utilisation de filter
ages = [12, 25, 17, 18, 40, 15, 22]
adultes = list(filter(lambda x: x >= 18, ages))
seniors = list(filter(lambda x: x >= 60, ages))

# Exercice 3 : Utilisation de reduce
ventes = [120, 50, 30, 20, 90, 100]
total_ventes = reduce(lambda x, y: x + y, ventes)
produit = reduce(lambda x, y: x * y, ventes)

# Exercice 4 : Combinaison de map, filter et reduce
notes = [12, 15, 9, 18, 6, 20, 14]
notes_sur_100 = list(map(lambda x: x * 5, notes))
notes_filtrees = list(filter(lambda x: x >= 50, notes_sur_100))
moyenne = reduce(lambda x, y: x + y, notes_filtrees) / len(notes_filtrees) if notes_filtrees else 0

# Exercice 5 : Données réelles (optionnel)
# Supposons que les données sont lues dans une liste de dictionnaires
employes = [{'nom': 'Alice', 'age': 30, 'salaire': 60000}, 
            {'nom': 'Bob', 'age': 25, 'salaire': 45000},
            {'nom': 'Charlie', 'age': 40, 'salaire': 70000}]

employes_maj = list(map(lambda x: {**x, 'nom': x['nom'].upper()}, employes))
employes_filtres = list(filter(lambda x: x['salaire'] > 50000, employes))
total_salaire = reduce(lambda x, y: x + y['salaire'], employes_filtres, 0)

def categoriser_salaire(emp):
    if emp['salaire'] < 30000:
        return {**emp, 'categorie': 'junior'}
    elif 30000 <= emp['salaire'] <= 50000:
        return {**emp, 'categorie': 'intermediaire'}
    else:
        return {**emp, 'categorie': 'senior'}

employes_categorises = list(map(categoriser_salaire, employes))

# Affichage des résultats (optionnel pour vérification)
print("Prix en dollars :", prix_en_dollars)
print("Prix en dollars avec symbole :", prix_en_dollars_avec_symbole)
print("Âges adultes :", adultes)
print("Âges seniors :", seniors)
print("Total des ventes :", total_ventes)
print("Produit des ventes :", produit)
print("Notes sur 100 :", notes_sur_100)
print("Notes filtrées :", notes_filtrees)
print("Moyenne des notes filtrées :", moyenne)
print("Employés avec noms en majuscule :", employes_maj)
print("Employés avec salaire > 50000 :", employes_filtres)
print("Total des salaires filtrés :", total_salaire)
print("Employés catégorisés :", employes_categorises)