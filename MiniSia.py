import sqlite3
from sqlite3 import Error


def conexionALaBD():  # Crea base de datos
    try:
        con = sqlite3.connect("MiBaseDatos.db")
        return con
    except Error:
        print(Error)


##MATERIAS


def crearTablaMaterias(con):  # Crea tabla de Materias
    cursorObj = con.cursor()
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS materias (codigo integer PRIMARY KEY, nombre text, facultadDicta text, departamentoDicta text, creditos integer, idioma text)"
    )
    con.commit()


def leerInfoMaterias():  # Pide al usuario información sobre las materias y la guarda en una tupla
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


def insertarTablaMaterias(
    con, materia
):  # Inserta la información de la tupla anterior en la base de datos
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


def borrarinfoTablaMaterias(con): #pide al usuario la materia que quiere borrar y la elimina de la tabla de materias
    cursorObjt = con.cursor()
    materiaBorrar = input("Codigo de la materia para borrar: ")
    borrar = 'DELETE FROM materias WHERE codigo ="' + materiaBorrar + '"'
    cursorObjt.execute(borrar)
    con.commit()


def promedioTablaMaterias(con): #calcula el promedio de los créditos
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT count (*) FROM materias"
    )  # cuenta el total de las materias inscritas
    cantidadMaterias = cursorObj.fetchall() # guarda el valor anterior en una lista
    for row in cantidadMaterias:
        cantidad = row[0]
    cursorObj.execute(
        "SELECT sum(creditos) FROM materias"
    )  # calcula la suma de los creditos de todas las materias inscritas
    sumatoriaCreditos = cursorObj.fetchall()
    for row in sumatoriaCreditos:
        sumatoria = row[0]
    promedio = sumatoria / cantidad
    print("El promedio de los creditos de las materias es: ", promedio)


def consultarTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT codigo, nombre FROM materias"
    )  # recopila el valor de las columnas "codigo" y "nombre" para cada fila
    filas = cursorObj.fetchall() # se guardan los codigos y los nombres de las materias una lista
    print("El tipo de dato de filas es: ", type(filas))
    for row in filas: # se itera la lista para imprimir el nombre y el código de cada materia
        codigo = row[0]
        nombre = row[1]
        print("La información de la materia es: ", codigo, nombre)
        print("La información de la lista es: ")
        print(row)


def consultarInfoMateria(con, codigo):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM materias WHERE codigo = ?", codigo) #filtra la información de la materia especificada por su código
    infoMateria = cursorObj.fetchall() # guarda la información de la materia en una lista
    for row in infoMateria: #Se itera la lista para imprimir cada característica de la materia
        print("Código: ", row[0])
        print("Nombre: ", row[2])
        print("Facultad: ", row[2])
        print("Departamento: ", row[3])
        print("Créditos: ", row[4])
        print("Idioma: ", row[5])


##ESTUDIANTE


def crearTablaEstudiante(con):
    cursorObj = con.cursor() #crea la tabla de estudiantes
    cursorObj.execute(
        f"""CREATE table IF NOT EXISTS estudiantes (identificacion integer PRIMARY KEY, 
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


def importarFoto(ubicacionArchivo): #permite leer un archivo en formato binario
    with open(ubicacionArchivo, "rb") as file:
        blobFoto = file.read()
    return blobFoto


def leerInfoEstudiante():
    id = input("Numero de identificación: ") #se pide al usuario la información personal
    nombre = input("Nombre del estudiante: ")
    apellido = input("Apellido del estudiante: ")
    carrera = input("Plan de estudios: ")
    fechaNacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
    fechaIngreso = input("Fecha de ingreso (dd/mm/aaaa): ")
    ciudadProcedencia = input("Ciudad de procedencia: ")
    email = input("Email: ")
    cantidadMatriculas = input("Cantidad de matrículas: ")
    foto = input("Ubicación completa de la fotografía (PATH): ")
    blobFoto = importarFoto(foto) #la imagen en formato binario se asigna a una variable
    infoEstudiante = (  # se guarda la información personal y la imagen en una tupla
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
    cursorObj = con.cursor()  # asigna los valores de la tupla anterior a una fila nueva en la tabla
    cursorObj.execute(
        """INSERT INTO estudiantes VALUES (?,?,?,?,?,?,?,?,?,?)""", infoEstudiante
    )
    con.commit()  # guarda la tabla en el drive


def actualizarTablaEstudiante(con, idEstudiante, columna):
    cursorObjt = con.cursor()  # dado el id de un estudiante permite actualizar los datos de una columna especificada
    nuevoValor = input("Ingrese información actualizada: ")
    actualizar = (
        'UPDATE estudiantes SET "'
        + columna  
        + '" ="'
        + nuevoValor  # remplaza por el nuevo valor
        + '"WHERE identificacion ="'
        + str(idEstudiante)
        + '"'
    )
    cursorObjt.execute(actualizar)
    con.commit()  # guardamos tabla en el drive


def consultarTablaEstudiantes(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT identificacion, nombre FROM estudiantes" #recopila el nombre y la identificación de todos los estudiantes en una lista
    )  
    filas = cursorObj.fetchall() 
    for row in filas: #itera la lista para imprimir la información de cada estudiante
        id = row[0]
        nombre = row[1]
        print("La información del estudiante es: ", id, nombre)
        print("La información de la lista es: ")
        print(row)


def consultarInfoEstudiante(con, id):
    cursorObj = con.cursor()
    cursorObj.execute(f"SELECT * FROM estudiantes WHERE identificacion = {id}") #dado el id de un estudiante, recopila todos sus datos en una lista
    infoMateria = cursorObj.fetchall()
    for row in infoMateria: #itera la lista para imprimir dato por dato
        print("Id: ", row[0])
        print("Nombre: ", row[1], row[2])
        print("Carrera: ", row[3])
        print("Fecha de nacimiento: ", row[4])
        print("Fecha de ingreso: ", row[5])
        print("Ciudad de procedencia: ", row[6])
        print("Email: ", row[7])
        print("Cantidad de matrículas: ", row[8])


##Historia Académica


def crearTablaHistoria(con): #se crea la tabla de historia académica con dos claves primarias: identificación del estudiante y código de la materia
    cursorObj = con.cursor()
    cursorObj.execute(
        f"""CREATE table IF NOT EXISTS historia (identificacion integer , 
                                   codigo integer, 
                                     notaFinal real, 
                                     creditos integer, 
                                   PRIMARY KEY(identificacion, codigo))"""
    )
    con.commit()


def leerInfoHistoria(con): #pide al usuario datos de las materias cursadas
    id = pedirNumeroDeIdentificación(con, "crear una historia académica")  # pide al usuario su número de identificación
    codigo = input("Código de la materia: ")
    notaFinal = input("Nota final: ")
    creditos = input("Número de créditos: ")
    infoEstudiante = (  # guardo los datos de la materia y el usuario en una tupla
        id,
        codigo,
        notaFinal,
        creditos,
    )
    return infoEstudiante


def insertarTablaHistoria(con, infoHistoria):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO historia VALUES (?,?,?,?)""", infoHistoria)  # agrega los datos de la tupla a la tabla
    con.commit()  # guarda la tabla en el drive


def consultarHistoriaAcademica(con, identificacion):
    cursorObj = con.cursor()
    cursorObj.execute(
        f"SELECT codigo, notaFinal, creditos FROM historia WHERE identificacion = {identificacion}"  # recopila la nota, los creditos y el codigo de todas las materias que el usuario ha visto en una lista
    )  
    filas = cursorObj.fetchall()
    for row in filas: #itera la lista e imprime la información básica de las materias cursadas
        codigo = row[0]
        notaFinal = row[1]
        creditos = row[2]
        print("Codigo de la materia: ", codigo)
        print("La nota final es: ", notaFinal)
        print("Número de créditos: ", creditos, "\n")


def borrarinfoTablaHistoria(con, identificacion):
    cursorObjt = con.cursor()
    materiaBorrar = input("Codigo de la materia para borrar: ")
    borrar = f"DELETE FROM historia WHERE identificacion = {identificacion} AND codigo = {materiaBorrar}"  # dados un numero de id y un codigo de materia, se elimina la materia de la historia académica
    cursorObjt.execute(borrar)
    con.commit()


def actualizarNota(con, identificacion): #dados un numero de id y un código de materia, se pide la nota correcta para ser corregida en la tabla
    cursorObjt = con.cursor()  
    codigoMateria = input("Qué materia desea actualizar? ")
    nuevaNota = input("Actualice la nota: ")
    actualizar = f"UPDATE historia SET notaFinal = {nuevaNota} WHERE identificacion = {identificacion} AND codigo = {codigoMateria}" #se actualiza la nota en la tabla
    cursorObjt.execute(actualizar)
    con.commit()  # guardamos tabla en el drive


##Clasificación


def crearTablaClasificación(con): #se crea una tabla donde se van a almacenar los promedios de los estudiantes para ser clasificados de mayor a menor
    cursorObj = con.cursor()
    cursorObj.execute(
        f"""CREATE table IF NOT EXISTS clasificacion (identificacion integer , 
                                   nombre text, 
                                     apellido text, 
                                     cantidadMateriasTomadas integer, 
                                   creditosAcumulados integer,
                                   promedio real
                                   )"""
    )
    con.commit()

# cuando queremos añadir las materias junto con sus notas y créditos para cada estudiante, toca hacerlo en la tabla de historia académica. También sabemos que 
# # hay una tabla de estudiantes donde se guardan sus datos personales. Es decir, que el id como PRIMARY KEY está en la tabla de historia académica y en la tabla
# estudiantes, por tanto, para evitar que se creen historias académicas de estudiantes que no están registrados
# en la tabla de estudiantes, es necesaria la siguiente función.

def pedirNumeroDeIdentificación(con, text):
    cursorObj = con.cursor()
    cursorObj.execute("""SELECT identificacion FROM estudiantes""")
    ids = cursorObj.fetchall()
    idSet = {str(i[0]) for i in ids} #se crea un conjunto con todos los ids de los usarios registrados en la tabla de estudiantes
    while True:
        print("Números de identificación almacenados en la tabla estudiantes: ")
        print(idSet)
        id = input(
            f"Ingrese el número de identificación del estudiante que quiere {text}: " #pide el id al usuario
        )
        if id in idSet: #verifica que el id ingresado ya esté registrado en estudiantes
            break
    return id


def actualizarTablaClasificacion(con):

    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM clasificacion") #todos los valores de la tabla de clasificación se calculan con los valores de las tablas 'estudiante' e 'historia'
    #entonces cada vez que se quiere actualizar la clasificación es más fácil borrar todos los valores de esta tabla e insertar de nuevo todos los valores 
    #que se obtienen a partir de 'estudiante' e 'historia'
    cursorObj.execute("""SELECT identificacion FROM historia""") #recolecta los ids de los usuarios que tienen historia académica

    ids = cursorObj.fetchall()
    # como los ids se repiten en la tabla de historia académica, se crea un conjunto para que aparezcan solo una vez
    idSet = {i[0] for i in ids}

    for i in idSet: # se itera el conjunto de los usuarios que tienen historia académica
        #se hacen los cálculos respectivos a partir de la historia académica para obtener promedios, creditos totales, etc. y se extrae el nombre y el apellido
        #para cada estudiante a partir de la tabla 'estudiante'

        sumaCreditos = cursorObj.execute(
            f"""SELECT  SUM(creditos) FROM historia WHERE identificacion = {i}"""
        )
        sumaCreditos = sumaCreditos.fetchall()

        promedio = cursorObj.execute(
            f"""SELECT  AVG(notaFinal) FROM historia WHERE identificacion = {i}"""
        )
        promedio = promedio.fetchall()

        cantidadMaterias = cursorObj.execute(
            f"""SELECT  COUNT(identificacion) FROM historia WHERE identificacion = {i}"""
        )
        cantidadMaterias = cantidadMaterias.fetchall()

        nombre = cursorObj.execute(
            f"""SELECT  nombre FROM estudiantes WHERE identificacion = {i}"""
        )
        nombre = nombre.fetchall()

        apellido = cursorObj.execute(
            f"""SELECT  apellido FROM estudiantes WHERE identificacion = {i}"""
        )
        apellido = apellido.fetchall()

        row = ( # se guardan los datos pertinentes para la clasificación en una tupla
            i,
            nombre[0][0],
            apellido[0][0],
            cantidadMaterias[0][0],
            sumaCreditos[0][0],
            promedio[0][0],
        )
        rowStrings = (str(i) for i in row)
        cursorObj.execute("INSERT INTO clasificacion VALUES (?,?,?,?,?,?)", row) # se agrega la tupla a la tabla

    con.commit()
    # for i in idSet:


def consultaClasificacion(con):
    actualizarTablaClasificacion(con)
    cursorObj = con.cursor()
    clasificacion = cursorObj.execute(
        "SELECT nombre, apellido, promedio FROM clasificacion ORDER BY promedio DESC" #se organiza la tabla de mayor a menor según el promedio de los estudiantes
    )
    posicion = 0 #
    for i in clasificacion: # itera la tabla organizada e imprime la información de los estudiantes  
        posicion += 1
        print("Posición", posicion)
        print("Nombre:", i[0], i[1])
        print("Nota:", i[2], "\n")


def consultaPosicionSegunId(con, id): #hace lo mismo que la función anterior pero en vez de imprimir todos los estudiantes siguiendo el orden de su promedio, 
#imprime la informacion de un estudiante determinado y su posición en la clasificación
    actualizarTablaClasificacion(con)
    cursorObj = con.cursor()
    clasificacion = cursorObj.execute(
        f"SELECT * FROM clasificacion ORDER BY promedio DESC"
    )

    posicion = 0
    for i in clasificacion:
        posicion += 1
        if id == i[0]:
            print("Posición", posicion)
            print("Nombre:", i[1], i[2])
            print("Cantidad de materias cursadas:", i[3])
            print("Créditos acumulados:", i[4])
            print("Promedio: ", i[5])

            break


def cerrarBD(con):
    con.close()


def menu(con):
    salirPrincipal = False
    while not salirPrincipal:
        opcPrincipal = input(
            """
        Menu de opciones

        1. Materias
        2. Estudiante
        3. Historia Académica
        4. Clasificación
        5. Salir

        Seleccione opción>>>: """
        )
        if opcPrincipal == "1":
            salirMaterias = False
            while not salirMaterias:
                opcionMaterias = input(
                    """
                Menu de Materias

                1. Insertar Materia leyendo información
                2. Insertar Materia sin leer infromación
                3. Consultar Materia
                4. Actualizar Materia
                5. Borrar Materia
                6. Calcular promedio de los créditos
                7. Salir

                Seleccione opción>>>: """
                )
                if opcionMaterias == "1":
                    miMateria = leerInfoMaterias()
                    insertarTablaMaterias(con, miMateria)
                elif opcionMaterias == "2":
                    insertarTablaMateria2(con)
                elif opcionMaterias == "3":
                    consultarTablaMaterias(con)
                elif opcionMaterias == "4":
                    codmatact = input("Codigo de la materia a actualizar: ")
                    actualizarTablaMaterias(con, codmatact)
                elif opcionMaterias == "5":
                    borrarinfoTablaMaterias(con)
                elif opcionMaterias == "6":
                    promedioTablaMaterias(con)
                elif opcionMaterias == "7":
                    salirMaterias = True

        elif opcPrincipal == "2":
            salirEstudiantes = False
            while not salirEstudiantes:
                opcionEstudiantes = input(
                    """
                Menu de Estudiantes

                1. Crear Estudiante
                2. Actualizar Estudiante
                3. Consultar tabla de estudiantes
                4. Consultar Estudiante
                5. Salir

                Seleccione opción>>>: """
                )
                if opcionEstudiantes == "1":
                    estudiante = leerInfoEstudiante()
                    insertarTablaEstudiante(con, estudiante)
                elif opcionEstudiantes == "2":
                    id = pedirNumeroDeIdentificación(con, "actualizar datos")
                    dato = input(
                        "Ingrese el atributo del estudiante que desea actualizar: "
                    )
                    actualizarTablaEstudiante(con, id, dato)
                elif opcionEstudiantes == "3":
                    consultarTablaEstudiantes(con)
                elif opcionEstudiantes == "4":
                    id = pedirNumeroDeIdentificación(con, "consultar datos")
                    consultarInfoEstudiante(con, id)
                elif opcionEstudiantes == "5":
                    salirEstudiantes = True

        elif opcPrincipal == "3":
            salirHistoriaAcademica = False
            while not salirHistoriaAcademica:
                opcionHistoriaAcademica = input(
                    """
                Menu de Historia Academica

                1. Crear nueva historia academica
                2. Consultar historia académica de estudiante
                3. Borrar materia de la historia académica de un estudiante
                4. Actualizar nota de materia de un estudiante
                5. Salir

                Seleccione opción>>>: """
                )
                if opcionHistoriaAcademica == "1":
                    historia = leerInfoHistoria(con)
                    insertarTablaHistoria(con, historia)
                elif opcionHistoriaAcademica == "2":
                    identificacion = pedirNumeroDeIdentificación(
                        con, "consultar la historia académica"
                    )
                    consultarHistoriaAcademica(con, identificacion)
                elif opcionHistoriaAcademica == "3":
                    identificacion = pedirNumeroDeIdentificación(
                        con, "borrar una materia de la historia académica"
                    )
                    borrarinfoTablaHistoria(con, identificacion)
                elif opcionHistoriaAcademica == "4":
                    identificacion = pedirNumeroDeIdentificación(
                        con, "actualizar la nota"
                    )
                    actualizarNota(con, identificacion)
                elif opcionHistoriaAcademica == "5":
                    salirHistoriaAcademica = True

        elif opcPrincipal == "4":
            salirClasificacion = False
            while not salirClasificacion:
                opcionClasificacion = input(
                    """
                Menu de Clasificación

                1. Consulta clasificación del estudiante
                2. Consulta tabla de clasificación
                3. Salir

                Seleccione opción>>>: """
                )
                if opcionClasificacion == "1":
                    consultaClasificacion(con)
                elif opcionClasificacion == "2":
                    identificacion = pedirNumeroDeIdentificación(
                        con, "consultar su clasificación"
                    )
                    consultaPosicionSegunId(con, identificacion)
                elif opcionClasificacion == "3":
                    salirClasificacion = True

        elif opcPrincipal == "5":
            salirPrincipal = True
    print(
        """
        Programa Finalizado. Gracias por utilizar nuestros servicios
    """
    )


def main():
    miCon = conexionALaBD()
    crearTablaMaterias(miCon)
    # miMateria = leerInfoMaterias()
    # insertarTablaMaterias(miCon, miMateria)
    # consultarTablaMaterias(miCon)
    # consultarInfoMateria(miCon, "4")
    # codMatact= input('Codigo de la materia a actualizar: ')
    # actualizarTablaMaterias(miCon, codMatact)
    # borrarinfoTablaMaterias(miCon)
    # promedioTablaMaterias(miCon)

    ##Estudiante
    crearTablaEstudiante(miCon)
    # infoEstudiante = leerInfoEstudiante()
    # insertarTablaEstudiante(miCon, infoEstudiante)
    # actualizarTablaEstudiante(miCon, 123, 'apellido')
    # consultarTablaEstudiantes(miCon)
    # consultarInfoEstudiante(miCon, 123)

    ##Historia
    crearTablaHistoria(miCon)
    # infoHistoria = leerInfoHistoria()
    # insertarTablaHistoria(miCon, infoHistoria)
    # consultarHistoriaAcademica(miCon, 123)
    # borrarinfoTablaHistoria(miCon, 123)
    # actualizarNota(miCon, 123)

    ##Clasificación
    crearTablaClasificación(miCon)
    # actualizarTablaClasificacion(miCon)
    # consultaClasificacion(miCon)
    # consultaPosicionSegunId(miCon, 234)

    menu(miCon)
    cerrarBD(miCon)


main()
