import sys
import time
from enum import Enum
from qtpy import QtWidgets
from ui.mainwindow import Ui_MainWindow
from functools import partial
from ui.cTechmanModbusClient import TechmanModbusClient


app = QtWidgets.QApplication(sys.argv)


class Kanalbelegung(Enum):
    kanal_programm = 9000
    kanal_hutschiene = 9002
    kanal_reihenfolge = 9101


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eingabe_Reihenklemmen")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.roboter = TechmanModbusClient('192.168.99.21')
        self.roboter.write_dint(Kanalbelegung.kanal_programm.value, [0])
        self.AnzahlKlemmen = 6
        self.AnzahlHutschienen = 8
        self.IndexHutschiene = 1
        self.maxKlemmenHutschiene = 20
        self.ui.label_command.setText("Bitte Parameter eingeben und bestätigen!")
        self.liste_alle_hutschienen = [[]]
        self.liste_anzahl_klemmen = []
        self.ui.getAnzahlKlemmen.setText('6')
        self.ui.getAnzahlHutschinen.setText('8')
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
        print(Kanalbelegung.kanal_hutschiene)

    def get_anzahl_klemmen(self):
        return self.eingabe_nur_integer(self.ui.getAnzahlKlemmen.text())

    def get_anzahl_hutschienen(self):
        return self.eingabe_nur_integer(self.ui.getAnzahlHutschinen.text())

    def get_klemmenlimit_hutschiene(self):
        return self.eingabe_nur_integer(self.ui.getMaxKlemmenHutschiene.text())

    def get_index_hutschiene(self):
        return self.eingabe_nur_integer(self.ui.tabWidget.currentIndex() + 1)

    def eingabe_nur_integer(self, x):
        try:
            return int(x)
        except:
            print("Fehler")
            self.ui.label_command.setText("Bitte nur Zahlen eingeben")

    def init_parameter(self):
        self.AnzahlKlemmen = self.get_anzahl_klemmen()
        self.AnzahlHutschienen = self.get_anzahl_hutschienen()
        self.maxKlemmenHutschiene = self.get_klemmenlimit_hutschiene()
        self.liste_anzahl_klemmen = self.init_liste(self.AnzahlKlemmen)
        self.liste_alle_hutschienen = self.init_2dim_array(self.AnzahlHutschienen)
        self.IndexHutschiene = self.get_index_hutschiene()
        print(self.liste_alle_hutschienen)
        print(self.liste_anzahl_klemmen)
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

    def init_liste(self, anzahl_klemmen):
        liste_anzahl_klemmen = []
        for i in range(anzahl_klemmen + 1):
            liste_anzahl_klemmen.append(0)
        return liste_anzahl_klemmen

    def init_2dim_array(self, anzahl_hutschienen):
        liste_alle_hutschienen = []
        for _ in range(anzahl_hutschienen):
            liste_alle_hutschienen.append([])
        return liste_alle_hutschienen

    def darstellung(self, klemme_value):
        index_hutschiene = self.get_index_hutschiene()
        self.liste_befuellen(index_hutschiene, klemme_value)
        self.zaehler()
        print(f'Gesamtarray für alle Hutschienen: {self.liste_alle_hutschienen}')
        print(f'Anzahl aller Klemmen: {self.liste_anzahl_klemmen}')
        self.ui.label_command.setText("Bitte wählen sie die Reihenfolge der Reihenklemmen für die aktive Hutschiene!")

    def liste_befuellen(self, nummer_hutschiene, klemme_value):
        if self.anzahl_gesamt_klemmen(nummer_hutschiene) < self.maxKlemmenHutschiene:
            self.liste_alle_hutschienen[nummer_hutschiene].append(klemme_value)
        else:
            self.ui.label_command.setText(
                "Das zuvor festgelegte Limit wurde bereits erreicht.")

    def zaehler(self):
        anzahl_klemmen = self.AnzahlKlemmen
        number_hutschiene = self.ui.tabWidget.currentIndex()+1
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

    def anzahl_gesamt_klemmen(self, number_hutschiene):
        return len(self.liste_alle_hutschienen[number_hutschiene])

    def tab_wechsel(self):
        self.zaehler()
        self.ui.label_command.setText("Bitte wählen sie die Reihenfolge der Reihenklemmen für die aktive Hutschiene!")

    def loeschen_eins(self):
        self.IndexHutschiene = self.get_index_hutschiene()
        self.liste_alle_hutschienen[self.IndexHutschiene] = []
        self.zaehler()
        self.ui.label_command.setText("Die angewählte Hutschiene wurde geleert.")

    def loeschen_alle_hutschienen(self):
        self.liste_alle_hutschienen = self.init_2dim_array(self.AnzahlHutschienen)
        self.zaehler()
        self.ui.label_command.setText("Alle Hutschienen wurden geleert.")

    def kommunikation_roboter(self, kanal, value, time):
        self.roboter.write_dint(kanal, [value])
        time.sleep(time)
        handshake_value = self.roboter.read_dint(kanal+500, 2)
        if handshake_value != value:
            self.ui.label_command.setText("Fehler bei der Übertragung!")
        else:
            self.ui.label_command.setText("Übertragung okay")

    def waitOfRobo(self, kanal, status):
        while self.roboter.read_dint(kanal, 2) != status:
            time.sleep(1)

    def roboter_starten(self):
        for i in range(1, self.AnzahlHutschienen):
            print("Start")
            self.kommunikation_roboter(Kanalbelegung.kanal_programm.value, 100, 0.2)
            print("Programmwahl: Einlesen")
            self.kommunikation_roboter(Kanalbelegung.kanal_hutschiene.value, i, 0.2)
            self.kommunikation_roboter(9004, 1, 0.2)
            print("Schiene wurde ausgewählt")
            self.kommunikation_roboter(Kanalbelegung.kanal_reihenfolge.value, self.liste_alle_hutschienen[i], 0.2)
            self.kommunikation_roboter(9006, 1, 5)
            if self.roboter.read_dint(9506, 2) == 1:
                self.kommunikation_roboter(Kanalbelegung.kanal_hutschiene.value, 0, 0.2)
                self.kommunikation_roboter(9004, 0, 0.2)
                self.kommunikation_roboter(Kanalbelegung.kanal_reihenfolge.value, 0, 0.2)
                self.kommunikation_roboter(9006, 0, 0.2)
                print("Kanäle wurden resettet")
            else:
                self.ui.label_command.setText("Fehler bei der Speicherung!")
                break
            print("Daten wurden übertragen")

        self.kommunikation_roboter(Kanalbelegung.kanal_programm.value, 200, 0.2)
        print("Programmwahl: Platzieren")
        self.kommunikation_roboter(Kanalbelegung.kanal_programm.value, 200, 0.2)
        self.waitOfRobo(9508, [1])
        self.ui.label_command.setText("Vorsicht, Roboter beginnt Platzierung")
        self.waitOfRobo(9500, [999])
        self.ui.label_command.setText("Platzierung erfolgreich")
        self.kommunikation_roboter(Kanalbelegung.kanal_programm.value, 0, 0.2)
        self.kommunikation_roboter(9008, 0, 0.2)



if __name__ == "__main__":
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
