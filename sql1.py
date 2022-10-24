import sqlite3
from sqlite3 import Error


def conexionALaBD():
    try:
        con = sqlite3.connect("MiBaseDatos.db")
        return con
    except Error:
        print(Error)

def crearTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "CREATE TABLE materias (codigo integer PRIMARY KEY, nombre text, facultadDicta text, departamentoDicta text, creditos integer, idioma text)"
    )
    con.commit()

def leerInfoMaterias():
    codigo = input("Codigo de la materia: ")
    codigo = codigo.ljust(12)   # ajusta a la izquierda 12 posiciones
    nombre = input("Nombre de la materia: ")
    facultadDicta = input("Facultad que la dicta: ")
    departamentoDicta = input("Departamento que la dicta: ")
    creditos = input("Cantidad de créditos: ")
    idioma = input("Idioma en que se dicta: ")
    materia = (codigo, nombre, facultadDicta, departamentoDicta, creditos, idioma)
    print('La información de la materia es: ', materia)
    return materia 

def insertarTablaMaterias(con, materia):
    cursorObj = con.cursor() #recorremos la base de datos con el objeto de conexión
    cursorObj.execute('''INSERT INTO materias VALUES (?,?,?,?,?,?)''', materia)
    # insertamos información en la tabla materias
    con.commit() #guarda la tabla en el drive

def insertarTablaMateria2(con):
    cursorObj = con.cursor() #recorremos la base de datos con el objeto de conexión
    # cursorObj.execute('''INSERT INTO materias VALUES (?,?,?,?,?,?)''', materia)
    cod = input("Ingrese el código: ")
    cad = 'INSERT INTO materias VALUES ("+cod+", "poo", "ing", "sist", "3", "español")'
    print('El SQL a ejecutar es ', cad)
    cursorObj.execute(cad)
    # insertamos información en la tabla materias
    con.commit() #guarda la tabla en el drive

def actualizarTablaMaterias(con, codMat):
    cursorObjt = con.cursor() #cursor recorrer base de datos
    nuevoidioma = input("Actualice el idioma: ")
    actualizar = 'UPDATE materias SET idioma ="'+nuevoidioma+'"WHERE codigo ="'+codMat+'"'
    cursorObjt.execute(actualizar)
    con.commit()#guardamos tabla en el drive

def borrarinfoTablaMaterias(con):
    cursorObjt = con.cursor()
    materiaBorrar = input("Codigo de la materia para borrar: ")
    borrar = 'DELETE FROM materias WHERE codigo ="'+materiaBorrar+'"'
    cursorObjt.execute(borrar)
    con.commit()

def promedioTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT count (*) FROM materias")  #se puede usar "*" para consultar todos los campos
    cantidadMaterias = cursorObj.fetchall()
    for row in cantidadMaterias:
        cantidad = row[0]
    cursorObj.execute("SELECT sum(creditos) FROM materias")  #se puede usar "*" para consultar todos los campos
    sumatoriaCreditos = cursorObj.fetchall()
    for row in sumatoriaCreditos:
        sumatoria = row[0]
    promedio = sumatoria/cantidad
    print('El promedio de los creditos de las materias es: ', promedio)
    
def consultarTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT codigo, nombre FROM materias")  #se puede usar "*" para consultar todos los campos
    filas = cursorObj.fetchall()
    print('El tipo de dato de filas es: ', type(filas))
    for row in filas:
        codigo = row[0]
        nombre = row[1]
        print('La información de la materia es: ', codigo, nombre)
        print('La información de la lista es: ')
        print(row)

def cerrarBD(con):
    con.close()

def menu(Con):
    salirPrincipal = False
    while not salirPrincipal:
        opc = input('''
                    Menú de Opciones
                    1. Materias
                    2. Estudiante
                    3. Historia Académica
                    4. Clasificación
                    5. Salir

                    Slececcione opción>>> ''')
        if (opc=='1'):
            salirMaterias = False
            while not salirMaterias:
                opcionMaterias = input('''
                                       Menú de Materias
                                       1. Leer información de la materia
                                       2. Insertar Materias
                                       3. Consultar Materias
                                       4. Actualizar Materias
                                       5. Borrar materia
                                       6. Calcular promedio de los créditos
                                       7. Salir

                                       Seleccione opción: 
                                       ''')
                if (opcionMaterias == '1'):
                    miMateria = leerInfoMaterias()
                elif (opcionMaterias == '2'):
                    insertarTablaMateria2(Con)
                elif (opcionMaterias == '3'):
                    consultarTablaMaterias(Con)
                elif (opcionMaterias == '4'):
                    actualizarTablaMaterias(Con, '123')
                elif (opcionMaterias == '5'):
                    borrarinfoTablaMaterias(Con)
                elif (opcionMaterias == '6'):
                    promedioTablaMaterias(Con)
                elif (opcionMaterias == '7'):
                    salirMaterias = True




def main():
    miCon = conexionALaBD()
    # # crearTablaMaterias(miCon)
    # miMateria = leerInfoMaterias()
    # insertarTablaMaterias(miCon, miMateria)
    # consultarTablaMaterias(miCon)
    # codMatact= input('Codigo de la materia a actualizar: ')
    # actualizarTablaMaterias(miCon, codMatact)
    # borrarinfoTablaMaterias(miCon)
    # promedioTablaMaterias(miCon)
    menu(miCon)
    cerrarBD(miCon)


main()
