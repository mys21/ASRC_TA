from PyQt5 import QtGui, QtCore,QtWidgets
from small_gui import Ui_MainWindow
import sys
#import os
#import subprocess
from test import camera1

class Editor(QtWidgets.QMainWindow):

    def __init__(self):#,lif,pl=np.zeros((50,1)),preloaded=False):
        super(Editor, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        #self.lif = lif


        #######################################################################
        # Section 1: Creates Connections between GUI objects in ta_gui_class.py
        # and the methods found in this class (Editor)
        self.ui.initializeButton.clicked.connect(self.exec_push_btn)
        self.ui.lineEdit.textChanged.connect(self.update_line_edit)

        #######################################################################
        # Section 2: Initializing values in the gui
        self.ui.History.setText(" ")

    ###########################################################################
    # Section 3: Methods which define signals connected in Section 1

    def update_line_edit(self):
        '''execute on text typed - just types some text'''

        self.append_history("typed: " + self.ui.lineEdit.text())
        return

    def append_history(self,message):
        self.ui.History.append(message)

    ###########################################################################
    # Section 6: Run functions
    def exec_push_btn(self):
        '''execute on pushed button - initializes camera'''
        self.append_history("button pushed")

        self.camera= camera1()
        self.something = self.camera.something
        self.append_history(self.something)
        self.camera.Initialize(number_of_scans=100, line_period=9)
        self.something2 = self.camera.something2
        self.append_history(self.something2)
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    #last_instance_filename = r'C:\Users\Public\Documents\Python Scripts\PyTA\last_instance_values.txt'
    #try:
        #last_instance_values = np.genfromtxt(last_instance_filename)
        #ex = Editor(last_instance_filename,pl=last_instance_values,preloaded=True)
    #except:
    ex = Editor()#last_instance_filename)


    ex.show()
    #ex.create_plots()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
