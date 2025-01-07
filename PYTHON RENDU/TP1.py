# TP : Découverte du paradigme impératif en Python
Nom=input("veuillez inserer votre nom :")
print(f"Bonjour {Nom}, combien d'étudiant voulez vous?")
Nombre=int(input("veuillez saisir le nombre d'étudiants : "))  

 

etudiants = []
Note = []

for i in range(Nombre) :
     print(f"Nom de l'étudiant {i+1} ")
     etudiants.append(input()) 
     Note.append(int(input("Note de l'étudiant " + etudiants[i]+ " : " )))
     
     
     
     
def moyenne(n):
    somme = 0
    for i in n :
     somme = somme + i
    somme = somme / len(n)
    
    print(f"La moyenne de la classe est {somme}")     

moyenne(Note)   
     
def repartition(etudiants,Note):
    reussite = []
    echec = []

    for i in range(len(Note)):
        if Note [i] >= 10:
        
            reussite.append(etudiants[i])
        else:
            echec.append(etudiants[i])
    print("reussite",reussite)
    print("echec",echec)
 
repartition (etudiants,Note)


def meilleure_note(Note):
    meilleur=0
   
    for i in range (len(Note)):
          if Note[i] > meilleur:
                meilleur=Note[i]
    print (f"la meilleure note est {meilleur}")            
 
meilleure_note(Note)
