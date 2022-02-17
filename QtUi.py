from PyQt5 import QtWidgets, uic

errorHandling = [
    'Please enter a value for all parameters',
    'Please enter a value between 400 and 1400 nm for the wavelength',
    'Wavelength step can''t be superior to the wavelength interval',
    'Please enter a numeric value for all parameters except the experience name',
    'The slits maximum width is 5 mm',

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

        if not all(v for v in self.data):
            self.msg.setInformativeText(errorHandling[0])
            self.msg.exec_()
        elif not (self.data[1].isdigit() or
                  self.data[2].isdigit() or
                  self.data[3].isdigit() or
                  self.data[4].isdigit() or
                  self.data[5].isdigit() or
                  self.data[6].isdigit() or
                  self.data[7].isdigit()):
            self.msg.setInformativeText(errorHandling[3])
            self.msg.exec_()
        elif int(self.data[1]) < 400 or int(self.data[3]) > 1400:
            self.msg.setInformativeText(errorHandling[1])
            self.msg.exec_()

        elif int(self.data[2]) >= (int(self.data[3])-int(self.data[1])):
            self.msg.setInformativeText(errorHandling[2])
            self.msg.exec_()
        elif int(self.data[6]) > 5 or int(self.data[7]) > 5:
            self.msg.setInformativeText(errorHandling[4])
            self.msg.exec_()
        else:
            self.close()
