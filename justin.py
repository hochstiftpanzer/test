import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
QPushButton, QGridLayout)
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):   
        grid = QGridLayout()  
        self.setLayout(grid)
        
        nameLabel = QLabel(self)
        nameLabel.setText('Name:')
        line = QLineEdit(self)

        line.move(80, 20)
        line.resize(200, 32)
        nameLabel.move(20, 20)
        
        grid.addWidget(nameLabel, 6,4)
        grid.addWidget(line, 7,4)
        names = ['Cls', 'Bck', '', 'Close', 
        '7', '8', '9', '/',
        '4', '5', '6', '*',
        '1', '2', '3', '-',
        '0', '.', '=', '+',]

        positions = [(i, j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)

        self.move(300, 150)
        self.setWindowTitle('PyQt window')  
        self.show()

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = Example()
     sys.exit(app.exec_())    