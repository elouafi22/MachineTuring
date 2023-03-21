from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys


class TuringMachineGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(800, 800)
        self.setWindowTitle("machine de Turing")
        # cree le widgets central
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.button = QPushButton("entree", self.centralWidget)
        self.button2 = QPushButton("importer", self.centralWidget)
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(400, 400, 800, 800)
        # Crée une vue graphique et ajoute la scène
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(400, 400, 900, 900)
        for i in range(10):
            cell = QGraphicsRectItem(40*i, 40, 40, 40)
            cell.setBrush(QBrush(Qt.white))
            self.scene.addItem(cell)

            value_text = QGraphicsTextItem(str(i))
            value_text.setPos(40*i + 15, 50)
            self.scene.addItem(value_text)
        # creation de la tete de lecture
        triangle = QGraphicsPolygonItem()
        triangle.setPolygon(
            QPolygonF([QPointF(45, 60), QPointF(20, 80), QPointF(65, 80)]))
        triangle.setPos(-20, 30)
        triangle.setBrush(QBrush(QColor(255, 0, 0)))
        triangle.setBrush(QBrush(QColor(255, 0, 0)))
        triangle.setPen(QPen(Qt.NoPen))
        self.scene.addItem(triangle)
        # ajouter la vue graphique dans le canvas principale
        self.hboxlayout = QHBoxLayout()
        self.hboxlayout.addStretch()
        self.hboxlayout.addWidget(self.view)
        self.hboxlayout.addStretch()
        self.qvbox = QVBoxLayout(self.centralWidget)
        self.qvbox.addLayout(self.hboxlayout)

        self.hboxlayout2 = QHBoxLayout()
        self.hboxlayout2.addStretch()
        self.hboxlayout2.addWidget(self.button)
        self.hboxlayout2.addWidget(self.button2)
        self.hboxlayout2.addStretch()
        self.qvbox.addLayout(self.hboxlayout2)
        self.button.clicked.connect(self.onPushButtonOkClicked)
        self.button2.clicked.connect(self.action_ouvrirFichier)

        # methode pour ouvrir un fichier
    @pyqtSlot()
    def action_ouvrirFichier(self):
        "methode permet d'ouvrir un fichier "
        fichier, filte = QFileDialog.getOpenFileName(
            self, "Selectionner un fichier pour importer", "", "les ficier texte (*.txt)")
        var = ""
        if fichier:
            var = "le fichier est bien importer"
        else:
            var = "le fichier n'exite pas"
        QMessageBox.information(
            self, "inforation", fichier)

   # methode pour de quiter l'application
    def action_quiter(self):
        self.close()
   # methode permet de quiter une application selon un evenement
    def action_fermetEvenement(self,event):
        messageConfirmation="Etes-vous sur de vouloir quitter L'application"
        reponce=QMessageBox.question(sefl,"Confirmation",messageConfirmation,QMessageBox.Yes,QMessageBox.No)
        if QMessageBox.Yes:
            event.accept()
        if QMessageBox.No:
            event.ignore()
    
    # methode pemet d'ouvrir une sous fenetre
    def onPushButtonOkClicked(self):
        QMessageBox.information(self, "info", "bonjour tout le monde")


app = QApplication(sys.argv)
machine = TuringMachineGUI()
machine.show()
app.exec_()
