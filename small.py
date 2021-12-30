from PyQt5 import QtGui, QtCore,QtWidgets
from small_gui_class import Ui_MainWindow
import sys
from small_camera import camera1
from TA2_camera import *
from ta_data_processing_class import *

class Editor(QtWidgets.QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.lines_per_frame = 1000

        #connects buttons to functions
        self.ui.initializeButton.clicked.connect(self.exec_initialize_btn)
        self.ui.linesPerFrame.textChanged.connect(self.update_lines_per_frame)

        #sets variables
        self.ui.History.setText(" ")

    #defines functions
    def append_history(self,message):
        self.ui.History.append(message)

    def update_lines_per_frame(self):
        '''execute on text typed - updates line period'''

        try:
            self.lines_per_frame= int(self.ui.linesPerFrame.text())
            self.append_history("changed line period to: " + str(self.lines_per_frame))
        except:
            self.append_history("that is not an integer, try again")
        return

    #things that happen during runtime
    def exec_initialize_btn(self):
        '''execute on pushed button - initializes camera'''
        self.append_history("button pushed")
        self.camera= octoplus()
        self.camera.Initialize( lines_per_frame=self.lines_per_frame)
        #self.cameraLog = "\n".join(self.camera.log)
        self.append_history("camera initialized")
        self.append_history("Number of Cameras: "+ str(self.camera.ulNbCameras.value))
        self.camera.Acquire()
        self.append_history("data acquired")
        self.append_history("Buffer Size: "+ str(oc.ImageInfos.iBufferSize))
        self.processing()
        self.append_history("data processed")
        self.create_plots()
        self.append_history("plots created")
        self.camera.Exit()
        return

    def processing(self):
        self.ta = ta_data_processing(self.camera.probe, self.camera.reference, self.camera.first_pixel, self.camera.num_pixels)
        self.ta.separate_on_off()
        self.ta.average_shots() #NOTE: average shots can only be called after separate_on_off
        #self.append_history("Pump on: ", self.ta.probe_on) #not sure if this is good to append cause entire array
        #self.append_history("Pump off: ", self.ta.probe_off)
        return

    #--start of plotting functions---
    def create_plots(self):
        #in self.ui.plotPumpOn, plot self.ta.probe_on because thats not confusing at all...
    	#in self.ui.plotPumpOff, plot self.ta.probe_off because thats not confusing at all...
        self.num_pixels= self.camera.num_pixels
        self.plot_waves = np.linspace(0,self.num_pixels-1,self.num_pixels)
        pump_off_plot()
        pump_on_plot()
        return

    def pump_off_plot(self):
        '''pump off plot'''
        try:
            self.ui.plotPumpOff.plotItem.plot(self.plot_waves,self.ta.probe_off,pen='g',clear=True)
        except:
            self.append_history('Error Plotting pump off Plot')

        self.ui.plotPumpOff.plotItem.setLabels(left='dtt',bottom='Wavelength / Pixel')
        self.ui.plotPumpOff.plotItem.showAxis('top',show=True)
        self.ui.plotPumpOff.plotItem.showAxis('right',show=True)
        return

    def pump_on_plot(self):
        '''pump off plot'''
        try:
            self.ui.plotPumpOn.plotItem.plot(self.plot_waves,self.ta.probe_on,pen='g',clear=True)
        except:
            self.append_history('Error Plotting pump on Plot')

        self.ui.plotPumpOn.plotItem.setLabels(left='dtt',bottom='Wavelength / Pixel')
        self.ui.plotPumpOn.plotItem.showAxis('top',show=True)
        self.ui.plotPumpOn.plotItem.showAxis('right',show=True)
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Editor()
    ex.show()
    #ex.create_plots()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
