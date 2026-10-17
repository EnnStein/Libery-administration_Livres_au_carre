import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
from PyQt6.QtPrintSupport import *

def widget_at(grid_layout, target_row, target_column):
    for index in range(grid_layout.count()):
        item = grid_layout.itemAt(index)
        row, column, row_span, column_span = grid_layout.getItemPosition(index)

        # Prüft auch Widgets, die mehrere Zellen überspannen.
        if (row <= target_row < row + row_span
                and column <= target_column < column + column_span):
            return item.widget()  # None, wenn das Element ein Layout ist
    return None

#Funktion, die Großbuchstaben in Kleinbuchstaben umwandelt
def grossKlein(Text):
    Grossbuchstaben = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    Kleinbuchstaben = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    Ausgabe = ""
    for x in Text:
        if x in Grossbuchstaben:
            Ausgabe += Kleinbuchstaben[Grossbuchstaben.index(x)]
        else:
            Ausgabe += x
    return Ausgabe


class MainWindow(QMainWindow):
    Schriftgroesse = 12
    Schriftart = "Arial"

    def __init__(self):
        super().__init__()
        self.datenLaden()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(600, 400)
        self.setWindowTitle("Livres au carré - Bibliotheksverwaltung")

        self.setup()
        self.createActions()
        self.createMenu()
        self.createToolBar()
        self.showFullScreen()

    def setup(self):
        self.Zentral_Widget = QWidget()
        self.setCentralWidget(self.Zentral_Widget)

        Leer = QWidget()

        Ausleih_Container = self.ausleiheErstellen()

        Abgabe_Container = self.abgabeErstellen()

        Katalog_Container = self.katalogErstellen()

        Kunden_Container = self.kundenErstellen()

        Faelligkeiten_Container = self.faelligkeitsBerichtErstellen()

        Einstell_Container = self.einstellungenErstellen()

        Hilfe_Container = self.hilfeErstellen()

        self.stacked = QStackedLayout()
        self.stacked.addWidget(Leer)
        self.stacked.addWidget(Ausleih_Container)
        self.stacked.addWidget(Abgabe_Container)
        self.stacked.addWidget(Faelligkeiten_Container)
        self.stacked.addWidget(Katalog_Container)
        self.stacked.addWidget(Kunden_Container)
        self.stacked.addWidget(Einstell_Container)
        self.stacked.addWidget(Hilfe_Container)
        self.stacked.setCurrentIndex(0)

        self.Zentral_Widget.setLayout(self.stacked)

    def ausleiheErstellen(self):
        Ausleih_VBox = QVBoxLayout()
        self.Ausleih_Anzeige = QLabel("Ausleihe")
        self.Ausleih_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Ausleih_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        Ausleih_VBox.addWidget(self.Ausleih_Anzeige, alignment=Qt.AlignmentFlag.AlignTop)

        self.Ausleih_Buch_Anzeige = QLabel("BuchID:")
        self.Ausleih_Buch_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Ausleih_Kunde_Anzeige = QLabel("KundenID:")
        self.Ausleih_Kunde_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Ausleih_Buch_Edit = QLineEdit()
        self.Ausleih_Buch_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Ausleih_Kunde_Edit = QLineEdit()
        self.Ausleih_Kunde_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Ausleih_Knopf = QPushButton("ausleihen")
        self.Ausleih_Knopf.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Ausleih_Knopf.setStyleSheet("background-color: lightblue")
        self.Ausleih_Knopf.clicked.connect(self.ausleihen)

        Ausleih_Form = QFormLayout()
        Ausleih_Form.addRow(self.Ausleih_Buch_Anzeige, self.Ausleih_Buch_Edit)
        Ausleih_Form.addRow(self.Ausleih_Kunde_Anzeige, self.Ausleih_Kunde_Edit)

        Ausleih_VBox.addLayout(Ausleih_Form)
        Ausleih_VBox.addWidget(self.Ausleih_Knopf, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.Ausleih_Container = QWidget()
        self.Ausleih_Container.setLayout(Ausleih_VBox)

        return self.Ausleih_Container

    def abgabeErstellen(self):

        Abgabe_VBox = QVBoxLayout()

        self.Abgabe_Anzeige = QLabel("Abgabe")
        self.Abgabe_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Abgabe_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.Abgabe_Auswahl_Anzeige = QLabel("Auswahl")
        self.Abgabe_Auswahl_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*2))
        self.Abgabe_Auswahl_Anzeige.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Abgbae_Aktualisieren_Knopf = QPushButton("aktualisieren")
        self.Abgbae_Aktualisieren_Knopf.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Abgbae_Aktualisieren_Knopf.setStyleSheet("background-color: lightblue")
        self.Abgbae_Aktualisieren_Knopf.clicked.connect(self.abgabeSuchen)

        self.Abgabe_BuchID_Anzeige = QLabel("Buch-ID:")
        self.Abgabe_BuchID_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Abgabe_KundenID_Anzeige = QLabel("Kunden-ID:")
        self.Abgabe_KundenID_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Abgabe_BuchID_Edit = QLineEdit()
        self.Abgabe_BuchID_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Abgabe_KundenID_Edit = QLineEdit()
        self.Abgabe_KundenID_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        Abgabe_Auswahl_Form = QFormLayout()
        Abgabe_Auswahl_Form.addRow(self.Abgabe_BuchID_Anzeige, self.Abgabe_BuchID_Edit)
        Abgabe_Auswahl_Form.addRow(self.Abgabe_KundenID_Anzeige, self.Abgabe_KundenID_Edit)

        self.Abgabe_Suchen_Knopf = QPushButton("suchen")
        self.Abgabe_Suchen_Knopf.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Abgabe_Suchen_Knopf.setStyleSheet("background-color: lightblue")
        self.Abgabe_Suchen_Knopf.clicked.connect(self.abgabeSuchen)

        Abgabe_Auswahl_VBox = QVBoxLayout()
        Abgabe_Auswahl_VBox.addWidget(self.Abgabe_Auswahl_Anzeige)
        Abgabe_Auswahl_VBox.addLayout(Abgabe_Auswahl_Form)
        Abgabe_Auswahl_VBox.addWidget(self.Abgabe_Suchen_Knopf, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.Abgabe_Treffer_Anzeige = QLabel("Trefferliste")
        self.Abgabe_Treffer_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*2))
        self.Abgabe_Treffer_Anzeige.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.Abgabe_AusleihID_Anzeige = QLabel("Ausleih-ID")
        self.Abgabe_AusleihID_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Abgabe_BuchID_Anzeige = QLabel("Buch-ID")
        self.Abgabe_BuchID_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Abgabe_Buch_Name_Anzeige = QLabel("Buch-Titel")
        self.Abgabe_Buch_Name_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Abgabe_KundeID_Anzeige = QLabel("Kunden-ID")
        self.Abgabe_KundeID_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Abgabe_Kunde_Name_Anzeige = QLabel("Kunden-Name")
        self.Abgabe_Kunde_Name_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Faelligkeit_Anzeige = QLabel("Fälligkeitsdatum")
        self.Faelligkeit_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Abgeben_Anzeige = QLabel("abgeben")
        self.Abgeben_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Abgabe_Treffer_Tabelle = QGridLayout()
        self.Abgabe_Treffer_Tabelle.addWidget(self.Abgabe_AusleihID_Anzeige, 0, 0)
        self.Abgabe_Treffer_Tabelle.addWidget(self.Abgabe_BuchID_Anzeige, 0, 1)
        self.Abgabe_Treffer_Tabelle.addWidget(self.Abgabe_Buch_Name_Anzeige, 0, 2)
        self.Abgabe_Treffer_Tabelle.addWidget(self.Abgabe_KundeID_Anzeige, 0, 3)
        self.Abgabe_Treffer_Tabelle.addWidget(self.Abgabe_Kunde_Name_Anzeige, 0, 4)
        self.Abgabe_Treffer_Tabelle.addWidget(self.Faelligkeit_Anzeige, 0, 5)
        self.Abgabe_Treffer_Tabelle.addWidget(self.Abgeben_Anzeige, 0, 6)

        Abgabe_Treffer_VBox = QVBoxLayout()
        Abgabe_Treffer_VBox.addWidget(self.Abgabe_Treffer_Anzeige)
        Abgabe_Treffer_VBox.addLayout(self.Abgabe_Treffer_Tabelle)

        Abgabe_VBox.addWidget(self.Abgabe_Anzeige, alignment=Qt.AlignmentFlag.AlignTop)
        Abgabe_VBox.addLayout(Abgabe_Auswahl_VBox)
        Abgabe_VBox.addLayout(Abgabe_Treffer_VBox)
        Abgabe_VBox.addWidget(self.Abgbae_Aktualisieren_Knopf, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.Abgabe_Container = QWidget()
        self.Abgabe_Container.setLayout(Abgabe_VBox)

        return self.Abgabe_Container

    def katalogErstellen(self):
        Katalog_VBox = QVBoxLayout()
        self.Katalog_Anzeige = QLabel("Katalog")
        self.Katalog_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Katalog_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        Katalog_VBox.addWidget(self.Katalog_Anzeige, alignment=Qt.AlignmentFlag.AlignTop)

        self.Buecher_Grid = QGridLayout()

        Katalog_Such_HBox = QHBoxLayout()
        self.Katalog_Suchleiste = QLineEdit()
        self.Katalog_Suchleiste.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Katalog_Suchleiste.setClearButtonEnabled(True)
        Katalog_Such_HBox.addWidget(self.Katalog_Suchleiste)
        self.Katalog_Suchen_Knopf = QPushButton("suchen")
        self.Katalog_Suchen_Knopf.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Katalog_Suchen_Knopf.setStyleSheet("background-color: lightblue")
        self.Katalog_Suchen_Knopf.clicked.connect(self.suchen)
        Katalog_Such_HBox.addWidget(self.Katalog_Suchen_Knopf)
        Katalog_VBox.addLayout(Katalog_Such_HBox)

        BuchIDs = []
        self.query.exec("SELECT BuchID FROM Katalog")
        while self.query.next():
            wert = self.query.value(0)
            BuchIDs.append(wert)

        Titel = []
        self.query.exec("SELECT Titel FROM Katalog")
        while self.query.next():
            wert = self.query.value(0)
            Titel.append(wert)

        Autoren = []
        self.query.exec("SELECT Autor FROM Katalog")
        while self.query.next():
            wert = self.query.value(0)
            Autoren.append(wert)

        Genres = []
        self.query.exec("SELECT Genre FROM Katalog")
        while self.query.next():
            wert = self.query.value(0)
            Genres.append(wert)

        Bilder = []
        self.query.exec("SELECT Bild FROM Katalog")
        while self.query.next():
            wert = self.query.value(0)
            Bilder.append(wert)

        Anmerkungen = []
        self.query.exec("SELECT Anmerkungen FROM Katalog")
        while self.query.next():
            wert = self.query.value(0)
            Anmerkungen.append(wert)

        Ausgeliehene_Buecher = []
        self.query.exec("SELECT BuchId FROM Ausgeliehen")
        while self.query.next():
            wert = self.query.value(0)
            Ausgeliehene_Buecher.append(wert)
        
        Buecher = []
        index = 0

        for buch in BuchIDs:
            Buch_Anzeige = Buch()
            Buch_Anzeige.titelEinsetzen(Titel[index])
            Buch_Anzeige.infosEinsetzen(Autoren[index], Genres[index], Anmerkungen[index])
            Buch_Anzeige.bildEinsetzen(Bilder[index])
            Buch_Anzeige.form.addRow("Status:", Buch_Anzeige.Status)
            if buch not in Ausgeliehene_Buecher:
                Buch_Anzeige.Status.setText("verfügbar")
            else:
                Buch_Anzeige.Status.setText("nicht verfügbar")
            Buecher.append(Buch_Anzeige)
            index += 1

        ende = False
        x, y = 0, 0
        index = 0
        while ende == False:
            self.Buecher_Grid.addWidget(Buecher[index], y, x)

            x += 1

            if x == 8:
                x = 0
                y += 1

            index += 1
            if index == len(Buecher):
                ende = True

        self.Buecher_Widget = QWidget()
        self.Buecher_Widget.setLayout(self.Buecher_Grid)
        Buecher_Scroll = QScrollArea()
        Buecher_Scroll.setWidget(self.Buecher_Widget)
        Katalog_VBox.addWidget(Buecher_Scroll)
        self.Katalog_Uebersicht_Container = QWidget()
        self.Katalog_Uebersicht_Container.setLayout(Katalog_VBox)
        self.Katalog_Container = QWidget()


        Neues_Buch_VBox = QVBoxLayout()
        self.Neues_Buch_Anzeige = QLabel("Neues Buch hinzufügen")
        self.Neues_Buch_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Neues_Buch_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        Neues_Buch_VBox.addWidget(self.Neues_Buch_Anzeige, alignment=Qt.AlignmentFlag.AlignTop)

        self.Titel_Edit = QLineEdit()
        self.Titel_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Autor_Edit = QLineEdit()
        self.Autor_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Genre_CB = QComboBox()
        self.Genre_CB.addItems(["", "Abenteuer", "Science Fiction", "Fantasy", "Klassiker", "historisch"])
        self.Genre_CB.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Bild_Edit = QLineEdit()
        self.Bild_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Anmerkungen_Edit = QLineEdit()
        self.Anmerkungen_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Neues_Buch_Form = QFormLayout()
        Titel_Anzeige = QLabel("Titel:")
        Titel_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        Autor_Anzeige = QLabel("Autor:")
        Autor_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        Genre_Anzeige = QLabel("Genre:")
        Genre_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        Bild_Anzeige = QLabel("Bild:")
        Bild_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Bild_Knopf = QPushButton("auswählen")
        self.Bild_Knopf.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Bild_Knopf.setStyleSheet("background: lightblue")
        self.Bild_Knopf.clicked.connect(self.bildWaehlen)
        Anmerkungen_Anzeige = QLabel("Anmerkungen")
        Anmerkungen_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Neues_Buch_Form.addRow(Titel_Anzeige, self.Titel_Edit)
        self.Neues_Buch_Form.addRow(Autor_Anzeige, self.Autor_Edit)
        self.Neues_Buch_Form.addRow(Genre_Anzeige, self.Genre_CB)
        self.Neues_Buch_Form.addRow(Anmerkungen_Anzeige, self.Anmerkungen_Edit)
        self.Neues_Buch_Form.addRow(Bild_Anzeige, self.Bild_Knopf)

        self.Neues_Buch_Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Neues_Buch_Bestaetigen_Knopf.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Neues_Buch_Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Neues_Buch_Bestaetigen_Knopf.clicked.connect(self.buchEinfuegen)

        Neues_Buch_VBox.addWidget(self.Neues_Buch_Anzeige)
        Neues_Buch_VBox.addLayout(self.Neues_Buch_Form)
        Neues_Buch_VBox.addWidget(self.Neues_Buch_Bestaetigen_Knopf, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.Neues_Buch_Container = QWidget()
        self.Neues_Buch_Container.setLayout(Neues_Buch_VBox)

        self.Katalog_Stacked = QStackedLayout()
        self.Katalog_Stacked.addWidget(self.Katalog_Uebersicht_Container)
        self.Katalog_Stacked.addWidget(self.Neues_Buch_Container)

        self.Katalog_Container.setLayout(self.Katalog_Stacked)

        return self.Katalog_Container

    def kundenErstellen(self):
        Kunden_VBox = QVBoxLayout()
        self.Kunden_Anzeige = QLabel("Kunden")
        self.Kunden_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Kunden_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        Kunden_VBox.addWidget(self.Kunden_Anzeige, alignment=Qt.AlignmentFlag.AlignTop)

        Kunden_Modell = QSqlTableModel()
        Kunden_Modell.setTable("Kunden")
        Kunden_Modell.select()
        self.Kunden_Tabelle = QTableView()
        #self.Kunden_Tabelle.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.Kunden_Tabelle.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Kunden_Tabelle.setModel(Kunden_Modell)
        self.Kunden_Tabelle.resizeColumnsToContents()
        self.Kunden_Tabelle.resizeRowsToContents()

        Kunden_VBox.addWidget(self.Kunden_Tabelle)

        self.Kunden_Uebersicht_Container = QWidget()
        self.Kunden_Uebersicht_Container.setLayout(Kunden_VBox)

        Neuer_Kunde_VBox = QVBoxLayout()
        self.Neuer_Kunde_Anzeige = QLabel("neuer Kunde")
        self.Neuer_Kunde_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Neuer_Kunde_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        Neuer_Kunde_VBox.addWidget(self.Neuer_Kunde_Anzeige, alignment=Qt.AlignmentFlag.AlignTop)

        self.Vorname_Edit = QLineEdit()
        self.Vorname_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Nachname_Edit = QLineEdit()
        self.Nachname_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Klasse_Edit = QLineEdit()
        self.Klasse_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Neuer_Kunde_Anmerkungen_Edit = QLineEdit()
        self.Neuer_Kunde_Anmerkungen_Edit.setFont(QFont(self.Schriftart, self.Schriftgroesse))

        self.Neuer_Kunde_Form = QFormLayout()
        Vorname_Anzeige = QLabel("Vorname:")
        Vorname_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        Nachname_Anzeige = QLabel("Nachname:")
        Nachname_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        Klasse_Anzeige = QLabel("Klasse:")
        Klasse_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        Neuer_Kunde_Anmerkungen_Anzeige = QLabel("Anmerkungen:")
        Neuer_Kunde_Anmerkungen_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Neuer_Kunde_Form.addRow(Vorname_Anzeige, self.Vorname_Edit)
        self.Neuer_Kunde_Form.addRow(Nachname_Anzeige, self.Nachname_Edit)
        self.Neuer_Kunde_Form.addRow(Klasse_Anzeige, self.Klasse_Edit)
        self.Neuer_Kunde_Form.addRow(Neuer_Kunde_Anmerkungen_Anzeige, self.Neuer_Kunde_Anmerkungen_Edit)
        Neuer_Kunde_VBox.addLayout(self.Neuer_Kunde_Form)

        self.Bestaetigen_Knopf = QPushButton("bestätigen")
        self.Bestaetigen_Knopf.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Bestaetigen_Knopf.setStyleSheet("background-color: lightblue")
        self.Bestaetigen_Knopf.clicked.connect(self.kundeEinfuegen)
        Neuer_Kunde_VBox.addWidget(self.Bestaetigen_Knopf, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.Neuer_Kunde_Container = QWidget()
        self.Neuer_Kunde_Container.setLayout(Neuer_Kunde_VBox)

        self.Kunden_Stacked = QStackedLayout()
        self.Kunden_Stacked.addWidget(self.Kunden_Uebersicht_Container)
        self.Kunden_Stacked.addWidget(self.Neuer_Kunde_Container)

        self.Kunden_Container = QWidget()
        self.Kunden_Container.setLayout(self.Kunden_Stacked)

        return self.Kunden_Container

    def faelligkeitsBerichtErstellen(self):
        Bericht_VBox = QVBoxLayout()

        self.Bericht_Anzeige = QLabel("Fälligkeiten-Bericht")
        self.Bericht_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Bericht_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.Ausleih_ID_Anzeige = QLabel("Ausleih-ID")
        self.Ausleih_ID_Anzeige = QLabel("Kunde")
        self.Mahnungen_Anzeige = QLabel("Mahnungen")
        self.Buch_Anzeige = QLabel("Buch")
        self.Rueckgabe_Datum_Anzeige = QLabel("Rückgabedatum")
        self.Ermahnen_Anzeige = QLabel("Ermahnen")
        
        self.Bericht_Tabelle = QGridLayout()

        self.Bericht_Tabelle.addWidget(self.Ausleih_ID_Anzeige, 0, 0)
        self.Bericht_Tabelle.addWidget(self.Ausleih_ID_Anzeige, 0, 1)
        self.Bericht_Tabelle.addWidget(self.Mahnungen_Anzeige, 0, 2)
        self.Bericht_Tabelle.addWidget(self.Buch_Anzeige, 0, 3)
        self.Bericht_Tabelle.addWidget(self.Rueckgabe_Datum_Anzeige, 0, 4)
        self.Bericht_Tabelle.addWidget(self.Ermahnen_Anzeige, 0, 5)
        
        Bericht_VBox.addWidget(self.Bericht_Anzeige, alignment=Qt.AlignmentFlag.AlignTop)
        Bericht_VBox.addLayout(self.Bericht_Tabelle)

        self.Faelligkeiten_Container = QWidget()
        self.Faelligkeiten_Container.setLayout(Bericht_VBox)

        return self.Faelligkeiten_Container

    def hilfeErstellen(self):
        Hilfe_VBox = QVBoxLayout()

        self.Hilfe_Anzeige = QLabel("Hilfe")
        self.Hilfe_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Hilfe_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.Hilfe_Text = QLabel()
        self.Hilfe_Text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.Hilfe_Text.setWordWrap(True)
        hilfe_text = "Text einfügen"
        self.Hilfe_Text.setText(hilfe_text)

        Hilfe_VBox.addWidget(self.Hilfe_Anzeige, alignment=Qt.AlignmentFlag.AlignTop)
        Hilfe_VBox.addWidget(self.Hilfe_Text)

        self.Hilfe_Container = QWidget()
        self.Hilfe_Container.setLayout(Hilfe_VBox)

        return self.Hilfe_Container

    def einstellungenErstellen(self):
        Einstell_VBox = QVBoxLayout()
        self.Einstell_Anzeige = QLabel("Einstellungen")
        self.Einstell_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse*4))
        self.Einstell_Anzeige.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        Einstell_VBox.addWidget(self.Einstell_Anzeige)

        self.Schriftgroesse_Anzeige = QLabel("Schriftgröße:")
        self.Schriftgroesse_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Schriftgroesse_cb = QComboBox()
        self.Schriftgroesse_cb.addItem("klein")
        self.Schriftgroesse_cb.addItem("mittel")
        self.Schriftgroesse_cb.addItem("groß")
        self.Schriftgroesse_cb.setCurrentIndex(1)
        self.Schriftgroesse_cb.currentIndexChanged.connect(self.schriftgroesseAendern)
        Schriftgroesse_Form = QFormLayout()
        Schriftgroesse_Form.addRow(self.Schriftgroesse_Anzeige, self.Schriftgroesse_cb)
        Einstell_VBox.addLayout(Schriftgroesse_Form)

        self.Schriftart_Anzeige = QLabel("Schriftart:")
        self.Schriftart_Anzeige.setFont(QFont(self.Schriftart, self.Schriftgroesse))
        self.Schriftart_cb = QComboBox()
        Fonts = ["Arial","Agency FB","Alef","Algerian","Amiri","Bahnschrift","Baskerville Old Face","Bauhaus 93","Bell MT","Nirmala UI"]
        for font in Fonts:
            self.Schriftart_cb.addItem(font)
        self.Schriftart_cb.currentIndexChanged.connect(self.schriftartAendern)
        Schriftart_Form = QFormLayout()
        Schriftart_Form.addRow(self.Schriftart_Anzeige, self.Schriftart_cb)
        Einstell_VBox.addLayout(Schriftart_Form)

        self.Einstell_Container = QWidget()
        self.Einstell_Container.setLayout(Einstell_VBox)

        return self.Einstell_Container

    def createActions(self):
        # Create actions for File menu
        self.Fenster_Act = QAction("Fenster-Modus")
        self.Fenster_Act.setShortcut("Esc")
        self.Fenster_Act.triggered.connect(self.wechselZuFenster)

        self.Vollbild_Act = QAction("Vollbild-Modus")
        self.Vollbild_Act.setShortcut("Ctrl+F")
        self.Vollbild_Act.triggered.connect(self.wechselZuVollbild)

        self.Ausleih_Act = QAction("ausleihen")
        self.Ausleih_Act.triggered.connect(self.neueAusleihe)

        self.Rueckgabe_Act = QAction("zurückgeben")
        self.Rueckgabe_Act.triggered.connect(self.zurueckgeben)
        
        self.Ansehen_Act = QAction("Übersicht")
        self.Ansehen_Act.triggered.connect(self.ansehen)

        self.Neues_Buch_Act = QAction("neues Buch")
        self.Neues_Buch_Act.triggered.connect(self.neuesBuch)
        
        self.Suchen_Act = QAction("suchen")
        self.Suchen_Act.setShortcut("Ctrl+S")
        self.Suchen_Act.triggered.connect(self.suchenStarten)

        self.Kunden_Uebersicht_Act = QAction("Übersicht zeigen")
        self.Kunden_Uebersicht_Act.triggered.connect(self.kundenUebersicht)

        self.Neuer_Kunde_Act = QAction("neuer Kunde")
        self.Neuer_Kunde_Act.triggered.connect(self.neuerKunde)

        self.Ablauf_Pruefen_Act = QAction("Fälligkeiten prüfen")
        self.Ablauf_Pruefen_Act.triggered.connect(self.ablaufPruefen)

        self.Einstell_Act = QAction("Einstellungen öffnen")
        self.Einstell_Act.triggered.connect(self.einstellen)

        self.Hilfe_Act = QAction("Hilfe öffnen")
        self.Hilfe_Act.triggered.connect(self.helfen)

        self.Beenden_Act = QAction("beenden")
        self.Beenden_Act.setShortcut("Ctrl+Q")
        self.Beenden_Act.triggered.connect(self.close)

    def createMenu(self):
        self.menuBar().setNativeMenuBar(False)

        # Create file menu and add actions 
        Ansicht = self.menuBar().addMenu("Ansicht")
        Ansicht.addAction(self.Fenster_Act)
        Ansicht.addAction(self.Vollbild_Act)

        Katalog = self.menuBar().addMenu("Katalog")
        Katalog.addAction(self.Ansehen_Act)
        Katalog.addAction(self.Suchen_Act)
        Katalog.addAction(self.Neues_Buch_Act)

        Kunden = self.menuBar().addMenu("Kunden")
        Kunden.addAction(self.Kunden_Uebersicht_Act)
        Kunden.addAction(self.Neuer_Kunde_Act)

        Einstellungen = self.menuBar().addMenu("Einstellungen")
        Einstellungen.addAction(self.Einstell_Act)

        Hilfe = self.menuBar().addMenu("Hilfe")
        Hilfe.addAction(self.Hilfe_Act)

        Ende = self.menuBar().addMenu("Beenden")
        Ende.addAction(self.Beenden_Act)
    
    def createToolBar(self):
        toolbar = QToolBar("Werkzeuge")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)

        toolbar.addAction(self.Ausleih_Act)
        toolbar.addAction(self.Rueckgabe_Act)
        toolbar.addAction(self.Suchen_Act)
        toolbar.addAction(self.Neuer_Kunde_Act)
        toolbar.addAction(self.Neues_Buch_Act)
        toolbar.addAction(self.Ablauf_Pruefen_Act)
        toolbar.addAction(self.Beenden_Act)

    def wechselZuFenster(self):
        self.showNormal()

    def wechselZuVollbild(self):
        self.showFullScreen()

    def neueAusleihe(self):
        self.stacked.setCurrentWidget(self.Ausleih_Container)

    def ausleihen(self):
        buchid = self.Ausleih_Buch_Edit.text()
        kundenid = self.Ausleih_Kunde_Edit.text()
        ausleih_datum = QDate.currentDate()
        rueckgabe_datum = ausleih_datum.addMonths(1)
        ausleih_datum = ausleih_datum.toString("dd.MM.yyyy")
        rueckgabe_datum = rueckgabe_datum.toString("dd.MM.yyyy")
        eintrag = "INSERT INTO Ausgeliehen (BuchID, KundenID, DatumAusleihe, DatumRückgabe) VALUES("
        eintrag += buchid+", "+kundenid+", "+"'"+ausleih_datum+"'"+", "+"'"+rueckgabe_datum+"')"
        if not self.query.exec(eintrag):
            print(self.query.lastError().text())

    def zurueckgeben(self):
        self.stacked.setCurrentWidget(self.Abgabe_Container)

    def abgabeSuchen(self):
        #"säubert die Tabelle"
        for index in reversed(range(self.Abgabe_Treffer_Tabelle.count())):
            item = self.Abgabe_Treffer_Tabelle.itemAt(index)
            widget = item.widget()

            # Überspringt Layout-Elemente; diese Funktion behandelt Widgets.
            if widget is None:
                continue

            row, column, row_span, column_span = self.Abgabe_Treffer_Tabelle.getItemPosition(index)

            if row != 0:
                self.Abgabe_Treffer_Tabelle.removeWidget(widget)
                widget.deleteLater()


        buchid = self.Abgabe_BuchID_Edit.text()
        kundeid = self.Abgabe_KundenID_Edit.text()
        suche = ""

        if buchid != "":
            suche = "SELECT * FROM Ausgeliehen WHERE BuchID = "+buchid

        elif kundeid != "":
            suche = "SELECT * FROM Ausgeliehen WHERE KundenID = "+kundeid
        
        if suche != "": 
            self.query.exec(suche)

            Ausleih_ID = []
            Buch_ID = []
            Buch_Name = []
            Kunden_ID = []
            Kunden_Name = []
            Datum = []

            while self.query.next():
                Ausleih_ID.append(self.query.value(0))
                Buch_ID.append(self.query.value(1))
                Kunden_ID.append(self.query.value(2))
                Datum.append(self.query.value(4))

            y = 1

            for buch in Ausleih_ID:
                index = Ausleih_ID.index(buch)

                auslese = "SELECT * FROM Kunden WHERE KundenID = " + str(Kunden_ID[index])
                #print(auslese)
                self.query.exec(auslese)
                self.query.next()
                vorname = self.query.value(1)
                nachname = self.query.value(2)
                kunde = vorname + " " + nachname

                auslese = "SELECT * FROM Katalog WHERE BuchID = " + str(Buch_ID[index])
                #print(auslese)
                self.query.exec(auslese)
                self.query.next()
                titel = self.query.value(2)

                Kunden_Name.append(kunde)
                Buch_Name.append(titel)

                self.Abgabe_Treffer_Tabelle.addWidget(QLabel(str(Ausleih_ID[index])), y, 0)
                self.Abgabe_Treffer_Tabelle.addWidget(QLabel(str(Buch_ID[index])), y, 1)
                self.Abgabe_Treffer_Tabelle.addWidget(QLabel(str(Buch_Name[index])), y, 2)
                self.Abgabe_Treffer_Tabelle.addWidget(QLabel(str(Kunden_ID[index])), y, 3)
                self.Abgabe_Treffer_Tabelle.addWidget(QLabel(str(Kunden_Name[index])), y, 4)
                self.Abgabe_Treffer_Tabelle.addWidget(QLabel(str(Datum[index])), y, 5)
                self.Abgabe_Treffer_Tabelle.addWidget(QPushButton("abgeben"), y, 6)

                y += 1
            
            for index in range(self.Abgabe_Treffer_Tabelle.count()):
                item = self.Abgabe_Treffer_Tabelle.itemAt(index)
                widget = item.widget()

                # Überspringt Layout-Elemente; diese Funktion behandelt Widgets.
                if widget is None:
                    continue

                row, column, row_span, column_span = self.Abgabe_Treffer_Tabelle.getItemPosition(index)

                if column == 6 and row != 0:
                    widget.setFont(QFont(MainWindow.Schriftart, MainWindow.Schriftgroesse))
                    widget.setStyleSheet("background-color: lightblue")
                    widget.setFixedWidth(140)
                    widget.clicked.connect(lambda checked=False, knopf=widget:self.abgeben(knopf))
                else:
                    widget.setFont(QFont(self.Schriftart, self.Schriftgroesse))

    def abgeben(self, knopf):
        index = self.Abgabe_Treffer_Tabelle.indexOf(knopf)
        if index != -1:
            row, column, row_span, column_span = self.Abgabe_Treffer_Tabelle.getItemPosition(index)
            a = widget_at(self.Abgabe_Treffer_Tabelle, row, 0)
            ausleih_id = a.text()
            loeschen = "DELETE FROM Ausgeliehen WHERE AusleihID = "+str(ausleih_id)
            #print(loeschen)
            self.query.exec(loeschen)
            self.abgabeSuchen()

    def ansehen(self):
        self.stacked.setCurrentWidget(self.Katalog_Container)
        self.Katalog_Stacked.setCurrentIndex(0)

    def neuesBuch(self):
        self.stacked.setCurrentWidget(self.Katalog_Container)
        self.Katalog_Stacked.setCurrentIndex(1)
        self.Titel_Edit.setFocus()
        self.bild = ""

    def bildWaehlen(self):
        self.bild, selected_filter = QFileDialog.getOpenFileName(self,"Select a file","","Images (*.png *.jpg *.jpeg);;All files (*)")

    def buchEinfuegen(self):
        eintrag = "INSERT INTO Katalog (Bild, Titel, Autor, Genre, Anmerkungen) VALUES("
        
        titel = self.Titel_Edit.text()
        autor = self.Autor_Edit.text()
        genre = self.Genre_CB.currentText()
        anmerkungen = self.Neuer_Kunde_Anmerkungen_Edit.text()
        if anmerkungen == "":
            anmerkungen = "-"
        if self.bild == "":
            self.bild = "kein_Bild"

        eintrag += "'"+self.bild+"'"+", "+"'"+titel+"'"+", "+"'"+autor+"'"+", "+"'"+genre+"'"+", "+"'"+anmerkungen+"'"+")"
        self.query.exec(eintrag)

    def suchenStarten(self):
        self.stacked.setCurrentWidget(self.Katalog_Container)
        self.Katalog_Stacked.setCurrentIndex(0)
        self.Katalog_Suchleiste.setFocus()
    
    def suchen(self):
        BuchIDs = []
        Bild = []
        Titel = []
        Autor = []
        Genre = []
        Anmerkungen = []

        suche = "SELECT * FROM Katalog WHERE Titel LIKE '%"+self.Katalog_Suchleiste.text()+"%' OR Autor LIKE '%"+self.Katalog_Suchleiste.text()+"%' OR Genre LIKE '%"+self.Katalog_Suchleiste.text()+"%'"
        self.query.exec(suche)
        while self.query.next():
            BuchIDs.append(self.query.value(0)) #ID im Katalog
            Bild.append(self.query.value(1))
            Titel.append(self.query.value(2))
            Autor.append(self.query.value(3))
            Genre.append(self.query.value(4))
            Anmerkungen.append(self.query.value(5))

        Ausgeliehene_Buecher = []
        self.query.exec("SELECT BuchId FROM Ausgeliehen")
        while self.query.next():
            wert = self.query.value(0)
            Ausgeliehene_Buecher.append(wert)

        #"säubert die Tabelle"
        for index in reversed(range(self.Buecher_Grid.count())):
            item = self.Buecher_Grid.itemAt(index)
            widget = item.widget()
            # Überspringt Layout-Elemente; diese Funktion behandelt Widgets.
            if widget is None:
                continue
            row, column, row_span, column_span = self.Buecher_Grid.getItemPosition(index)
            self.Buecher_Grid.removeWidget(widget)
            widget.deleteLater()

        Buecher = []
        index = 0

        for buch in BuchIDs:
            Buch_Anzeige = Buch()
            Buch_Anzeige.titelEinsetzen(Titel[index])
            Buch_Anzeige.infosEinsetzen(Autor[index], Genre[index], Anmerkungen[index])
            Buch_Anzeige.bildEinsetzen(Bild[index])
            Buch_Anzeige.form.addRow("Status:", Buch_Anzeige.Status)
            if buch not in Ausgeliehene_Buecher:
                Buch_Anzeige.Status.setText("verfügbar")
            else:
                Buch_Anzeige.Status.setText("nicht verfügbar")
            Buecher.append(Buch_Anzeige)
            index += 1

        ende = False
        x, y = 0, 0
        index = 0
        while ende == False:
            self.Buecher_Grid.addWidget(Buecher[index], y, x)

            x += 1

            if x == 8:
                x = 0
                y += 1

            index += 1
            if index == len(Buecher):
                ende = True

    def kundenUebersicht(self):
        self.stacked.setCurrentWidget(self.Kunden_Container)
        self.Kunden_Stacked.setCurrentIndex(0)

    def neuerKunde(self):
        self.stacked.setCurrentWidget(self.Kunden_Container)
        self.Kunden_Stacked.setCurrentIndex(1)

    def kundeEinfuegen(self):
        eintrag = "INSERT INTO Kunden (Vorname, Nachname, Klasse, Anmerkungen) VALUES("

        vorname = self.Vorname_Edit.text()
        nachname = self.Nachname_Edit.text()
        klasse = self.Klasse_Edit.text()
        anmerkungen = self.Neuer_Kunde_Anmerkungen_Edit.text()

        eintrag += "'"+vorname+"'"+", "+"'"+nachname+"'"+", "+"'"+klasse+"'"+", "+"'"+anmerkungen+"'"+")"
        self.query.exec(eintrag)

    def ablaufPruefen(self):
        self.stacked.setCurrentWidget(self.Faelligkeiten_Container)

        Ausleih_ID = []
        Buch_ID = []
        Kunden_ID = []
        Datum = []
        zaehler = 0

        self.query.exec("SELECT * FROM Ausgeliehen")
        while self.query.next():
            Ausleih_ID.append(self.query.value(0))
            Buch_ID.append(self.query.value(1))
            Kunden_ID.append(self.query.value(2))
            Datum.append(self.query.value(4))

        y = 1
        for rueckgabe_datum in Datum:
            faelligkeit = QDate.fromString(rueckgabe_datum, "dd.MM.yyyy")
            if faelligkeit < QDate.currentDate():
                index = Datum.index(rueckgabe_datum)

                auslese = "SELECT * FROM Kunden WHERE KundenID = " + str(Kunden_ID[index])
                #print(auslese)
                self.query.exec(auslese)
                self.query.next()
                vorname = self.query.value(1)
                nachname = self.query.value(2)
                kunde = vorname + " " + nachname
                mahnungen = self.query.value(4)

                auslese = "SELECT * FROM Katalog WHERE BuchID = " + str(Buch_ID[index])
                #print(auslese)
                self.query.exec(auslese)
                self.query.next()
                buch = self.query.value(2)

                self.Bericht_Tabelle.addWidget(QLabel(str(Ausleih_ID[index])), y, 0)
                self.Bericht_Tabelle.addWidget(QLabel(buch), y, 1)
                self.Bericht_Tabelle.addWidget(QLabel(kunde), y, 2)
                self.Bericht_Tabelle.addWidget(QLabel(str(mahnungen)), y, 3)
                self.Bericht_Tabelle.addWidget(QLabel(rueckgabe_datum), y, 4)
                self.Bericht_Tabelle.addWidget(QPushButton("ermahnen"), y, 5)

                y += 1

        if y == 1: #Prüfung, ob es überhaupt überfällige Bücher gibt.
            QLabel, y, QMessageBox.information(self, "Info", "Es gibt keine überfälligen Bücher.")

    def einstellen(self):
        self.stacked.setCurrentWidget(self.Einstell_Container)

    def helfen(self):
        self.stacked.setCurrentWidget(self.Hilfe_Container)

    def schriftgroesseAendern(self):
        if self.Schriftgroesse_cb.currentText() == "klein":
            self.Schriftgroesse = 12
        elif self.Schriftgroesse_cb.currentText() == "mittel":
            self.Schriftgroesse = 14
        else:
            self.Schriftgroesse = 15

    def schriftartAendern(self):
        self.Schriftart = self.Schriftart_cb.currentText()

    def datenLaden(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("Datenbank.db")
        db.open()

        self.query = QSqlQuery()

class Buch(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.Titel = QLabel()
        self.Titel.setFont(QFont("Arial", 12))
        self.Titel.setWordWrap(True)
        self.Titel.setStyleSheet("font: bold")
        self.Bild_Anzeige = QLabel()
        self.form = QFormLayout()
        self.Status = QLabel()
        self.Status.setFont(QFont("Arial", 11))

        VBox = QVBoxLayout()
        VBox.addWidget(self.Titel)
        VBox.addWidget(self.Bild_Anzeige)
        VBox.addLayout(self.form)
        self.setLayout(VBox)

    def titelEinsetzen(self, titel):
        self.Titel.setText(titel)

    def bildEinsetzen(self, bild):
        if bild != "kein_Bild":
            Bild = QPixmap(bild)
            skaliert = Bild.scaled(200, 150, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.Bild_Anzeige.setPixmap(skaliert)
        else:
            self.Bild_Anzeige.setText("Kein Bild verfügbar")

    def infosEinsetzen(self, autor, genre, anmerkungen):
        Autor = QLabel("Autor:")
        Autor.setFont(QFont("Arial", 11))
        Autor_Anzeige = QLabel(autor)
        Autor_Anzeige.setWordWrap(True)
        Autor_Anzeige.setFont(QFont("Arial", 11))
        Genre = QLabel("Genre:")
        Genre.setFont(QFont("Arial", 11))
        Genre_Anzeige = QLabel(genre)
        Genre_Anzeige.setFont(QFont("Arial", 11))
        Anmerkungen = QLabel("Anmerkungen:")
        Anmerkungen.setFont(QFont("Arial", 11))
        Anmerkungen_Anzeige = QLabel(anmerkungen)
        Anmerkungen_Anzeige.setFont(QFont("Arial", 11))
        Anmerkungen_Anzeige.setWordWrap(True)
        self.form.addRow(Autor, Autor_Anzeige)
        self.form.addRow(Genre, Genre_Anzeige)
        self.form.addRow(Anmerkungen, Anmerkungen_Anzeige)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())