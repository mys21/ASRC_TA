from PyQt5 import QtGui, QtCore,QtWidgets
from small_gui_class import Ui_MainWindow
import sys
from small_camera import camera1

class Editor(QtWidgets.QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.line_period = 9

        #connects buttons to functions
        self.ui.initializeButton.clicked.connect(self.exec_initialize_btn)
        self.ui.linePeriod.textChanged.connect(self.update_line_period)

        #sets variables
        self.ui.History.setText(" ")

    #defines functions
    def append_history(self,message):
        self.ui.History.append(message)

    def update_line_period(self):
        '''execute on text typed - updates line period'''

        try:
            self.line_period= int(self.ui.linePeriod.text())
            self.append_history("changed line period to: " + str(self.line_period))
        except:
            self.append_history("that is not an integer, try again")

        return

    #things that happen during runtime
    def exec_initialize_btn(self):
        '''execute on pushed button - initializes camera'''
        self.append_history("button pushed")
        self.camera= camera1()
        self.camera.Initialize(number_of_scans=100, line_period=self.line_period)
        self.cameraLog = self.camera.log
        self.append_history(self.cameraLog)
        return


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Editor()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
