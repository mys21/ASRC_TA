'''scripts to help create ta_gui_class.py from the QtCreator .ui file'''

#import os

#os.system(r'pyuic5 "C:\Users\Public\Documents\Python Scripts\PyTA\TA_GUI\ta_gui.ui" -o ta_gui_class.py')

import PyQt5.uic

with open('ta_gui_class.py','w') as file:
    PyQt5.uic.compileUi(r"C:\Users\Public\Documents\Git_Clone\TA2\TA_GUI\ta_gui.ui",file)
