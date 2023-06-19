import sys
import time
from enum import Enum
from qtpy import QtWidgets
from ui.mainwindow import Ui_MainWindow
from functools import partial
from ui.cTechmanModbusClient import TechmanModbusClient


app = QtWidgets.QApplication(sys.argv)


# Hier können die Kanäle des Roboters, die beschrieben werden sollen, angepasst werden.
class Kanalbelegung(Enum):
    kanal_programm = 9000
    kanal_hutschiene = 9002
    kanal_hutschiene_handshake = 9004
    kanal_reihenfolge = 9101
    kanal_reihenfolge_handshake = 9006
    kanal_betrieb_handshake = 9008


# Hauptanwendung zur Roboterkommunikation via Modbus
class MainWindow(QtWidgets.QMainWindow):

    # Initialisierung der Variablen und Erstellung des Fensters, Zuweisung der Pushbuttons zu Funktionen
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eingabe_Reihenklemmen")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.roboter = TechmanModbusClient('192.168.99.21')
        self.roboter.write_dint(9000, [0])
        self.AnzahlKlemmen = 6
        self.AnzahlHutschienen = 8
        self.IndexHutschiene = 1
        self.maxKlemmenHutschiene = 20
        self.ui.label_command.setText("Bitte Parameter eingeben und bestätigen!")
        self.liste_alle_hutschienen = [[]]
        self.liste_anzahl_klemmen = []
        self.ui.getAnzahlKlemmen.setText('6')
        self.ui.getAnzahlHutschienen.setText('8')
        self.ui.getMaxKlemmenHutschiene.setText('20')
        self.ui.Absenden.clicked.connect(self.init_parameter)
        self.ui.Klemme1.clicked.connect(partial(self.darstellung, 1))
        self.ui.Klemme2.clicked.connect(partial(self.darstellung, 2))
        self.ui.Klemme3.clicked.connect(partial(self.darstellung, 3))
        self.ui.Klemme4.clicked.connect(partial(self.darstellung, 4))
        self.ui.Klemme5.clicked.connect(partial(self.darstellung, 5))
        self.ui.Klemme6.clicked.connect(partial(self.darstellung, 6))
        self.ui.Loeschen.clicked.connect(self.loeschen_eins)
        self.ui.AllesLoeschen.clicked.connect(self.loeschen_alle_hutschienen)
        self.ui.SendenAnRobo.clicked.connect(self.roboter_starten)
        self.ui.tabWidget.currentChanged.connect(self.tab_wechsel)

    # Anzahl von Klemmentypen aus GUI-Eingabefeld einlesen
    def get_anzahl_klemmen(self):
        return self.eingabe_nur_integer(self.ui.getAnzahlKlemmen.text())

    # Anzahl von Hutschienen aus GUI-Eingabefeld einlesen
    def get_anzahl_hutschienen(self):
        return self.eingabe_nur_integer(self.ui.getAnzahlHutschienen.text())

    # Klemmenlimit aus GUI-Eingabefeld einlesen
    def get_klemmenlimit_hutschiene(self):
        return self.eingabe_nur_integer(self.ui.getMaxKlemmenHutschiene.text())

    # aktuell angewählten Hutschienen-Tab einlesen
    def get_index_hutschiene(self):
        return self.eingabe_nur_integer(self.ui.tabWidget.currentIndex())

    # Funktion um Eingabeparameter auf Datentyp Integer zu prüfen
    def eingabe_nur_integer(self, x):
        try:
            return int(x)
        except:
            print("Fehler")
            self.ui.label_command.setText("Bitte nur Zahlen eingeben")

    # Hauptprogramm, Initialisierung der Parameter
    def init_parameter(self):
        self.AnzahlKlemmen = self.get_anzahl_klemmen()
        self.AnzahlHutschienen = self.get_anzahl_hutschienen()
        self.maxKlemmenHutschiene = self.get_klemmenlimit_hutschiene()
        self.liste_anzahl_klemmen = self.init_liste(self.AnzahlKlemmen)
        self.liste_alle_hutschienen = self.init_2dim_array(self.AnzahlHutschienen)
        self.IndexHutschiene = self.get_index_hutschiene()
        print(self.liste_alle_hutschienen)
        print(self.liste_anzahl_klemmen)
        # Graut Eingabefelder aus, bis Parameter bestätigt werden
        self.ui.AllesLoeschen.setEnabled(True)
        self.ui.Klemme1.setEnabled(True)
        self.ui.Klemme2.setEnabled(True)
        self.ui.Klemme3.setEnabled(True)
        self.ui.Klemme4.setEnabled(True)
        self.ui.Klemme5.setEnabled(True)
        self.ui.Klemme6.setEnabled(True)
        self.ui.Loeschen.setEnabled(True)
        self.ui.SendenAnRobo.setEnabled(True)
        self.ui.label_command.setText("Bitte wählen sie die Reihenfolge der Reihenklemmen für die aktive Hutschiene!")

    # Liste zur Summierung der Gesamt- und typspezifischen Anzahl der gesetzten Reihenklemmen erstellen
    def init_liste(self, anzahl_klemmen):
        liste_anzahl_klemmen = []
        for i in range(anzahl_klemmen + 1):
            liste_anzahl_klemmen.append(0)
        return liste_anzahl_klemmen

    # leere 2-dimensionale Liste zur Darstellung der Reihenfolge der Reihenklemmen erstellen, eine Zeile pro Hutschiene
    def init_2dim_array(self, anzahl_hutschienen):
        liste_alle_hutschienen = []
        for _ in range(anzahl_hutschienen):
            liste_alle_hutschienen.append([])
        return liste_alle_hutschienen

    # befüllt die zugehörige Zeile der Liste jeweils am Ende mit gewählter Reihenklemme und zeigt Liste und Anzahlen
    def darstellung(self, klemme_value):
        index_hutschiene = self.get_index_hutschiene()
        self.liste_befuellen(index_hutschiene, klemme_value)
        self.zaehler()
        print(f'Gesamtarray für alle Hutschienen: {self.liste_alle_hutschienen}')
        print(f'Anzahl aller Klemmen: {self.liste_anzahl_klemmen}')
        self.ui.label_command.setText("Bitte wählen sie die Reihenfolge der Reihenklemmen für die aktive Hutschiene!")

    # befüllt die Liste, insofern Klemmenlimit nicht erreicht ist, ansonsten Fehlermeldung
    def liste_befuellen(self, nummer_hutschiene, klemme_value):
        if self.anzahl_gesamt_klemmen(nummer_hutschiene) < self.maxKlemmenHutschiene:
            self.liste_alle_hutschienen[nummer_hutschiene].append(klemme_value)
        else:
            self.ui.label_command.setText(
                "Das zuvor festgelegte Limit wurde bereits erreicht.")

    # Funktion zur Erfassung der gesetzten Klemmen
    def zaehler(self):
        anzahl_klemmen = self.AnzahlKlemmen
        number_hutschiene = self.ui.tabWidget.currentIndex()
        print("Hutschiene", number_hutschiene)
        self.liste_anzahl_klemmen = self.init_liste(anzahl_klemmen)
        #  print(self.liste_anzahl_klemmen)
        for i in range(1, anzahl_klemmen + 1):
            for number in self.liste_alle_hutschienen[number_hutschiene]:
                if i == number:
                    self.liste_anzahl_klemmen[number - 1] += 1
        self.liste_anzahl_klemmen[-1] = self.anzahl_gesamt_klemmen(number_hutschiene)
        self.ui.setAnzahlGesamt.setText(str(self.liste_anzahl_klemmen[-1]))
        self.ui.setAnzahlKlemme1.setText(str(self.liste_anzahl_klemmen[0]))
        self.ui.setAnzahlKlemme2.setText(str(self.liste_anzahl_klemmen[1]))
        self.ui.setAnzahlKlemme3.setText(str(self.liste_anzahl_klemmen[2]))
        self.ui.setAnzahlKlemme4.setText(str(self.liste_anzahl_klemmen[3]))
        self.ui.setAnzahlKlemme5.setText(str(self.liste_anzahl_klemmen[4]))
        self.ui.setAnzahlKlemme6.setText(str(self.liste_anzahl_klemmen[5]))

    # Ermittelt die Anzahl an Feldern in der angewählten Zeile der Liste und gibt sie zurück -- Summe Reihenklemmen
    def anzahl_gesamt_klemmen(self, number_hutschiene):
        return len(self.liste_alle_hutschienen[number_hutschiene])

    # Aktualisiert die gezählten Werte bei Tabwechsel
    def tab_wechsel(self):
        self.zaehler()
        self.ui.label_command.setText("Bitte wählen sie die Reihenfolge der Reihenklemmen für die aktive Hutschiene!")

    # Leert die Zeile der angewählten Hutschiene in der Liste
    def loeschen_eins(self):
        self.IndexHutschiene = self.get_index_hutschiene()
        self.liste_alle_hutschienen[self.IndexHutschiene] = []
        self.zaehler()
        self.ui.label_command.setText("Die angewählte Hutschiene wurde geleert.")

    # Leert die gesamte Liste
    def loeschen_alle_hutschienen(self):
        self.liste_alle_hutschienen = self.init_2dim_array(self.AnzahlHutschienen)
        self.zaehler()
        self.ui.label_command.setText("Alle Hutschienen wurden geleert.")

    # schreibt einen "value" auf einen "kanal" im Roboter, wartet eine "Zeit", prüft auf erfolgreichen Handshake
    def kommunikation_roboter(self, kanal, value, zeit):
        self.roboter.write_dint(kanal, value)
        print("Wurde geschrieben auf Kanal:", kanal, "Status", self.roboter.read_dint(kanal, 50))
        time.sleep(float(zeit))
        handshake_value = self.roboter.read_dint(kanal+500, 1)
        print("aus Roboter Kanal", kanal+500, "Status", handshake_value)
        if handshake_value != value:
            self.ui.label_command.setText("Fehler bei der Übertragung!")
        else:
            self.ui.label_command.setText("Übertragung okay")

    # wartet auf das fremde Setzen eines Kanals auf einen festgelegten Status, Abfragezyklus 1x pro Sekunde
    def warten_auf_roboter(self, kanal, status):
        print(self.roboter.read_dint(kanal, 1))
        while self.roboter.read_dint(kanal, 1) != [status]:
            time.sleep(1)

    # startet die Datenübertragung mit dem Roboter, anschließend Platzierung der Reihenklemmen
    def roboter_starten(self):
        roboter_hutschienen = self.AnzahlHutschienen + 1
        print(roboter_hutschienen)
        self.kommunikation_roboter(9002, [0], 0.2)
        self.kommunikation_roboter(9502, [0], 0.2)
        self.kommunikation_roboter(9004, [0], 0.2)
        self.kommunikation_roboter(9504, [0], 0.2)
        self.kommunikation_roboter(9101, [0] * 50, 0.2)
        self.kommunikation_roboter(9601, [0] * 50, 0.2)
        self.kommunikation_roboter(9006, [0], 0.2)
        self.kommunikation_roboter(9506, [0], 0.2)
        for i in range(1, roboter_hutschienen):
            print(i)
            reihenfolge = self.liste_alle_hutschienen[i-1]
            self.ui.label_command.setText("Datenübertragung initiiert!")
            print("Datenübertragung initiiert!")
            self.kommunikation_roboter(9000, [100], 0.2)
            self.ui.label_command.setText("Programmwahl: Einlesen")
            print("Programmwahl: Einlesen")
            self.kommunikation_roboter(9002, [i], 0.2)
            self.kommunikation_roboter(9004, [1], 0.2)
            self.ui.label_command.setText("Schiene wurde ausgewählt")
            print("Schiene wurde ausgewählt")
            print(reihenfolge)
            time.sleep(1)
            self.kommunikation_roboter(9101, reihenfolge, 1)
            print("test")
            self.kommunikation_roboter(9006, [1], 1)
            self.ui.label_command.setText("Reihenfolge wurde übertragen")
            if self.roboter.read_dint(9506, 1) == [1]:
                self.kommunikation_roboter(9002, [0], 1)
                self.kommunikation_roboter(9004, [0], 1)
                self.kommunikation_roboter(9101, [0] * 50, 1)
                self.kommunikation_roboter(9006, [0], 1)
                print("warten auf Null Return")
                self.warten_auf_roboter(9502, 0)
                self.warten_auf_roboter(9504, 0)
                self.warten_auf_roboter(9601, 0)
                self.warten_auf_roboter(9506, 0)
                print("Die Kanäle wurden resettet")
            else:
                self.ui.label_command.setText("Fehler bei der Speicherung!")
                print("error")
                time.sleep(10)
                break
            print("Daten wurden erfolgreich übertragen")

        self.kommunikation_roboter(9000, [200], 0.2)
        self.ui.label_command.setText("Programmwahl: Platzieren")
        print("Programmwahl: Platzieren")
        self.warten_auf_roboter(9508, 1)
        self.ui.label_command.setText("Vorsicht, Roboter beginnt Platzierung")
        self.warten_auf_roboter(9500, 999)
        self.ui.label_command.setText("Platzierung erfolgreich")
        self.kommunikation_roboter(9000, [0], 0.2)
        self.kommunikation_roboter(9008, [0], 0.2)


# öffnet das Fenster zur Benutzereingabe
if __name__ == "__main__":
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
