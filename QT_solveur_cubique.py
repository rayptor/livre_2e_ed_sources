import sys
import numpy as np
from PyQt6 import QtCore
from PyQt6.QtCore import (QRegularExpression, QSize, Qt)
from PyQt6.QtGui import (QRegularExpressionValidator, QPalette,
                         QGuiApplication, QFont)
from PyQt6.QtWidgets import (QApplication, QFormLayout, QGroupBox, QLabel,
                             QLineEdit, QMainWindow, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FCQTA

class PlotWindow(QMainWindow):
    epsilon = sys.float_info.epsilon

    def __init__(self,
                 a: float,
                 b: float,
                 c: float,
                 d: float,
                 racines: np.ndarray,
                 parent=None
                 ) -> None:
        super(PlotWindow, self).__init__(parent)
        self.setWindowTitle("Tracé du polynôme cubique")
        self.setFixedSize(800, 600)
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FCQTA(self.figure)
        self.setCentralWidget(self.canvas)
        self.mpl(a, b, c, d, racines)

    def mpl(self,
            a: float,
            b: float,
            c: float,
            d: float,
            racines: np.ndarray
            ) -> None:
        ax = self.figure.add_subplot(111)
        racinesReelles = [r.real for r in racines if np.abs(r.imag) < self.epsilon]
        if len(racinesReelles) > 0:
            x_min = np.min(racinesReelles)
            x_max = np.max(racinesReelles)
            margin = max(np.fabs(x_min), np.fabs(x_max), 1.0)
            x_min -= margin
            x_max += margin
        else:
            scale = max(abs(a), abs(b), abs(c), abs(d))
            x_min, x_max = -5.0, 5.0
            if scale > self.epsilon:
                x_min *= scale / self.epsilon
                x_max *= scale / self.epsilon

        x = np.linspace(x_min, x_max, 1000)
        y = a * x**3 + b * x**2 + c * x + d

        ax.plot(x, y, label=f"{a}x³ + {b}x² + {c}x + {d}", color="yellow")
        ax.axhline(0, color="white", lw=0.5)
        ax.axvline(0, color="white", lw=0.5)

        if len(racinesReelles) > 0:
            yRoots = np.zeros_like(racinesReelles)
            ax.scatter(racinesReelles, yRoots, color="red", s=30, label="Racines")
            prec = np.finfo(np.float32).precision
            for racine in racinesReelles:
                racineFormat = f"{racine:.{prec}f}".rstrip("0").rstrip(".")
                ax.annotate(racineFormat, 
                            xy=(racine, 0), 
                            xytext=(10, 10),
                            textcoords="offset points",
                            color="white",
                            fontsize=14,
                            bbox=dict(boxstyle="round,pad=0.3", edgecolor="white", facecolor="black"))

        y_abs_max = np.max(np.abs(y))
        if y_abs_max > self.epsilon:
            ax.set_ylim(-y_abs_max / 10, y_abs_max / 10)

        ax.set_facecolor("#7F7EE4")
        ax.set_title("Graphique du polynôme cubique")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()
        self.figure.tight_layout()
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Recherche des racines cubiques")
        # self.setWindowOpacity(0.95)
        w, h = 450, 540
        self.setFixedSize(QSize(w, h))
        lineEditW, lineEditH = w - 47, 25
        self.calculFait = False

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
                background-color: QLinearGradient(x0: 0, y0: 0, x1: 1, y1: 1,
                                                 stop: 0 #4444AA, stop: 1 #CCCCFF);
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
            QLineEdit {
                padding: 2px 2px;
                border-radius: 6px;
                border: 2px solid white;
            }
        """)

        # Expression régulière
        # ne permet que les chiffres et le signe moins
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
        self.a_lineedit.setTextMargins(0, 0, 4, 0)
        self.b_lineedit.setTextMargins(0, 0, 4, 0)
        self.c_lineedit.setTextMargins(0, 0, 4, 0)
        self.d_lineedit.setTextMargins(0, 0, 4, 0)
        self.a_lineedit.setPlaceholderText("...")
        self.b_lineedit.setPlaceholderText("...")
        self.c_lineedit.setPlaceholderText("...")
        self.d_lineedit.setPlaceholderText("...")

        # Couleur de fond des champs A, B, C, D
        bg_abcd = "background: white; color: black; font-size:16px"
        self.a_lineedit.setStyleSheet(bg_abcd)
        self.b_lineedit.setStyleSheet(bg_abcd)
        self.c_lineedit.setStyleSheet(bg_abcd)
        self.d_lineedit.setStyleSheet(bg_abcd)
        self.a_lineedit.setFixedSize(lineEditW, lineEditH)
        self.b_lineedit.setFixedSize(lineEditW, lineEditH)
        self.c_lineedit.setFixedSize(lineEditW, lineEditH)
        self.d_lineedit.setFixedSize(lineEditW, lineEditH)

        # Alignement du texte pour les champs A, B, C, D
        lineEditAlignRight = Qt.AlignmentFlag.AlignRight
        self.a_lineedit.setAlignment(lineEditAlignRight)
        self.b_lineedit.setAlignment(lineEditAlignRight)
        self.c_lineedit.setAlignment(lineEditAlignRight)
        self.d_lineedit.setAlignment(lineEditAlignRight)

        # Application de l'expression régulière
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
        self.disc_lineedit.setTextMargins(0, 0, 4, 0)
        self.x1_lineedit.setTextMargins(0, 0, 4, 0)
        self.x2_lineedit.setTextMargins(0, 0, 4, 0)
        self.x3_lineedit.setTextMargins(0, 0, 4, 0)
        self.disc_lineedit.setPlaceholderText("0")
        self.x1_lineedit.setPlaceholderText("0")
        self.x2_lineedit.setPlaceholderText("0")
        self.x3_lineedit.setPlaceholderText("0")

        # Couleur de fond des champs Delta, x1, x2, x3 ne sont pas éditables
        bg_discx1x2x3 = "background: white; color: red; font-size:16px"
        self.disc_lineedit.setStyleSheet(bg_discx1x2x3)
        self.x1_lineedit.setStyleSheet(bg_discx1x2x3)
        self.x2_lineedit.setStyleSheet(bg_discx1x2x3)
        self.x3_lineedit.setStyleSheet(bg_discx1x2x3)

        # Les champs Delta, x1, x2, x3 ne sont pas éditables
        self.disc_lineedit.setReadOnly(True)
        self.x1_lineedit.setReadOnly(True)
        self.x2_lineedit.setReadOnly(True)
        self.x3_lineedit.setReadOnly(True)
        self.disc_lineedit.setFixedSize(lineEditW, lineEditH)
        self.x1_lineedit.setFixedSize(lineEditW, lineEditH)
        self.x2_lineedit.setFixedSize(lineEditW, lineEditH)
        self.x3_lineedit.setFixedSize(lineEditW, lineEditH)
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

        # Apparence du caractère pour les boutons
        ft = QFont()
        ft.setPointSize(16)
        ft.setBold(True)
        ft.setUnderline(False)
        ft.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

        # Bouton Calculer
        computePushButton = QPushButton("Calculer")
        computePushButton.clicked.connect(self.calcul_des_racines)
        computePushButton.setFocus()
        computePushButton.setFont(ft)

        # Bouton Graphique
        graphPushButton = QPushButton("Graphique")
        graphPushButton.clicked.connect(self.graphique)
        graphPushButton.setFont(ft)

        # Boutons Effacer, À propos et Quitter
        effacerPushButton = QPushButton("Effacer")
        effacerPushButton.clicked.connect(self.effacer)
        effacerPushButton.setFont(ft)
        aProposPushButton = QPushButton("À propos...")
        aProposPushButton.clicked.connect(self.a_propos)
        aProposPushButton.setFont(ft)
        quitButton = QPushButton("Quitter")
        quitButton.clicked.connect(QApplication.instance().quit)
        quitButton.setFont(ft)
        quitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Ajout des boutons à leur layout
        widget = QWidget()
        global_layout.addWidget(coefficientsGroupBox)
        global_layout.addWidget(resGroupBox)
        global_layout.addWidget(computePushButton)
        global_layout.addWidget(graphPushButton)
        global_layout.addWidget(effacerPushButton)
        global_layout.addWidget(aProposPushButton)
        global_layout.addWidget(quitButton)
        widget.setLayout(global_layout)
        self.setCentralWidget(widget)

    def calcul_des_racines(self) -> None:
        if self.a_lineedit.text() == "" and self.b_lineedit.text() == "" \
                and self.c_lineedit.text() == "" and self.d_lineedit.text() == "":
            self.a_lineedit.setFocus()
            self.afficher_erreurs("Tous les champs sont vides !")

        zEros = ("0", "-0", "0.0")
        if self.a_lineedit.text() in zEros:
            self.a_lineedit.setFocus()
            self.afficher_erreurs("A = 0 !")
            return

        if self.b_lineedit.text() in zEros:
            self.b_lineedit.setFocus()
            self.afficher_erreurs("B = 0 !")
            return

        if self.c_lineedit.text() in zEros:
            self.c_lineedit.setFocus()
            self.afficher_erreurs("C = 0 !")
            return

        if self.d_lineedit.text() in zEros:
            self.d_lineedit.setFocus()
            self.afficher_erreurs("D = 0 !")
            return

        strValManquante = "La valeur {} est manquante."
        if not self.a_lineedit.text():
            self.afficher_erreurs(strValManquante.format("A"))
            self.a_lineedit.setFocus()
            return

        if not self.b_lineedit.text():
            self.afficher_erreurs(strValManquante.format("B"))
            self.b_lineedit.setFocus()
            return

        if not self.c_lineedit.text():
            self.afficher_erreurs(strValManquante.format("C"))
            self.c_lineedit.setFocus()
            return

        if not self.d_lineedit.text():
            self.afficher_erreurs(strValManquante.format("D"))
            self.d_lineedit.setFocus()
            return

        a = float(self.a_lineedit.text())
        b = float(self.b_lineedit.text())
        c = float(self.c_lineedit.text())
        d = float(self.d_lineedit.text())
        coefs = np.array([a, b, c, d])
        npp = np.polynomial.polynomial
        roots = npp.polyroots(coefs[::-1])
        npPrec = np.finfo(np.float64).precision
        npEps = np.finfo(np.float64).eps
        x = np.round(roots, decimals=npPrec)

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
            tri = np.sort(np.real_if_close(x, tol=npEps))
            self.x1_lineedit.setText(str(tri[0]))
            self.x2_lineedit.setText(str(tri[1]))
            self.x3_lineedit.setText(str(tri[2]))
        else:
            self.disc_lineedit.setText(str(disc))
            for i, root in enumerate(x):
                if np.abs(root.imag) < npEps:
                    formatRoot = f"{root.real:.{npPrec}f}".rstrip("0").rstrip(".")
                else:
                    formatRoot = str(root)
                if i == 0:
                    self.x1_lineedit.setText(formatRoot)
                elif i == 1:
                    self.x2_lineedit.setText(formatRoot)
                elif i == 2:
                    self.x3_lineedit.setText(formatRoot)

        self.calculFait = True
        self.coef_a = a
        self.coef_b = b
        self.coef_c = c
        self.coef_d = d
        self.racines = roots

    def graphique(self) -> None:
        if not self.calculFait:
            self.calcul_des_racines()

        plot_window = PlotWindow(self.coef_a, self.coef_b,
                                 self.coef_c, self.coef_d,
                                 self.racines, self)
        plot_window.show()

    def effacer(self) -> None:
        self.a_lineedit.clear()
        self.b_lineedit.clear()
        self.c_lineedit.clear()
        self.d_lineedit.clear()
        self.disc_lineedit.clear()
        self.x1_lineedit.clear()
        self.x2_lineedit.clear()
        self.x3_lineedit.clear()
        self.x2_lineedit.setEnabled(True)
        self.x3_lineedit.setEnabled(True)
        self.a_lineedit.setFocus()
        self.calculFait = False

    def a_propos(self) -> None:
        mb = QMessageBox()
        mb.setWindowTitle("À propos")
        mb.setText("Polyz v1.0\nRecherche les zéros d'un polynôme cubique.")
        mb.setStandardButtons(QMessageBox.StandardButton.Close)
        mb.setIcon(QMessageBox.Icon.Information)
        mb.exec()

    def afficher_erreurs(self, msg) -> None:
        mb = QMessageBox(self)
        mb.setWindowTitle("Attention !")
        mb.setText(msg)
        mb.setStandardButtons(QMessageBox.StandardButton.Ok)
        mb.setIcon(QMessageBox.Icon.Critical)
        mb.exec()

def main() -> None:
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QtCore.Qt.GlobalColor.lightGray)
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

if __name__ == "__main__":
    main()
