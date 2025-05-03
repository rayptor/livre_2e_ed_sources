import os
import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,
                            QFileDialog, QGridLayout, QHBoxLayout,
                            QVBoxLayout, QPushButton, QLineEdit,
                            QDial, QStyle, QLabel)
from PyQt6.QtMultimedia import QAudioOutput, QMediaMetaData, QMediaPlayer

class MP3Player(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Lecteur MP3")
        self.setFixedSize(400, 250)
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.isPlaying = False
        self.volume = 50
        self.dureeTotal = 0
        self.playicon = QApplication.style().standardIcon( \
            QStyle.StandardPixmap.SP_MediaPlay)
        self.pauseIcon = QApplication.style().standardIcon( \
            QStyle.StandardPixmap.SP_MediaPause)
        self.stopIcon = QApplication.style().standardIcon( \
            QStyle.StandardPixmap.SP_MediaStop)
        self.ouvrirPushButton = QPushButton("Ouvrir MP3...")
        self.playPushButton = QPushButton()
        self.playPushButton.setIcon(self.playicon)
        self.stopPushButton = QPushButton()
        self.stopPushButton.setIcon(self.stopIcon)
        self.titreLineEdit = QLineEdit()
        self.artisteLineEdit = QLineEdit()
        self.albumLineEdit = QLineEdit()
        self.dureeLineEdit = QLineEdit()
        self.titreLabel = QLabel("Titre :")
        self.artisteLabel = QLabel("Artiste :")
        self.albumLabel = QLabel("Album :")
        self.dureeLabel = QLabel("Durée :")
        self.volumeDial = QDial()
        self.volumeDial.setRange(0, 100)
        self.volumeDial.setValue(50)
        self.volumeLabel = QLabel("50%")
        self.titreLineEdit.setReadOnly(True)
        self.artisteLineEdit.setReadOnly(True)
        self.albumLineEdit.setReadOnly(True)
        self.dureeLineEdit.setReadOnly(True)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        baseVBoxLayout = QVBoxLayout(central_widget)
        buttonHBoxLayout = QHBoxLayout()
        buttonHBoxLayout.addWidget(self.ouvrirPushButton)
        buttonHBoxLayout.addWidget(self.playPushButton)
        buttonHBoxLayout.addWidget(self.stopPushButton)
        volumeHBoxLayout = QHBoxLayout()
        volumeHBoxLayout.addStretch()
        volumeHBoxLayout.addWidget(self.volumeDial)
        volumeHBoxLayout.addWidget(self.volumeLabel)
        volumeHBoxLayout.addStretch()
        display_layout = QGridLayout()
        display_layout.addWidget(self.titreLabel, 0, 0)
        display_layout.addWidget(self.titreLineEdit, 0, 1)
        display_layout.addWidget(self.artisteLabel, 1, 0)
        display_layout.addWidget(self.artisteLineEdit, 1, 1)
        display_layout.addWidget(self.albumLabel, 2, 0)
        display_layout.addWidget(self.albumLineEdit, 2, 1)
        display_layout.addWidget(self.dureeLabel, 4, 0)
        display_layout.addWidget(self.dureeLineEdit, 4, 1)
        baseVBoxLayout.addLayout(buttonHBoxLayout)
        baseVBoxLayout.addLayout(volumeHBoxLayout)
        baseVBoxLayout.addLayout(display_layout)
        self.ouvrirPushButton.clicked.connect(self.ouvrir_fichier_mp3)
        self.playPushButton.clicked.connect(self.lecture_pause)
        self.stopPushButton.clicked.connect(self.stop)
        self.player.durationChanged.connect(self.duree_piste)
        self.player.positionChanged.connect(self.maj_position)
        self.player.metaDataChanged.connect(self.maj_metadata)
        self.volumeDial.valueChanged.connect(self.ajuster_volume)
        self.audioOutput.setVolume(0.5)

    def ouvrir_fichier_mp3(self) -> None:
        cheminDacces, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir Fichier MP3", "", "Fichiers MP3 (*.mp3)"
        )
        if cheminDacces:
            self.player.setSource(QtCore.QUrl.fromLocalFile(cheminDacces))
            self.isPlaying = False
            self.playPushButton.setIcon(self.playicon)
            self.titreLineEdit.clear()
            self.artisteLineEdit.clear()
            self.albumLineEdit.clear()
            self.dureeLineEdit.clear()
            self.dureeTotal = 0

    def lecture_pause(self) -> None:
        if not self.player.source().isEmpty():
            if self.isPlaying:
                self.player.pause()
                self.playPushButton.setIcon(self.playicon)
                self.isPlaying = False
            else:
                self.player.play()
                self.playPushButton.setIcon(self.pauseIcon)
                self.isPlaying = True

    def stop(self) -> None:
        if not self.player.source().isEmpty():
            self.player.stop()
            self.playPushButton.setIcon(self.playicon)
            self.isPlaying = False
            dt = self.format_temps(self.dureeTotal)
            self.dureeLineEdit.setText(f"00:00 / {dt}")

    def maj_metadata(self) -> None:
        titre = self.player.metaData().value(QMediaMetaData.Key.Title)
        if titre:
            self.titreLineEdit.setText(str(titre))
        else:
            cheminDacces = self.player.source().toLocalFile()
            if cheminDacces:
                acces = os.path.splitext(os.path.basename(cheminDacces))[0]
                self.titreLineEdit.setText(acces)
            else:
                self.titreLineEdit.setText("Pas de fichier sélectionné")

        artiste = self.player.metaData().value(QMediaMetaData.Key.AlbumArtist)
        if artiste:
            self.artisteLineEdit.setText(str(artiste))
        else:
            self.artisteLineEdit.setText("Inconnu")

        album = self.player.metaData().value(QMediaMetaData.Key.AlbumTitle)
        if album:
            self.albumLineEdit.setText(str(album))
        else:
            self.albumLineEdit.setText("Inconnu")

    def format_temps(self, milliseconds) -> str:
        if milliseconds <= 0:
            return "00:00"
        seconds = milliseconds // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def duree_piste(self, duree) -> None:
        if duree > 0:
            self.dureeTotal = duree
            self.dureeLineEdit.setText(f"00:00 / {self.format_temps(duree)}")

    def maj_position(self, position) -> None:
        if self.dureeTotal > 0:
            champ1 = self.format_temps(position)
            champ2 = self.format_temps(self.dureeTotal)
            self.dureeLineEdit.setText(f"{champ1} / {champ2}")

    def ajuster_volume(self, valeur) -> None:
        if abs(valeur - self.volume) > 50:
            valeur = self.volume
            self.volumeDial.setValue(valeur)
        self.audioOutput.setVolume(valeur / 100.0)
        self.volumeLabel.setText(f"{valeur}%")
        self.volume = valeur


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtCore.QLoggingCategory.setFilterRules("qt.*=false")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QtCore.Qt.GlobalColor.black)
    app.setStyle("Fusion")
    app.setPalette(palette)
    player = MP3Player()
    player.show()
    sys.exit(app.exec())