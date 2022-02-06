'''scripts to help create small_gui_class.py from the QtCreator .ui file'''

#import os

#os.system(r'pyuic5 "C:\Users\Public\Documents\Python Scripts\PyTA\TA_GUI\ta_gui.ui" -o ta_gui_class.py')

import PyQt5.uic
from pathlib import Path

with open('small_gui_class.py','w+') as file:
    #PyQt5.uic.compileUi(r"\Users\annezats\Documents\research\spectrometer build\ASRC_TA\small_gui.ui",file)
    PyQt5.uic.compileUi(Path('small_gui.ui'),file)
