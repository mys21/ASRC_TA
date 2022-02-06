from PyQt5 import QtGui, QtCore,QtWidgets
from small_gui_class import Ui_MainWindow
import sys
from small_camera import camera1
from TA2_camera import *
from ta_data_processing_class import *
import time
#import pyqtgraph as pg
#from pyqtgraph import ImageView, PlotWidget #in class ui

class Editor(QtWidgets.QMainWindow):

    def __init__(self):
        super(Editor, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        self.lines_per_frame = 1000
        self.self.times = [1]
        #connects buttons to functions
        self.ui.runButton.clicked.connect(self.exec_run_btn)
        self.ui.stopButton.clicked.connect(self.exec_stop_btn)
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
    def exec_run_btn(self):
        '''execute on pushed button - initializes camera'''
        self.ui.runButton.setDisabled(True)
        self.camera= octoplus()
        #self.camera.start_acquire.connect(self.camera.Acquire)
        self.camera.data_ready.connect(self.post_acquire)
        self.camera.Initialize( lines_per_frame=self.lines_per_frame)

        self.append_history("camera initialized")
        self.append_history("Number of Cameras: "+ str(self.camera.ulNbCameras.value))

        self.timestep = 0
        self.append_history('Acquiring '+str(self.num_shots)+' shots')
        #self.camera.start_acquire.emit()
        self.camera.Acquire()
        self.append_history("data acquired"+ " timer: "+ str(end-start))
        self.append_history("Buffer Size: "+ str(self.camera.ImageInfos.iBufferSize))
        return

    def post_acquire(self):
        self.current_data = ta_data_processing(self.camera.probe, self.camera.first_pixel, self.camera.num_pixels)
        self.current_data.separate_on_off()
        self.current_data.average_shots()
        self.append_history("data processed")
        self.create_plots()
        self.append_history("plots created")

        if self.stop_request is True:
            self.finish()
        elif elf.timestep == len(self.times)-1:
            #self.post_sweep()
            self.finish()
        else:
            #this does DELAY stuff that is not connected
            self.timestep = self.timestep+1
            #self.time = self.times[self.timestep]
            #self.move(self.time)
            self.camera.Acquire()
        return

    def finish():
        self.camera.Exit()
        self.append_history("camera closed")
        self.ui.runButton.setDisabled(False)
        return

    def exec_stop_btn(self):
        self.stop_request=True
        return

    #--start of plotting functions---

    def pump_off_plot(self):
        '''pump off plot'''
        #if doesn't work, remove the .plotItem
        try:
            self.ui.pumpsOffPlot.plotItem.plot(self.plot_waves,self.ta.probe_off,pen='g',clear=True)
        except:
            self.append_history('Error Plotting pump off Plot')

        self.ui.pumpsOffPlot.plotItem.setLabels(left='dtt',bottom='Wavelength / Pixel')
        self.ui.pumpsOffPlot.plotItem.showAxis('top',show=True)
        self.ui.pumpsOffPlot.plotItem.showAxis('right',show=True)
        return

    def pump_on_plot(self):
        '''pump off plot'''
        try:
            self.ui.pumpsOnPlot.plotItem.plot(self.plot_waves,self.ta.probe_on,pen='g',clear=True)
        except:
            self.append_history('Error Plotting pump on Plot')

        self.ui.pumpsOnPlot.plotItem.setLabels(left='dtt',bottom='Wavelength / Pixel')
        self.ui.pumpsOnPlot.plotItem.showAxis('top',show=True)
        self.ui.pumpsOnPlot.plotItem.showAxis('right',show=True)
        return

    def create_plots(self):
		#in self.ui.plotPumpOn, plot self.ta.probe_on because thats not confusing at all...
		#in self.ui.plotPumpOff, plot self.ta.probe_off because thats not confusing at all...
        self.num_pixels= self.camera.num_pixels
        self.plot_waves = np.linspace(0,self.num_pixels-1,self.num_pixels)
        self.pump_off_plot()
        self.pump_on_plot()
        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Editor()
    ex.show()
    #ex.create_plots()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
