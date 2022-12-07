#REQUISITOS
#Instalar la librería PyQt5 para poder ejecutar la interfaz gráfica

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys

#tabla es el nombre del archivo que obtuvimos al convertir el archivo tipo '.ui' que exportamos desde Qt Designer
from tabla import Ui_MainWindow


#Objeto llamado myWindow que es instancia de QMainWindow y Ui_MainWindow (este es el objeto que se genera con pyuic5 al convertir 
#el archivo ".ui" que obtenemos desde QtDesigner). En su método init tiene como argumento a 'data' que puede ser una lista o tupla
#que contenga la información completa de la tabla clasificacion, luego 'data' pasa a ser un atributo del objeto.
class myWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, data):
        super(myWindow, self).__init__()
        self.setupUi(self)
        self.data = data

        #Tabla de Clasificación
        self.tableWidget.setSortingEnabled(True) #Permite organizar según la columna que se escoja
        self.tableWidget.setColumnCount(6)  #Establece 6 columnas en la tabla
        self.tableWidget.setRowCount(10) #Establece 10 filas en la tabla
        self.tableWidget.setHorizontalHeaderLabels(('Id', 'Nombre', 'Apellido', '# Materias', 'Créditos cursados', 'Promedio')) #Añade enncabezados a las columnas

        #Toma los elemento de una lista o tupla y los agrega a la tabla, los convierte a un objeto tipo "QTableWidgetItem"
        #y luego los agrega a la tabla. De izquierda a derecha y de arriba para abajo
        row = 0
        for i in self.data:
            col = 0
            for item in i:
                cellinfo = QtWidgets.QTableWidgetItem(str(item))
                cellinfo.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled) #Evita que el usuario modifique las celdas de la tabla
                self.tableWidget.setItem(row, col, cellinfo)
                col += 1
            row += 1


#Función main que al ser llamada ejecuta la ventana de la interfaz.
#Tiene como argumento a data que es el mismo 'data' que es argumento de la clase myWindow
def main(data):
    app = QApplication(sys.argv)
    form = myWindow(data)
    form.show()
    app.exec_()

#Previene que este archivo ejecute la ventana al ser inmediatamente ejecutado
if __name__ == '__main__':
    main(data)
