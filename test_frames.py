import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QHBoxLayout, QFrame, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tab_widget = QTabWidget(self)
        self.setCentralWidget(self.tab_widget)

        self.tab_widget.currentChanged.connect(self.tab_changed)

        self.frames_per_tab = 0
        self.max_frames = 50

    def tab_changed(self, index):
        self.frames_per_tab = 0

    def create_frame(self, button_index):
        if self.frames_per_tab >= self.max_frames:
            return

        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        if button_index in [1, 2, 3]:
            frame.setStyleSheet("background-color: gray;")
        else:
            frame.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFFF00, stop:1 #00FF00);")

        if button_index in [1, 4]:
            frame.setFixedHeight(100)
            frame.setFixedWidth(15)
        elif button_index in [3, 6]:
            frame.setFixedHeight(70)
            frame.setFixedWidth(15)
        else:
            frame.setFixedHeight(40)
            frame.setFixedWidth(15)

        layout = QHBoxLayout()
        layout.addWidget(frame)
        self.tab_widget.currentWidget().layout().addLayout(layout)

        self.frames_per_tab += 1

    def create_buttons(self):
        for i in range(1, 7):
            button = QPushButton(f"Button {i}")
            button.clicked.connect(lambda _, idx=i: self.create_frame(idx))
            self.tab_widget.currentWidget().layout().addWidget(button)


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()

    tab1 = QWidget()
    tab1.setLayout(QHBoxLayout())
    window.tab_widget.addTab(tab1, "Tab 1")
    window.create_buttons()

    tab2 = QWidget()
    tab2.setLayout(QHBoxLayout())
    window.tab_widget.addTab(tab2, "Tab 2")

    window.show()
    sys.exit(app.exec_())