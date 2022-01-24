from PyQt5 import QtCore as qtc

class PXIOperation(qtc.QObject):
    def status(self):
        print("Hallo Welt.")