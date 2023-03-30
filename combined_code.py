import time

class Automate:
    "transformation du transitionsramme ecrit dans un fichier sur un dictionnaire"

    def __init__(self, fichier):
        with open(fichier) as fichierAutomate:
            self.titre = fichierAutomate.readline().strip()
            self.mode = fichierAutomate.readline().strip()
            self.etatInitial = fichierAutomate.readline().strip()
            self.etatFinals = fichierAutomate.readline().strip().split(',')
            self.transitions = {}
            for line in fichierAutomate:
                colonnes = line.strip().split(',')
                key = (colonnes[0],colonnes[1])
                value = (colonnes[2],colonnes[3], colonnes[4])
                self.transitions[key]=value
            '''
            print(self.titre)
            print(self.mode)
            print(self.etatInitial)
            print(self.etatFinals)
            print(self.transitions)
            '''
            
            

    def getTransitions(self):
        "cette methode return la table de trasition sous la forme d'un dictionaire"
        return self.transitions

    def getInformations(self):
        "cette methode return le nom du transitionsramme a faire plus l'etat initiale et l'etat finale et le mode d'utilisation de la machine(accepteur/calculateur) sou la forme d'une liste "
        return [self.titre, self.etatInitial, self.etatFinals, self.mode]


class MachineDeTuring:
    def __init__(self, fichier, probleme, N=100):
        "initialisation de la machine avec le probleme et le transitionsrmme"
        self.tete = N//2
        self.probleme = probleme
        self.ruban = ''.join('#'*self.tete)+self.probleme+''.join('#'*self.tete)
        self.automate = Automate(fichier)
        self.titre = self.automate.getInformations()[0]
        self.transitions = self.automate.getTransitions()
        self.etatInitial = self.automate.etatInitial
        self.etatFinals = self.automate.etatFinals
        self.mode = self.automate.mode


    def afficherInstruction(self, i):
        "cette methode permet d'afficher une itération de la machine"
        print(self.ruban)
        print(''.join(' '*i)+'^')
        print("etat courant :" + self.etatCourant)


    def execution(self):
        "execution du transitionsramme sur la machine "
        i = self.tete
        self.etatCourant = self.etatInitial
        while self.etatCourant not in self.etatFinals:
            if self.transitions.__contains__((self.etatCourant, self.ruban[i])) == True:
                self.ruban = list(self.ruban)
                val1 = self.ruban[i]
                self.ruban[i] = self.transitions[(self.etatCourant, self.ruban[i])][1]
                self.ruban = ''.join(self.ruban)
                self.afficherInstruction(i)
                if(self.transitions[(self.etatCourant, val1)][2] == 'R'):
                    i = i+1
                elif(self.transitions[(self.etatCourant, val1)][2] == 'L'):
                    i = i-1
                self.etatCourant = self.transitions[(self.etatCourant, val1)][0]
                print("etat suivant : "+self.etatCourant)
                print("-------------------------------------------")
                time.sleep(1)

            else:
                if(self.mode == "accepteur"):
                    print("le mot n'est pas roconnue")
                break
        if(self.etatCourant in self.etatFinals and self.mode == "accepteur"):
            print("le mot est rocconue")
        
    def console(self):
        print('------------------------- ' + self.titre + '------------')
        print()
        self.execution()

#Automate("aNbN.txt")
MachineDeTuring("aNbNcN.txt","aabbcc").console()