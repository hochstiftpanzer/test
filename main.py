import sys
from qtpy import QtWidgets

from ui.mainwindow_alt import Ui_MainWindow
from ui.cTechmanModbusClient import TechmanModbusClient

app = QtWidgets.QApplication(sys.argv)

class MainWindow(QtWidgets.QMainWindow):
    hw1 = []
    hw2 = []
    hw3 = []
    hw4 = []
    hs1 = []
    hs2 = []
    hs3 = []
    hs4 = []
    listAllHW =\
    [
        [],
        [],
        []
    ]
    roboter = TechmanModbusClient('192.168.99.21')
    "hutschiene = 1"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Berufliche Schulen Obersberg x AEM - Abschlussprojekt 2023 Robotik ")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.PB_HW1_STT.clicked.
        self.ui.PB_HW1_ST.clicked.connect(self.hw1st)
        self.ui.PB_HW1_STST.clicked.connect(self.hw1stst)
        self.ui.PB_HW1_STT_PE.clicked.connect(self.hw1sttpe)
        self.ui.PB_HW1_ST_PE.clicked.connect(self.hw1stpe)
        self.ui.PB_HW1_STST_PE.clicked.connect(self.hw1ststpe)
        self.ui.PB_HW1_DEL.clicked.connect(self.hw1delete)
        "self.ui.PB_ALG_ROB.clicked.connect(self.senden)"
        "self.ui.PB_ALG_SHOW.clicked.connect(self.sendenhw1, self.hw1st)"
        self.ui.PB_HW1_NEXT.clicked.connect(self.sendenhw1)
        self.ui.PB_HW2_NEXT.clicked.connect(self.sendenhw2)
        self.ui.PB_HW3_NEXT.clicked.connect(self.sendenhw3)
        self.ui.PB_HW4_NEXT.clicked.connect(self.sendenhw4)
        self.ui.PB_HS1_NEXT.clicked.connect(self.sendenhs1)
        self.ui.PB_HS2_NEXT.clicked.connect(self.sendenhs2)
        self.ui.PB_HS3_NEXT.clicked.connect(self.sendenhs3)
        self.ui.PB_ALG_ROB.clicked.connect(self.sendenhs4)

    def sendenhw1(self, hw1):
        MainWindow.roboter.write_dint(9101, hw1)
        print(MainWindow.roboter.read_dint(9101, 2))
        print(self)

    def sendenhw2(self, hw1):
        MainWindow.roboter.write_dint(9101, hw1)
        print(MainWindow.roboter.read_dint(9101, 2))
        print(self)

    def sendenhw3(self, hw1):
        MainWindow.roboter.write_dint(9101, hw1)
        print(MainWindow.roboter.read_dint(9101, 2))
        print(self)

    def sendenhw4(self, hw1):
        MainWindow.roboter.write_dint(9101, hw1)
        print(MainWindow.roboter.read_dint(9101, 2))
        print(self)

    def sendenhs1(self, hw1):
        MainWindow.roboter.write_dint(9101, hw1)
        print(MainWindow.roboter.read_dint(9101, 2))
        print(self)

    def sendenhs2(self, hw1):
        MainWindow.roboter.write_dint(9101, hw1)
        print(MainWindow.roboter.read_dint(9101, 2))
        print(self)

    def sendenhs3(self, hw1):
        MainWindow.roboter.write_dint(9101, hw1)
        print(MainWindow.roboter.read_dint(9101, 2))
        print(self)

    def sendenhs4(self, hw1):
        MainWindow.roboter.write_dint(9101, hw1)
        print(MainWindow.roboter.read_dint(9101, 2))
        print(self)

    def hw1st(self):
        MainWindow.hw1.append("3")
        MainWindow.hutschiene = MainWindow.hutschiene + 1
        print(MainWindow.hw1)
        self.ui.label_HW1_sum_total.setText(str(MainWindow.hutschiene))

    def hw1stst(self):
        MainWindow.hw1.append("5")
        MainWindow.hutschiene = len(MainWindow.hw1)
        print(MainWindow.hw1)
        self.ui.label_HW1_sum_total.setText(str(MainWindow.hutschiene))

    def hw1sttpe(self):
        MainWindow.hw1.append("2")
        MainWindow.hutschiene = MainWindow.hutschiene + 1
        print(MainWindow.hw1)
        self.ui.label_HW1_sum_total.setText(str(MainWindow.hutschiene))

    def hw1stpe(self):
        MainWindow.hw1.append("4")
        MainWindow.hutschiene = MainWindow.hutschiene + 1
        print(MainWindow.hw1)
        self.ui.label_HW1_sum_total.setText(str(MainWindow.hutschiene))

    def hw1ststpe(self):
        MainWindow.hw1.append("6")
        MainWindow.hutschiene = MainWindow.hutschiene + 1
        print(MainWindow.hw1)
        self.ui.label_HW1_sum_total.setText(str(MainWindow.hutschiene))

    def hw1delete(self):
        MainWindow.hw1.clear()
        MainWindow.hutschiene = 0
        print(MainWindow.hw1)
        self.ui.label_HW1_sum_total.setText("0")

    def zaehler(self, numberHW):
        for i in range(1,6):
            print((i))
            for number in MainWindow.listAllHW[numberHW]:
                print(number)
                pass



    def setHW(self, number):
        return MainWindow.listAllHW[number -1]

window = MainWindow()

window.show()

sys.exit(app.exec())
