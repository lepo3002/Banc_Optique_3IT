import sys

from PyQt5 import QtWidgets, uic
import os

errorHandling = [
    'Please enter a value for all parameters',
    'Please enter a value between 400 and 1400 nm for the wavelength',
    'Wavelength step can''t be superior to the wavelength interval',
    'Please enter a numeric value for all parameters except the experience name',
    'The slits maximum width is 5 mm',
    'The wavelength to crop needs to be between the high and low wavelengths',
    'The wavelength to crop is not in the data to measure',
    'You need at least 1 zone'
]


class MainWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__()
        uic.loadUi("settings.ui", self)
        self.show()
        self.setWindowTitle("Settings")
        self.data = []
        self.bt.clicked.connect(self.button_pressed)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setText('Error')
        self.msg.setInformativeText('Please enter a value for all parameters')
        self.msg.setWindowTitle("Error")
        self.working_dir = os.getcwd()
        self.bt_working_dir.clicked.connect(self.set_working_dir)
        self.crop.stateChanged.connect(self.browsing)
        self.multiple.stateChanged.connect(self.multiplezones)
        self.bt_working_dir.setEnabled(False)
        self.wavelengths = []
        self.zones = 1
        self.cancel.clicked.connect(self.quit)

    def set_working_dir(self):
        value = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Open Directory", self.working_dir, QtWidgets.QFileDialog.ShowDirsOnly
        )
        if value:
            self.working_dir = value

    def button_pressed(self):
        self.data.clear()
        self.data.append(self.exp.text())
        self.data.append(self.w_start.text())
        self.data.append(self.w_step.text())
        self.data.append(self.w_stop.text())
        self.data.append(self.exposure.text())
        self.data.append(self.gain.text())
        self.data.append(self.entrance.text())
        self.data.append(self.exit.text())
        self.data.append(self.firstw.text())
        if self.multiple.isChecked():
            self.data.append(self.nbZones.text())
        else:
            self.data.append('1')

        if not all(v for v in self.data):
            self.msg.setInformativeText(errorHandling[0])
            self.msg.exec_()
            self.data.clear()
        elif not (self.data[1].isdigit() or
                  self.data[2].isdigit() or
                  self.data[3].isdigit() or
                  self.data[4].isdigit() or
                  self.data[5].isdigit() or
                  self.data[6].isdigit() or
                  self.data[7].isdigit() or
                  self.data[8].isdigit() or
                  self.data[9].isdigit()):
            self.msg.setInformativeText(errorHandling[3])
            self.msg.exec_()
            self.data.clear()
        elif int(self.data[1]) < 400 or int(self.data[3]) > 1400:
            self.msg.setInformativeText(errorHandling[1])
            self.msg.exec_()
            self.data.clear()
        elif int(self.data[2]) >= (int(self.data[3])-int(self.data[1])):
            self.msg.setInformativeText(errorHandling[2])
            self.msg.exec_()
            self.data.clear()
        elif int(self.data[6]) > 5 or int(self.data[7]) > 5:
            self.msg.setInformativeText(errorHandling[4])
            self.msg.exec_()
            self.data.clear()
        elif (int(self.data[8]) < int(self.data[1]) or
              int(self.data[8]) > int(self.data[3])):
            self.msg.setInformativeText(errorHandling[5])
            self.msg.exec_()
            self.data.clear()
        elif int(self.data[9]) == 0:
            self.msg.setInformativeText(errorHandling[7])
            self.msg.exec_()
            self.data.clear()
        else:
            for i in range((int(self.data[3]) - int(self.data[1])) // int(self.data[2])):
                self.wavelengths.append(int(self.data[1]) + (i * int(self.data[2])))

            if self.multiple.isChecked():
                self.zones = self.data[9]

            if int(self.data[8]) in self.wavelengths:
                self.close()
            else:
                self.msg.setInformativeText(errorHandling[6])
                self.msg.exec_()
                self.data.clear()

    def browsing(self):
        if self.crop.isChecked():
            self.bt_working_dir.setEnabled(True)
        else:
            self.bt_working_dir.setEnabled(False)
            self.working_dir = os.getcwd()

    def multiplezones(self):
        if self.multiple.isChecked():
            self.nbZones.setEnabled(True)
        else:
            self.nbZones.setEnabled(False)

    def quit(self):
        sys.exit()
