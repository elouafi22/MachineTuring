from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from machineModule import *
from PyQt5 import QtCore
import time

# cette class definie la tete de lecture


class teteLecture(QGraphicsObject):
    def __init__(self):
        super(teteLecture, self).__init__()

    def boundingRect(self):
        return QRectF(0, 0, 100, 30)

    def paint(self, painter, option, widget=None):
        painter.setBrush(Qt.red)
        # Déplacez le triangle au centre de la boîte englobante
        painter.drawPolygon(
            QPolygonF([QPointF(50, 0), QPointF(0, 30), QPointF(100, 30)]))

    def deplasserTete(self, x, y):
        "methode permet de deplacer la tete de lecture"
        self.setPos(x, y)

# cette class definir l'affichage de la table de transition


class TableTransition(QTableWidget):
    def __init__(self, transitions):
        super().__init__()
        nRows, nColumns = len(transitions), 5
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)
        header = self.horizontalHeader()
        header.setStyleSheet("background-color: gray;")
        self.titreTabtransition=['Etat', 'Lit', 'Ecrit', 'Déplacement', 'Nouvel Etat']
        self.setHorizontalHeaderLabels(self.titreTabtransition)
        #item.setBackground(QColor(255, 0, 0))
        i = 0
        for key, val in transitions.items():
            self.setItem(i, 0, QTableWidgetItem(key[0]))
            self.setItem(i, 1, QTableWidgetItem(key[1]))
            self.setItem(i, 2, QTableWidgetItem(val[1]))
            self.setItem(i, 3, QTableWidgetItem(val[2]))
            self.setItem(i, 4, QTableWidgetItem(val[0]))
            i += 1

        self.previous_row=-1
        self.previous_column=-1  
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.itemSelectionChanged.connect(self.change_color_selected)
    
           
    def change_color_selected(self):
        current_row=self.currentRow()
        current_column=self.currentColumn()
        if current_row >= 0 and current_column >= 0:
            # Changement de couleur de la cellule précédemment sélectionnée
            if self.previous_row >= 0 and self.previous_column >= 0:
                item = self.item(self.previous_row, self.previous_column)
                item.setBackground(QColor(255, 255, 255))

            # Changement de couleur de la nouvelle cellule sélectionnée
            item = self.item(current_row, current_column)
            item.setBackground(QColor(255, 0, 0))

            self.previous_row = current_row
            self.previous_column = current_column
          
          


class machineInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Machine de Turing")
        # self.setFixedSize(1080, 720)
        self.resize(1080, 720)
        # self.setStyleSheet("background-color: #E7F7F7;")

        # definition des font utiler
        fonttitre = QFont()
        fonttitre.setPointSize(24)

        fontText = QFont()
        fontText.setPointSize(16)

        # creation du widget principale
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # creation du premiere ligne du box0 qui contient le titre du programme
        # a executer par default vide
        self.label_programme = QLabel("Nom programme")

        # création des trois niveaux de l'interface
        self.niveau1 = QHBoxLayout()
        self.niveau2 = QHBoxLayout()
        self.niveau3 = QHBoxLayout()
        self.niveau4 = QHBoxLayout()
        self.niveau5 = QHBoxLayout()
        self.niveau6 = QHBoxLayout()

        # création des widgets pour niveau 1
        self.label_programme = QLabel("Nom du programme")
        self.label_programme.setFont(fonttitre)

        # creation des widgets pour niveau 2
        self.label_etat = QLabel("Etat:")
        self.label_message = QLabel("Etat depart:")
        self.label_reponce = QLabel("")

        self.label_etat.setFont(fontText)
        self.label_message.setFont(fontText)
        self.label_reponce.setFont(fontText)

        # creation des widgets pour niveau 3
        self.scene = QGraphicsScene()
        self.vue = QGraphicsView(self.scene)
        self.vue.resize(1080, 720)
        self.rectPrincipal = self.scene.addRect(self.scene.sceneRect())
        self.vue.setScene(self.scene)
        self.vue.fitInView(self.rectPrincipal, Qt.KeepAspectRatio)

        self.rect_width = 60
        self.rect_height = 60
        self.rect_gap = 5
        self.rect_count = 8
        self.cells = []
        self.ruban = "#"*16
            

        # création du ruban et initialisation
        self.initialiserRuban()
            
        # creation de la tete de lecture
        
        self.creationTetelecture()
        
        self.transitions = {}

        # creation des widgets pour niveau 4
        self.lineEditProbleme = QLineEdit()
        self.buttonValider = QPushButton("valider")
        self.buttonChoisirProgramme = QPushButton("Choisir Programme")

        # creation des widgets pour niveau 5
        self.buttonCommencer = QPushButton("Commencer")
        self.buttonPause = QPushButton("Pause")
        self.buttonRecommancer = QPushButton("Recommencer")

        # niveau1
        self.niveau1.addStretch()
        self.niveau1.addWidget(self.label_programme)
        self.niveau1.addStretch()

        # niveau2
        self.niveau2.addSpacing(10)
        self.niveau2.addWidget(self.label_etat)
        self.niveau2.addStretch()
        self.niveau2.addWidget(self.label_message)
        self.niveau2.addStretch()
        self.niveau2.addWidget(self.label_reponce)
        self.niveau2.addSpacing(10)
        # niveau3
        self.niveau3.addSpacing(10)
        self.niveau3.addWidget(self.vue)
        self.niveau3.addSpacing(10)

        # niveau4
        self.niveau4.addStretch()
        self.niveau4.addWidget(self.lineEditProbleme)
        self.niveau4.addWidget(self.buttonValider)
        self.niveau4.addSpacing(10)
        self.niveau4.addWidget(self.buttonChoisirProgramme)
        self.niveau4.addStretch()

        # niveau5
        self.niveau5.addStretch()
        self.niveau5.addWidget(self.buttonCommencer)
        self.niveau5.addSpacing(10)
        self.niveau5.addWidget(self.buttonPause)
        self.niveau5.addSpacing(10)
        self.niveau5.addWidget(self.buttonRecommancer)
        self.niveau5.addStretch()
        self.tableTransition = None

        # ajout des niveaux à la fenêtre
        self.box0 = QVBoxLayout(self.central_widget)
        self.box0.addLayout(self.niveau1)
        self.box0.addSpacing(20)
        self.box0.addLayout(self.niveau2)
        self.box0.addSpacing(50)
        self.box0.addLayout(self.niveau3)
        self.box0.addSpacing(10)
        self.box0.addLayout(self.niveau6)
        self.box0.addSpacing(10)
        self.box0.addLayout(self.niveau4)
        self.box0.addSpacing(20)
        self.box0.addLayout(self.niveau5)

        # ajouter les evenement pour les button
        self.buttonCommencer.clicked.connect(self.execution)
        self.buttonChoisirProgramme.clicked.connect(self.chargerProgramme)
        self.buttonValider.clicked.connect(self.ajouterProblemeAuRubban)
        self.buttonRecommancer.clicked.connect(self.rocommencer)
        
#methode permet de cree la tete de lecture 
    def creationTetelecture(self):
        self.triangle = teteLecture()
        self.triangle.setPos(-20, 0)
        self.scene.addItem(self.triangle)
        self.vue.ensureVisible(self.triangle, 50, 50)
 
# creation d'un objet de type QGraphicsTextItem
    def creationObjetQgraphicsText(self,caractere,position):
        "cette methode permet de creer un objet de type QGraphicsTextItem et de le positionner"
        rect = self.scene.addRect(position * (self.rect_width + self.rect_gap), self.decalge, self.rect_width,
                                      self.rect_height, pen=QPen(QColor("white")), brush=QBrush(QColor("#33B9FF")))
        text = QGraphicsTextItem(caractere)
        text.setFont(QFont("Arial", 25))
        text_rect = text.boundingRect()
        text.setDefaultTextColor(QColor("white"))
        text_x = position * (self.rect_width + self.rect_gap) + \
                (self.rect_width - text_rect.width()) / 2
        text_y = ((self.rect_height - text_rect.height()) / 2)+self.decalge
        text.setPos(text_x, text_y)
        self.scene.addItem(text)
        self.cells.append(text)

#methode permet d'initialiser le ruban 
    def initialiserRuban(self):
        self.cells = []
        self.decalge = -70
        for i in range(self.rect_count):
            self.creationObjetQgraphicsText("#",i)

# mathode permet d'ajouter la table de transition

    def chargerProgramme(self):
        self.fichier, filte = QFileDialog.getOpenFileName(
            self, "Selectionner un fichier pour importer", "", "les ficier texte (*.txt)")
        var = ""
        if self.fichier:
            var = "le fichier est bien importer"
        else:
            var = "le fichier n'exite pas"
        QMessageBox.information(
            self, "inforation", var)
        # cree une intance de la class automate
        self.automate = Automate(self.fichier)

        # cree une instance de la class tableTransition
        self.transitions = self.automate.getTransitions()
        self.tableTransition = TableTransition(self.transitions)

        self.label_programme.setText(self.automate.getInformations()[0])
        self.etaIital = self.automate.getInformations()[1]
        self.etatFinals = self.automate.getInformations()[2]
        self.mode = self.automate.getInformations()[3]
        self.etatCourant = self.etaIital

        self.label_etat.setText("Etat : "+self.etaIital)
        self.label_message.setText("Etat depart : "+self.etaIital)

        # niveau6
        self.niveau6.addSpacing(10)
        self.niveau6.addWidget(self.tableTransition)
        self.niveau6.addSpacing(10)

# methode permet d'ajouter une instance du prbleme au ruban

    def ajouterProblemeAuRubban(self):
     "Méthode permettant d'insérer le problème dans le ruban"
     self.tete = 4
     self.probleme = self.lineEditProbleme.text()
     if self.probleme.strip():
         for indice in range(len(self.probleme)):
            if indice < len(self.cells) - self.tete:
                self.cells[indice + self.tete].setPlainText(self.probleme[indice])
            else:
                self.creationObjetQgraphicsText(self.probleme[indice], indice + self.tete)
         self.triangle.setPos(self.tete * 60, 0)
         print(self.triangle.x())
     else:
        QMessageBox.information(self, "Information", "Entrez une valeur valide.")
        

# methode permet de recommencer l'execution 
    
    def rocommencer(self):
        self.etatCourant=self.etaIital
        
        for item in self.scene.items():
            self.scene.removeItem(item)
            
        self.creationTetelecture()
        self.initialiserRuban()
        self.ajouterProblemeAuRubban()
        print(self.probleme)
        print(self.tete)
        
#methode permet de pauser l'execution du programme 
    
    def pause(self):
        pass


# methode permet de deplacer la tete le delecture

    def deplacementRuban(self, R):
        vitesse = 1000  # controler la vitesse d'animation
        print(self.triangle.pos().x())
        self.animation = QPropertyAnimation(
            self.triangle, b'pos')  # remplacer l'objet d'animation
        self.triangle.update()
        self.animation.setDuration(vitesse)
        self.animation.setStartValue(
            QPointF(self.triangle.pos().x(), self.triangle.pos().y()))
        if R == "R":
            self.animation.setEndValue(
                QPointF(self.triangle.pos().x()+65, self.triangle.pos().y()))
        else:
            self.animation.setEndValue(
                QPointF(self.triangle.pos().x()-65, self.triangle.pos().y()))

        # self.animation.setLoopCount(-1)
        self.triangle.update()
        self.animation.finished.connect(self.execution)
        self.animation.start()
        position = QPointF(self.triangle.pos().x(), 0)
        self.vue.centerOn(QPointF(self.triangle.pos().x(), 0))

# methode permet d'executer les instructions de la table de transition
    def execution(self):
        val = 1  # controler la vitesse d'execution
        "execution des instruction da la table de transition sur la la machine"
        if self.etatCourant not in self.etatFinals:
            
            if self.tete>=len(self.cells):
                  self.creationObjetQgraphicsText('#',self.tete) #creation d'une nouvelle case si on a arriver a la fin du ruban
                  
            cle =(self.etatCourant, self.cells[self.tete].toPlainText())
            self.transition = self.transitions.get(cle, None)
            self.getposition(cle,'Etat')
        
            #['Etat', 'Lit', 'Ecrit', 'Déplacement', 'Nouvel Etat']
            self.getposition(cle,'Lit')
            if self.transition:
                self.deplacementRuban(self.transition[2]) #! deplacement la tete de lecture
                
                self.getposition(cle,'Ecrit')
                self.cells[self.tete].setPlainText(self.transition[1])

                if(self.transition[2] == 'R'):
                    self.tete += 1
                    self.getposition(cle,'Déplacement')
                    
                elif(self.transition[2] == 'L'):
                    self.tete -= 1
                    self.getposition(cle,'Déplacement')
                    
                self.etatCourant = self.transition[0]
                self.label_etat.setText("Etat : "+self.transition[0])
                self.getposition(cle,'Nouvel Etat')
                time.sleep(val)
            else:
                if (self.mode == "reconnaisseur"):
                    self.label_reponce.setText("n'est pas reconnu")
                    self.label_reponce.setStyleSheet("color: red;")
                # break
        if self.etatCourant in self.etatFinals and self.mode == "reconnaisseur":
            self.label_reponce.setText("reconnu")
            self.label_reponce.setStyleSheet("color: green;")
        
# autre methode pour l'aide
    def getposition(self,cle,valeur):
        "methode permet de returner la position de la case en cour de traiter"
        line=list(self.transitions.keys()).index(cle)
        colone=self.tableTransition.titreTabtransition.index(valeur)
        self.tableTransition.setCurrentCell(line,colone)
        
        #['Etat', 'Lit', 'Ecrit', 'Déplacement', 'Nouvel Etat']
        if valeur==2:
         self.label_message.setText(
                "Symbole lit : "+self.cells[self.tete].toPlainText())
        elif valeur==3:
            self.label_message.setText("Symbole ecrit : "+self.transition[1])
        elif valeur==4 and self.transition[2] == 'R':
            self.label_message.setText(
                      "Mouvement de rubant : vers la droite")
        elif valeur==4 and self.transition[2] == 'L':
            self.label_message.setText(
                      "Mouvement de rubant : vers la gauche")
        else:
            self.label_message.setText("Etat : "+self.transition[0])

app = QApplication(sys.argv)
machine = machineInterface()
machine.show()
app.exec_()


"""

        QGraphicsPolygonItem()
        self.triangle.setPolygon(
            QPolygonF([QPointF(30, 30), QPointF(10, 60), QPointF(50, 60)]))
        self.triangle.setPos(455,40)
        self.triangle.setBrush(QBrush(QColor(255, 0, 0)))
        self.triangle.setPen(QPen(Qt.NoPen))

        ------------------------------------------------------

        def deplacementRuban(self):
        start_pos = self.triangle.pos()
        print(f"Start position: {start_pos}")

        end_pos = QtCore.QPointF(start_pos.x() + 100, start_pos.y())
        print(f"End position: {end_pos}")

        animation = QtCore.QPropertyAnimation(self.triangle, b"pos")
        animation.setDuration(1500)
        animation.setStartValue(start_pos)
        animation.setEndValue(end_pos)
        animation.start()
----------------------------------------------------------------------------

def creationObjetQgraphicsText(self,caractere,position,decalge):
        "cette methode permet de creer un objet de type QGraphicsTextItem et de le positionner"
        rect = self.scene.addRect(position * (self.rect_width + self.rect_gap), decalge, self.rect_width,
                                      self.rect_height, pen=QPen(QColor("white")), brush=QBrush(QColor("#33B9FF")))
        text = QGraphicsTextItem(caractere)
        text.setFont(QFont("Arial", 25))
        text_rect = text.boundingRect()
        text.setDefaultTextColor(QColor("white"))
        text_x = position * (self.rect_width + self.rect_gap) + \
                (self.rect_width - text_rect.width()) / 2
        text_y = ((self.rect_height - text_rect.height()) / 2)+decalge
        text.setPos(text_x, text_y)
        self.scene.addItem(text)
        self.cells.append(text)

        ----------------------------------------------


   # créer une animation qui déplace les cellules de droite à gauche
   for i in range(self.rect_count):
        animation = QPropertyAnimation(self.cells[i], b"pos")
 # durée de l'animation en millisecondes
        animation.setDuration(1000)
        start_pos = QPoint(i * (self.rect_width + self.rect_gap), 0)
        end_pos = QPoint((i - 1) * (self.rect_width + self.rect_gap), 0)
        animation.setStartValue(start_pos)

        animation.setEndValue(end_pos)
        animation.start()

        ----------------------------------------

           for item in self.cells:
            if self.j < (len(self.ruban)):
                item.setPlainText(self.ruban[self.j])
                self.j += 1

    self.j = 1
    self.j += self.cmt
    print("apeler la ", self.j)
    self.cmt += 1

"""
