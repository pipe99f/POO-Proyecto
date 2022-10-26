import sqlite3
from sqlite3 import Error


def conexionALaBD():
    try:
        con = sqlite3.connect("MiBaseDatos.db")
        return con
    except Error:
        print(Error)


##MATERIAS


def crearTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "CREATE TABLE materias (codigo integer PRIMARY KEY, nombre text, facultadDicta text, departamentoDicta text, creditos integer, idioma text)"
    )
    con.commit()


def leerInfoMaterias():
    codigo = input("Codigo de la materia: ")
    codigo = codigo.ljust(12)  # ajusta a la izquierda 12 posiciones
    nombre = input("Nombre de la materia: ")
    facultadDicta = input("Facultad que la dicta: ")
    departamentoDicta = input("Departamento que la dicta: ")
    creditos = input("Cantidad de créditos: ")
    idioma = input("Idioma en que se dicta: ")
    materia = (codigo, nombre, facultadDicta, departamentoDicta, creditos, idioma)
    print("La información de la materia es: ", materia)
    return materia


def insertarTablaMaterias(con, materia):
    cursorObj = con.cursor()  # recorremos la base de datos con el objeto de conexión
    cursorObj.execute("""INSERT INTO materias VALUES (?,?,?,?,?,?)""", materia)
    # insertamos información en la tabla materias
    con.commit()  # guarda la tabla en el drive


def insertarTablaMateria2(con):
    cursorObj = con.cursor()  # recorremos la base de datos con el objeto de conexión
    # cursorObj.execute('''INSERT INTO materias VALUES (?,?,?,?,?,?)''', materia)
    cod = input("Ingrese el código: ")
    cad = 'INSERT INTO materias VALUES ("+cod+", "poo", "ing", "sist", "3", "español")'
    print("El SQL a ejecutar es ", cad)
    cursorObj.execute(cad)
    # insertamos información en la tabla materias
    con.commit()  # guarda la tabla en el drive


def actualizarTablaMaterias(con, codMat):
    cursorObjt = con.cursor()  # cursor recorrer base de datos
    nuevoidioma = input("Actualice el idioma: ")
    actualizar = (
        'UPDATE materias SET idioma ="'
        + nuevoidioma
        + '"WHERE codigo ="'
        + codMat
        + '"'
    )
    cursorObjt.execute(actualizar)
    con.commit()  # guardamos tabla en el drive


def borrarinfoTablaMaterias(con):
    cursorObjt = con.cursor()
    materiaBorrar = input("Codigo de la materia para borrar: ")
    borrar = 'DELETE FROM materias WHERE codigo ="' + materiaBorrar + '"'
    cursorObjt.execute(borrar)
    con.commit()


def promedioTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT count (*) FROM materias"
    )  # se puede usar "*" para consultar todos los campos
    cantidadMaterias = cursorObj.fetchall()
    for row in cantidadMaterias:
        cantidad = row[0]
    cursorObj.execute(
        "SELECT sum(creditos) FROM materias"
    )  # se puede usar "*" para consultar todos los campos
    sumatoriaCreditos = cursorObj.fetchall()
    for row in sumatoriaCreditos:
        sumatoria = row[0]
    promedio = sumatoria / cantidad
    print("El promedio de los creditos de las materias es: ", promedio)


def consultarTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT codigo, nombre FROM materias"
    )  # se puede usar "*" para consultar todos los campos
    filas = cursorObj.fetchall()
    print("El tipo de dato de filas es: ", type(filas))
    for row in filas:
        codigo = row[0]
        nombre = row[1]
        print("La información de la materia es: ", codigo, nombre)
        print("La información de la lista es: ")
        print(row)


def consultarInfoMateria(con, codigo):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM materias WHERE codigo = ?", codigo)
    infoMateria = cursorObj.fetchall()
    for row in infoMateria:
        print("Código: ", row[0])
        print("Nombre: ", row[2])
        print("Facultad: ", row[2])
        print("Departamento: ", row[3])
        print("Créditos: ", row[4])
        print("Idioma: ", row[5])


##ESTUDIANTE


def crearTablaEstudiante(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        f"""CREATE TABLE estudiantes (identificacion integer PRIMARY KEY, 
                                     nombre text, 
                                     apellido text, 
                                     carrera text, 
                                     fechaNacimiento text, 
                                     fechaIngreso text,
                                     ciudadProcedencia text, 
                                     email text, 
                                     cantidadMatriculas integer,
                                     fotografia blob)"""
    )
    con.commit()


def importarFoto(ubicacionArchivo):
    with open(ubicacionArchivo, "rb") as file:
        blobFoto = file.read()
    return blobFoto


def leerInfoEstudiante():
    id = input("Numero de identificación: ")
    nombre = input("Nombre del estudiante: ")
    apellido = input("Apellido del estudiante: ")
    carrera = input("Plan de estudios: ")
    fechaNacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
    fechaIngreso = input("Fecha de ingreso (dd/mm/aaaa): ")
    ciudadProcedencia = input("Ciudad de procedencia: ")
    email = input("Email: ")
    cantidadMatriculas = input("Cantidad de matrículas: ")
    foto = input("Ubicación completa de la fotografía (PATH): ")
    blobFoto = importarFoto(foto)
    infoEstudiante = (
        id,
        nombre,
        apellido,
        carrera,
        fechaNacimiento,
        fechaIngreso,
        ciudadProcedencia,
        email,
        cantidadMatriculas,
        blobFoto,
    )
    return infoEstudiante


def insertarTablaEstudiante(con, infoEstudiante):
    cursorObj = con.cursor()  # recorremos la base de datos con el objeto de conexión
    cursorObj.execute(
        """INSERT INTO estudiantes VALUES (?,?,?,?,?,?,?,?,?,?)""", infoEstudiante
    )
    # insertamos información en la tabla materias
    con.commit()  # guarda la tabla en el drive


def actualizarTablaEstudiante(con, idEstudiante, columna):
    cursorObjt = con.cursor()  # cursor recorrer base de datos
    nuevoValor = input("Ingrese información actualizada: ")
    actualizar = (
        'UPDATE estudiantes SET "'
        + columna
        + '" ="'
        + nuevoValor
        + '"WHERE identificacion ="'
        + str(idEstudiante)
        + '"'
    )
    cursorObjt.execute(actualizar)
    con.commit()  # guardamos tabla en el drive


def consultarTablaEstudiantes(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT identificacion, nombre FROM estudiantes"
    )  # se puede usar "*" para consultar todos los campos
    filas = cursorObj.fetchall()
    print("El tipo de dato de filas es: ", type(filas))
    for row in filas:
        id = row[0]
        nombre = row[1]
        print("La información del estudiante es: ", id, nombre)
        print("La información de la lista es: ")
        print(row)


def consultarInfoEstudiante(con, id):
    cursorObj = con.cursor()
    cursorObj.execute(f"SELECT * FROM estudiantes WHERE identificacion = {id}")
    infoMateria = cursorObj.fetchall()
    for row in infoMateria:
        print("Id: ", row[0])
        print("Nombre: ", row[1], row[2])
        print("Carrera: ", row[3])
        print("Fecha de nacimiento: ", row[4])
        print("Fecha de ingreso: ", row[5])
        print("Ciudad de procedencia: ", row[6])
        print("Email: ", row[7])
        print("Cantidad de matrículas: ", row[8])


##Historia Académica


def crearTablaHistoria(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        f"""CREATE TABLE historia (identificacion integer , 
                                   codigo integer, 
                                     notaFinal real, 
                                     creditos integer, 
                                   PRIMARY KEY(identificacion, codigo))"""
    )
    con.commit()

def leerInfoHistoria():
    id = input("Numero de identificación: ")
    codigo = input("Código de la materia: ")
    notaFinal = input("Nota final: ")
    creditos = input("Número de créditos: ")
    infoEstudiante = (
        id,
        codigo,
        notaFinal,
        creditos,
    )
    return infoEstudiante

def insertarTablaHistoria(con, infoHistoria):
    cursorObj = con.cursor()  # recorremos la base de datos con el objeto de conexión
    cursorObj.execute(
        """INSERT INTO historia VALUES (?,?,?,?)""", infoHistoria
    )
    # insertamos información en la tabla materias
    con.commit()  # guarda la tabla en el drive


def consultarHistoriaAcademica(con, identificacion):
    cursorObj = con.cursor()
    cursorObj.execute(
        f"SELECT codigo, notaFinal, creditos FROM historia WHERE identificacion = {identificacion}",
    )  # se puede usar "*" para consultar todos los campos
    filas = cursorObj.fetchall()
    for row in filas:
        codigo = row[0]
        notaFinal = row[1]
        creditos = row[2]
        print("Codigo de la materia: ", codigo)
        print("La nota final es: ", notaFinal)
        print("Número de créditos: ", creditos, '\n')


def borrarinfoTablaHistoria(con, identificacion):
    cursorObjt = con.cursor()
    materiaBorrar = input("Codigo de la materia para borrar: ")
    borrar = f"DELETE FROM historia WHERE identificacion = {identificacion} AND codigo = {materiaBorrar}"
    cursorObjt.execute(borrar)
    con.commit()


def actualizarNota(con, identificacion):
    cursorObjt = con.cursor()  # cursor recorrer base de datos
    codigoMateria = input("Qué materia desea actualizar? ")
    nuevaNota = input("Actualice la nota: ")
    actualizar = f"UPDATE historia SET notaFinal = {nuevaNota} WHERE identificacion = {identificacion} AND codigo = {codigoMateria}"
    cursorObjt.execute(actualizar)
    con.commit()  # guardamos tabla en el drive


##Clasificación


def crearTablaClasificación(con, identificacion, codigo):
    cursorObj = con.cursor()
    cursorObj.execute(
        f"""CREATE TABLE historia (identificacion integer , 
                                   nombre text, 
                                     apellido text, 
                                     cantidadMateriasTomadas integer, 
                                   creditosAcumulados integer,
                                   promedio integer
                                   )"""
    )
    con.commit()


def cerrarBD(con):
    con.close()


def menu(Con):
    salirPrincipal = False
    while not salirPrincipal:
        opc = input(
            """
                    Menú de Opciones
                    1. Materias
                    2. Estudiante
                    3. Historia Académica
                    4. Clasificación
                    5. Salir
                    Seleccione opción>>> """
        )
        if opc == "1":
            salirMaterias = False
            while not salirMaterias:
                opcionMaterias = input(
                    """
                                       Menú de Materias
                                       1. Leer información de la materia
                                       2. Insertar Materias
                                       3. Consultar Materias
                                       4. Actualizar Materias
                                       5. Borrar materia
                                       6. Calcular promedio de los créditos
                                       7. Salir

                                       Seleccione opción: 
                                       """
                )
                if opcionMaterias == "1":
                    miMateria = leerInfoMaterias()
                elif opcionMaterias == "2":
                    insertarTablaMateria2(Con)
                elif opcionMaterias == "3":
                    consultarTablaMaterias(Con)
                elif opcionMaterias == "4":
                    actualizarTablaMaterias(Con, "123")
                elif opcionMaterias == "5":
                    borrarinfoTablaMaterias(Con)
                elif opcionMaterias == "6":
                    promedioTablaMaterias(Con)
                elif opcionMaterias == "7":
                    salirMaterias = True


def main():
    miCon = conexionALaBD()
    # # crearTablaMaterias(miCon)
    # miMateria = leerInfoMaterias()
    # insertarTablaMaterias(miCon, miMateria)
    # consultarTablaMaterias(miCon)
    # consultarInfoMateria(miCon, "4")
    # codMatact= input('Codigo de la materia a actualizar: ')
    # actualizarTablaMaterias(miCon, codMatact)
    # borrarinfoTablaMaterias(miCon)
    # promedioTablaMaterias(miCon)

    ##Estudiante
    # crearTablaEstudiante(miCon)
    # infoEstudiante = leerInfoEstudiante()
    # insertarTablaEstudiante(miCon, infoEstudiante)
    # actualizarTablaEstudiante(miCon, 123, 'apellido')
    # consultarTablaEstudiantes(miCon)
    # consultarInfoEstudiante(miCon, 123)
    
    ##Historia
    # crearTablaHistoria(miCon)
    infoHistoria = leerInfoHistoria()
    insertarTablaHistoria(miCon, infoHistoria)
    # consultarHistoriaAcademica(miCon, 123)
    # borrarinfoTablaHistoria(miCon, 123)
    actualizarNota(miCon, 123)

    # menu(miCon)
    cerrarBD(miCon)


main()
