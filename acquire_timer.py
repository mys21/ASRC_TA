from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot
import time

class timer(QObject):
    def __init__(self):
        super(QObject,self).__init__()
        
    timer_updated = pyqtSignal(int)
    start_timer = pyqtSignal(int)
    @pyqtSlot()
    def run(self,num_shots):
        i = 0
        while i < num_shots:
            i = i+10
            time.sleep(.01)
            self.timer_updated.emit(i)
            print(i)