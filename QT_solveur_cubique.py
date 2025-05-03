import sys
import numpy as np

from PyQt6 import QtCore
from PyQt6.QtCore import (QRegularExpression,
                          QSize, Qt, qVersion)
from PyQt6.QtGui import (QRegularExpressionValidator, QPalette,
                         QGuiApplication, QFont)
from PyQt6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QLabel,
    QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Recherche des racines cubiques")
        self.setWindowOpacity(0.95)
        w = 450
        h = 540
        self.setFixedSize(QSize(w, h))
        lineEditW = w - 47
        lineEditH = 25

        # Définition du style CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #7F7EE4;
            }
            GroupBox {
                color: white;
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton {
                color: white;
                background-color:
                           QLinearGradient(x0: 0, y0: 0,
                           x1: 1, y1: 1, stop: 0 #4444AA,
                           stop: 1 #CCCCFF);
                padding: 8px;
                border: none;
                border-radius: 8px;
                margin: 4px 0 0 0;
            }
            QPushButton:focus {
                border: 2px solid white;
                border-radius: 8px;
            }
            QPushButton:hover {
                color: black;
                font: bold;
                border: 2px solid white;
                border-radius: 8px;
            }
            QLabel {
                color: white;
            }
            QLineEdit{
                padding: 2px 2px;
                border-radius: 6px;
                border:2px solid white;
            }
        """)

        # Expression régulière        
        re = "-?(\\d+(\\.\\d*)?|\\d*\\.\\d+)"
        regex = QRegularExpression(re)
        validregex = QRegularExpressionValidator(regex)
        global_layout = QVBoxLayout()

        # Création du groupe pour les coefficients
        coefficientsGroupBox = QGroupBox("Coefficients")
        coefficientsGroupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vBoxLayoutCoefficients = QVBoxLayout()
        vBoxLayoutCoefficients.setSpacing(16)
        vBoxLayoutCoefficients.setContentsMargins(0, 4, 0, 4)

        # Construction des champs A, B, C, D
        a_label = QLabel("A")
        b_label = QLabel("B")
        c_label = QLabel("C")
        d_label = QLabel("D")
        self.a_lineedit = QLineEdit()
        self.b_lineedit = QLineEdit()
        self.c_lineedit = QLineEdit()
        self.d_lineedit = QLineEdit()
        self.a_lineedit.setTextMargins(0,0,4,0)
        self.b_lineedit.setTextMargins(0,0,4,0)
        self.c_lineedit.setTextMargins(0,0,4,0)
        self.d_lineedit.setTextMargins(0,0,4,0)
        self.a_lineedit.setPlaceholderText("...")
        self.b_lineedit.setPlaceholderText("...")
        self.c_lineedit.setPlaceholderText("...")
        self.d_lineedit.setPlaceholderText("...")

        # Couleur de fond des champs A, B, C, D
        bg_abcd = str("background: white; color: black; font-size:16px")
        self.a_lineedit.setStyleSheet(bg_abcd)
        self.b_lineedit.setStyleSheet(bg_abcd)
        self.c_lineedit.setStyleSheet(bg_abcd)
        self.d_lineedit.setStyleSheet(bg_abcd)
        self.a_lineedit.setFixedSize(lineEditW,lineEditH)
        self.b_lineedit.setFixedSize(lineEditW,lineEditH)
        self.c_lineedit.setFixedSize(lineEditW,lineEditH)
        self.d_lineedit.setFixedSize(lineEditW,lineEditH)

        # Alignement du texte pour les champs A, B, C, D
        lineEditAlignRight = Qt.AlignmentFlag.AlignRight
        self.a_lineedit.setAlignment(lineEditAlignRight)
        self.b_lineedit.setAlignment(lineEditAlignRight)
        self.c_lineedit.setAlignment(lineEditAlignRight)
        self.d_lineedit.setAlignment(lineEditAlignRight)
        # Application de la règle de l'expression régulière
        self.a_lineedit.setValidator(validregex)
        self.b_lineedit.setValidator(validregex)
        self.c_lineedit.setValidator(validregex)
        self.d_lineedit.setValidator(validregex)
        # Grouper le label avec le champ de saisie
        abcd_flayout = QFormLayout()
        abcd_flayout.addRow(a_label, self.a_lineedit)
        abcd_flayout.addRow(b_label, self.b_lineedit)
        abcd_flayout.addRow(c_label, self.c_lineedit)
        abcd_flayout.addRow(d_label, self.d_lineedit)

        # Création du groupe pour le discriminant et les trois racines
        resGroupBox = QGroupBox("Racines")
        resGroupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vBoxLayoutResultats = QVBoxLayout()
        vBoxLayoutResultats.setSpacing(12)
        vBoxLayoutResultats.setContentsMargins(0, 4, 0, 4)

        # Ce groupe contient 4 champs non éditables (delta, x1, x2, x3)
        disc_label = QLabel("\u0394")
        x1_label = QLabel(u"x\u2081")
        x2_label = QLabel(u"x\u2082")
        x3_label = QLabel(u"x\u2083")
        self.disc_lineedit = QLineEdit()
        self.x1_lineedit = QLineEdit()
        self.x2_lineedit = QLineEdit()
        self.x3_lineedit = QLineEdit()
        self.disc_lineedit.setTextMargins(0,0,4,0)
        self.x1_lineedit.setTextMargins(0,0,4,0)
        self.x2_lineedit.setTextMargins(0,0,4,0)
        self.x3_lineedit.setTextMargins(0,0,4,0)
        # Affiche la valeur 0 par défaut
        self.disc_lineedit.setPlaceholderText("0")
        self.x1_lineedit.setPlaceholderText("0")
        self.x2_lineedit.setPlaceholderText("0")
        self.x3_lineedit.setPlaceholderText("0")

        # Couleur de fond des champs Delta, x1, x2, x3 ne sont pas éditables
        bg_discx1x2x3 = str("background: white; color: red; font-size:16px")
        self.disc_lineedit.setStyleSheet(bg_discx1x2x3)
        self.x1_lineedit.setStyleSheet(bg_discx1x2x3)
        self.x2_lineedit.setStyleSheet(bg_discx1x2x3)
        self.x3_lineedit.setStyleSheet(bg_discx1x2x3)

        # Les champs Delta, x1, x2, x3 ne sont pas éditables,
        # de longueur fixe et le texte est aligné à droite
        self.disc_lineedit.setReadOnly(True)
        self.x1_lineedit.setReadOnly(True)
        self.x2_lineedit.setReadOnly(True)
        self.x3_lineedit.setReadOnly(True)
        self.disc_lineedit.setFixedSize(lineEditW,lineEditH)
        self.x1_lineedit.setFixedSize(lineEditW,lineEditH)
        self.x2_lineedit.setFixedSize(lineEditW,lineEditH)
        self.x3_lineedit.setFixedSize(lineEditW,lineEditH)
        self.disc_lineedit.setAlignment(lineEditAlignRight)
        self.x1_lineedit.setAlignment(lineEditAlignRight)
        self.x2_lineedit.setAlignment(lineEditAlignRight)
        self.x3_lineedit.setAlignment(lineEditAlignRight)
        # Grouper le label avec le champ de saisie
        dx1x2x3_flayout = QFormLayout()
        dx1x2x3_flayout.addRow(disc_label, self.disc_lineedit)
        dx1x2x3_flayout.addRow(x1_label, self.x1_lineedit)
        dx1x2x3_flayout.addRow(x2_label, self.x2_lineedit)
        dx1x2x3_flayout.addRow(x3_label, self.x3_lineedit)

        # Grouper les deux layouts (coef et racines)
        vBoxLayoutCoefficients.addLayout(abcd_flayout)
        vBoxLayoutCoefficients.addStretch(2)
        coefficientsGroupBox.setLayout(vBoxLayoutCoefficients)
        vBoxLayoutResultats.addLayout(dx1x2x3_flayout)
        resGroupBox.setLayout(vBoxLayoutResultats)

        # Apparence du caractère pour les boutons ci-dessous
        ft = QFont()
        ft.setPointSize(16)
        ft.setBold(True)
        ft.setUnderline(False)
        ft.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

        # Bouton Calculer (libellé, focus, style)
        computePushButton = QPushButton("Calculer")
        computePushButton.clicked.connect(self.Calculer)
        computePushButton.setFocus()
        computePushButton.setFont(ft)

        # Boutons Effacer, À propos et Quitter (libellé, focus, style)
        effacerPushButton = QPushButton("Effacer")
        effacerPushButton.clicked.connect(self.Effacer)
        aProposPushButton = QPushButton("À propos...")
        aProposPushButton.clicked.connect(self.aPropos)
        quitButton = QPushButton("Quitter")
        quitButton.clicked.connect(QApplication.instance().quit)
        quitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Ajout des quatre doutons à leur layout
        widget = QWidget()
        global_layout.addWidget(coefficientsGroupBox)
        global_layout.addWidget(resGroupBox)
        global_layout.addWidget(computePushButton)
        global_layout.addWidget(effacerPushButton)
        global_layout.addWidget(aProposPushButton)
        global_layout.addWidget(quitButton)
        widget.setLayout(global_layout)
        self.setCentralWidget(widget)

    # Fonction Calculer avec vérification de toutes les saisies
    def Calculer(self):
        # Est-ce que tous les champs sont simultanément vides ?
        if self.a_lineedit.text() == "" \
                and self.b_lineedit.text() == "" \
                and self.c_lineedit.text() == "" \
                and self.d_lineedit.text() == "":
            self.a_lineedit.setFocus()
            self.afficherErreurs("Tous les champs sont vides.")
            return
        
        # Est-ce que l'un des champ contient un zéro ?
        if self.a_lineedit.text() == "0" \
                or self.a_lineedit.text() == "-0" \
                or self.a_lineedit.text() == "0.0":
            self.a_lineedit.setFocus()
            self.afficherErreurs("A = 0 !")
            return
        if self.b_lineedit.text() == "0" \
                or self.b_lineedit.text() == "-0" \
                or self.b_lineedit.text() == "0.0":
            self.b_lineedit.setFocus()
            self.afficherErreurs("B = 0 !")
            return
        if self.c_lineedit.text() == "0" \
                or self.c_lineedit.text() == "-0" \
                or self.c_lineedit.text() == "0.0":
            self.c_lineedit.setFocus()
            self.afficherErreurs("C = 0 !")
            return
        if self.d_lineedit.text() == "0" \
                or self.d_lineedit.text() == "-0" \
                or self.d_lineedit.text() == "0.0":
            self.a_lineedit.setFocus()
            self.afficherErreurs("D = 0 !")
            return
        
        # Est-ce que l'un des champ est vide ?
        if not self.a_lineedit.text():
            self.afficherErreurs("La valeur A est manquante.")
            self.a_lineedit.setFocus()
            return
        if not self.b_lineedit.text():
            self.afficherErreurs("La valeur B est manquante.")
            self.b_lineedit.setFocus()
            return
        if not self.c_lineedit.text():
            self.afficherErreurs("La valeur C est manquante.")
            self.c_lineedit.setFocus()
            return
        if not self.d_lineedit.text():
            self.afficherErreurs("La valeur D est manquante.")
            self.d_lineedit.setFocus()
            return

        # Calcul des racines avec Numpy
        a = float(self.a_lineedit.text())
        b = float(self.b_lineedit.text())
        c = float(self.c_lineedit.text())
        d = float(self.d_lineedit.text())
        npp = np.polynomial.polynomial
        roots = npp.polyroots((d, c, b, a))
        prec = np.finfo(np.float128).precision
        x = np.round(roots, decimals=prec)

        # Calcul du discriminant
        disc = b**2 * c**2 - 4 * a * c**3 - 4 * b**3 * d \
                - 27 * a**2 * d**2 + 18 * a * b * c * d
        if np.equal(disc, 0.0):
            self.disc_lineedit.setText("0")
            self.x1_lineedit.setText(str(x[0].real))
            self.x2_lineedit.clear()
            self.x2_lineedit.setDisabled(True)
            self.x3_lineedit.clear()
            self.x3_lineedit.setDisabled(True)

        elif np.greater(disc, 0.0):
            self.disc_lineedit.setText(str(disc))
            tri = np.sort(x)
            self.x1_lineedit.setText(str(tri[0]))
            self.x2_lineedit.setText(str(tri[1]))
            self.x3_lineedit.setText(str(tri[2]))

        else:
            self.disc_lineedit.setText(str(disc))
            self.x1_lineedit.setText(str(x[0]))
            self.x2_lineedit.setText(str(x[1]))
            self.x3_lineedit.setText(str(x[2]))

    # Fonction qui vide le contenu de tous les champs
    def Effacer(self):
        self.a_lineedit.clear()
        self.b_lineedit.clear()
        self.c_lineedit.clear()
        self.d_lineedit.clear()
        self.disc_lineedit.clear()
        self.x1_lineedit.clear()
        self.x2_lineedit.clear()
        self.x3_lineedit.clear()
        self.disc_lineedit.clear()
        self.x1_lineedit.clear()
        self.x2_lineedit.clear()
        self.x3_lineedit.clear()
        if self.x2_lineedit.setEnabled(True) == False \
                and self.x3_lineedit.setEnabled(True) == False:
            self.x2_lineedit.setDisabled(True)
            self.x3_lineedit.setDisabled(True)
        self.a_lineedit.setFocus()

    # Fonction aPropos
    def aPropos(self):
        msg = str("Permet de rechercher les zéros d'un polynôme cubique.")
        mb = QMessageBox()
        mb.setText("Calcularoots v1.0")
        mb.setDetailedText(msg)
        mb.setStandardButtons(QMessageBox.StandardButton.Close)
        mb.setIcon(QMessageBox.Icon.Information)
        mb.exec()

    def afficherErreurs(self, msg):
        mb = QMessageBox(self)
        mb.setWindowTitle("Warning!")
        mb.setText(msg)
        mb.setStandardButtons(QMessageBox.StandardButton.Ok)
        mb.setIcon(QMessageBox.Icon.Critical)
        mb.exec()

def run():
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window,
                     QtCore.Qt.GlobalColor.lightGray)
    app.setStyle("Fusion")
    app.setPalette(palette)
    window = MainWindow()
    frame = window.frameGeometry()
    window.setWindowFlags(Qt.WindowType.NoDropShadowWindowHint)
    screen = QGuiApplication.primaryScreen()
    centre = screen.availableGeometry().center()
    frame.moveCenter(centre)
    window.show()
    app.exec()

if __name__ == '__main__':
    run()
