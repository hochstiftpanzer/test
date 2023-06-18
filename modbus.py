# Pakete importieren
import sys
from qtpy import QtWidgets

# QT Datei importieren
from ui.mainwindow_alt import Ui_MainWindow
from ui.cTechmanModbusClient import TechmanModbusClient


app = QtWidgets.QApplication(sys.argv)

# Hauptprogramm

hw1 = []
hw2 = []
hw3 = []
hw4 = []
hs1 = []
hs2 = []
hs3 = []
hs4 = []
hn = 1


class MainWindow2(QtWidgets.QMainWindow):
    [
    hw1 = [1, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
    hw2 = [2, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
    hw3 = [3, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
    hw4 = [4, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
    hs1 = [1, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
    hs2 = [2, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
    hs3 = [3, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
    hs4 = [4, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
    ]
    roboter = TechmanModbusClient('192.168.99.21')
    print(hw1)
    roboter.write_dint(9101, hw1)
    roboter.write_dint(9102, hw2)
    roboter.write_dint(9103, hw3)
    roboter.write_dint(9104, hw4)
    roboter.write_dint(9105, hs1)
    roboter.write_dint(9106, hs2)
    roboter.write_dint(9107, hs3)
    roboter.write_dint(9108, hs4)
    print("Hutschiene Waagerecht 1", roboter.read_dint(9101, 20))
    print("Hutschiene Waagerecht 2", roboter.read_dint(9102, 20))
    print("Hutschiene Waagerecht 3", roboter.read_dint(9103, 20))
    print("Hutschiene Waagerecht 4", roboter.read_dint(9104, 20))
    print("Hutschiene Senkrecht 1", roboter.read_dint(9105, 20))
    print("Hutschiene Senkrecht 2", roboter.read_dint(9106, 20))
    print("Hutschiene Senkrecht 3", roboter.read_dint(9107, 20))
    print("Hutschiene Senkrecht 4", roboter.read_dint(9108, 20))

    def __init__(self, parent=None):
        #super().__init__(parent)

        self.setWindowTitle("Abschlussprojekt")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.PB_HW1_STT.clicked.connect(self.hw1stt)
        self.ui.PB_HW1_ST.clicked.connect(self.hw1st)
        self.ui.PB_HW1_STST.clicked.connect(self.hw1stst)
        self.ui.PB_HW1_STT_PE.clicked.connect(self.hw1sttpe)
        self.ui.PB_HW1_ST_PE.clicked.connect(self.hw1stpe)
        self.ui.PB_HW1_STST_PE.clicked.connect(self.hw1ststpe)
        self.ui.PB_ALG_ROB.clicked.connect(self.senden)
        # roboter = TechmanModbusClient('192.168.99.21')
        # MainWindow2.hw1 = [3, 5, 4, 2, 6, 3, 4, 5, 1, 4, 2, 3, 5, 6, 5, 4, 1, 2, 3, 6]
        # roboter.write_dint(9101,hw1)
        # print(roboter.read_dint(9101, 20))

    # Unterprogramm übertragen

    def senden(self):
        print("Senden an Roboter")
        print(MainWindow2.hw1)
        MainWindow2.roboter = TechmanModbusClient('192.168.99.21')
        MainWindow2.roboter.write_dint(9101, MainWindow2.hw1)
        print(MainWindow2.roboter.read_dint(9101, 20))
        # print(MainWindow2.hw1)

    # Taster für STT Klemme

    def hw1stt(self):
        if MainWindow2.hn == 1:
            MainWindow2.hw1.append("1")
            print(MainWindow2.hw1)
        elif MainWindow2.hn == 2:
            MainWindow2.hw2.append("1")
            print(MainWindow2.hw2)
        elif MainWindow2.hn == 3:
            MainWindow2.hw3.append("1")
            print(MainWindow2.hw3)
        elif MainWindow2.hn == 4:
            MainWindow2.hw4.append("1")
            print(MainWindow2.hw4)
        elif MainWindow2.hn == 5:
            MainWindow2.hs1.append("1")
            print(MainWindow2.hs1)
        elif MainWindow2.hn == 6:
            MainWindow2.hs2.append("1")
            print(MainWindow2.hs2)
        elif MainWindow2.hn == 7:
            MainWindow2.hs3.append("1")
            print(MainWindow2.hs3)
        elif MainWindow2.hn == 8:
            MainWindow2.hs4.append("1")
            print(MainWindow2.hs4)
        else:
            print("Bitte gültige Hutschiene wählen!")

    # Taster für ST Klemme

    def hw1st(self):
        if MainWindow2.hn == 1:
            MainWindow2.hw1.append("3")
            print("HW1" and MainWindow2.hw1)
        elif MainWindow2.hn == 2:
            MainWindow2.hw2.append("3")
            print("HW2" and MainWindow2.hw2)
        elif MainWindow2.hn == 3:
            MainWindow2.hw3.append("3")
            print("HW3" and MainWindow2.hw3)
        elif MainWindow2.hn == 4:
            MainWindow2.hw4.append("3")
            print("HW4" and MainWindow2.hw4)
        elif MainWindow2.hn == 5:
            MainWindow2.hs1.append("3")
            print("HS1" and MainWindow2.hs1)
        elif MainWindow2.hn == 6:
            MainWindow2.hs2.append("3")
            print("HS2" and MainWindow2.hs2)
        elif MainWindow2.hn == 7:
            MainWindow2.hs3.append("3")
            print("HS3" and MainWindow2.hs3)
        elif MainWindow2.hn == 8:
            MainWindow2.hs4.append("3")
            print("HS4" and MainWindow2.hs4)
        else:
            print("Bitte gültige Hutschiene wählen!")


    # Taster für STST Klemme

    def hw1stst(self):
        if MainWindow2.hn == 1:
            MainWindow2.hw1.append("5")
            print("HW1" and MainWindow2.hw1)
        elif MainWindow2.hn == 2:
            MainWindow2.hw2.append("5")
            print("HW2" and MainWindow2.hw2)
        elif MainWindow2.hn == 3:
            MainWindow2.hw3.append("5")
            print("HW3" and MainWindow2.hw3)
        elif MainWindow2.hn == 4:
            MainWindow2.hw4.append("5")
            print("HW4" and MainWindow2.hw4)
        elif MainWindow2.hn == 5:
            MainWindow2.hs1.append("5")
            print("HS1" and MainWindow2.hs1)
        elif MainWindow2.hn == 6:
            MainWindow2.hs2.append("5")
            print("HS2" and MainWindow2.hs2)
        elif MainWindow2.hn == 7:
            MainWindow2.hs3.append("5")
            print("HS3" and MainWindow2.hs3)
        elif MainWindow2.hn == 8:
            MainWindow2.hs4.append("5")
            print("HS4" and MainWindow2.hs4)
        else:
            print("Bitte gültige Hutschiene wählen!")

    # Taster für STT-PE Klemme

    def hw1sttpe(self):
        if MainWindow2.hn == 1:
            MainWindow2.hw1.append("2")
            print("HW1" and MainWindow2.hw1)
        elif MainWindow2.hn == 2:
            MainWindow2.hw2.append("2")
            print("HW2" and MainWindow2.hw2)
        elif MainWindow2.hn == 3:
            MainWindow2.hw3.append("2")
            print("HW3" and MainWindow2.hw3)
        elif MainWindow2.hn == 4:
            MainWindow2.hw4.append("2")
            print("HW4" and MainWindow2.hw4)
        elif MainWindow2.hn == 5:
            MainWindow2.hs1.append("2")
            print("HS1" and MainWindow2.hs1)
        elif MainWindow2.hn == 6:
            MainWindow2.hs2.append("2")
            print("HS2" and MainWindow2.hs2)
        elif MainWindow2.hn == 7:
            MainWindow2.hs3.append("2")
            print("HS3" and MainWindow2.hs3)
        elif MainWindow2.hn == 8:
            MainWindow2.hs4.append("2")
            print("HS4" and MainWindow2.hs4)
        else:
            print("Bitte gültige Hutschiene wählen!")

    # Taster für ST-PE Klemme

    def hw1stpe(self):
        if MainWindow2.hn == 1:
            MainWindow2.hw1.append("4")
            print("HW1" and MainWindow2.hw1)
        elif MainWindow2.hn == 2:
            MainWindow2.hw2.append("4")
            print("HW2" and MainWindow2.hw2)
        elif MainWindow2.hn == 3:
            MainWindow2.hw3.append("4")
            print("HW3" and MainWindow2.hw3)
        elif MainWindow2.hn == 4:
            MainWindow2.hw4.append("4")
            print("HW4" and MainWindow2.hw4)
        elif MainWindow2.hn == 5:
            MainWindow2.hs1.append("4")
            print("HS1" and MainWindow2.hs1)
        elif MainWindow2.hn == 6:
            MainWindow2.hs2.append("4")
            print("HS2" and MainWindow2.hs2)
        elif MainWindow2.hn == 7:
            MainWindow2.hs3.append("4")
            print("HS3" and MainWindow2.hs3)
        elif MainWindow2.hn == 8:
            MainWindow2.hs4.append("4")
            print("HS4" and MainWindow2.hs4)
        else:
            print("Bitte gültige Hutschiene wählen!")

    # Taster für STST-PE Klemme

    def hw1ststpe(self):

        if MainWindow2.hn == 1:
            MainWindow2.
            .append("6")
            print("HW1" and MainWindow2.hw1)
        elif MainWindow2.hn == 2:
            MainWindow2.hw2.append("6")
            print("HW2" and MainWindow2.hw2)
        elif MainWindow2.hn == 3:
            MainWindow2.hw3.append("6")
            print("HW3" and MainWindow2.hw3)
        elif MainWindow2.hn == 4:
            MainWindow2.hw4.append("6")
            print("HW4" and MainWindow2.hw4)
        elif MainWindow2.hn == 5:
            MainWindow2.hs1.append("6")
            print("HS1" and MainWindow2.hs1)
        elif MainWindow2.hn == 6:
            MainWindow2.hs2.append("6")
            print("HS2" and MainWindow2.hs2)
        elif MainWindow2.hn == 7:
            MainWindow2.hs3.append("6")
            print("HS3" and MainWindow2.hs3)
        elif MainWindow2.hn == 8:
            MainWindow2.hs4.append("6")
            print("HS4" and MainWindow2.hs4)
        else:
            print("Bitte gültige Hutschiene wählen!")


# Fenster öffnen


window = MainWindow2()

window.show()

sys.exit(app.exec_())
