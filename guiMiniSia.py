from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
from tabla import Ui_MainWindow
# from MiniSiaPOO import data

# data = [(222222, 'Javier', 'Garcia', 1, 4, 5.0), (101010, 'Antonio', 'Castañeda', 2, 8, 4.5), (888888, 'Laura', 'Pinzon', 1, 3, 4.0)]

class myWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, data, parent=None):
        super(myWindow, self).__init__(parent)
        self.setupUi(self)
        self.data = data

        #Tabla de Clasificación
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(10)
        self.tableWidget.setHorizontalHeaderLabels(('Id', 'Nombre', 'Apellido', '# Materias', 'Créditos acumulados', 'Promedio'))

        row = 0
        for i in self.data:
            col = 0
            for item in i:
                cellinfo = QtWidgets.QTableWidgetItem(str(item))
                self.tableWidget.setItem(row, col, cellinfo)
                col += 1
            row += 1



def main(data):
    app = QApplication(sys.argv)
    form = myWindow(data)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main(data)
