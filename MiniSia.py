import sqlite3
from sqlite3 import Error
import datetime

# Crea base de datos
def conexionALaBD():
    try:
        con = sqlite3.connect("MiBaseDatos.db")
        return con
    except Error:
        print(Error)

###VALIDACIONES DE DATOS

#Esta función retorna la lista de los números de identificación que estan almacenados en la tabla de estudiantes
#Será útil para verificar si algún NI ya existe o no
def listaNumerosDeIdentificacion(con):
    cursorObj = con.cursor()
    cursorObj.execute("""SELECT identificacion FROM estudiantes""")
    ids = cursorObj.fetchall()
    idSet = {str(i[0]) for i in ids} #se crea un conjunto con todos los ids de los usarios registrados en la tabla de estudiantes
    return idSet

#Esta función se llama cuando se quiere pedir un número de identificación existente
#Esta función muestra los números de identificación existentes, hace ciclos que validan si el NI que digite el usuario existe, si es así sale del ciclo y retorna el NI
#Esta función usa consultarTablaEstudiantes(con) para mostrar los NI almacenados en la BD
def pedirNumeroDeIdentificacion(con, text):
    idSet = listaNumerosDeIdentificacion(con)
    while True:
        consultarTablaEstudiantes(con)
        id = input(text)
        if id in idSet: #verifica que el id ingresado ya esté registrado en estudiantes
            break
        else:
            print('El número de identificación ingresado no aparece en la lista')
    return id

#Esta función retorna la lista de los códigos de materias que estan almacenados en la tabla de materias
#Será útil para verificar si algún códido de materia ya existe o no
def listaCodigosDeMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute("""SELECT codigo FROM materias""")
    cods = cursorObj.fetchall()
    codsSet = {str(i[0]) for i in cods} #se crea un conjunto con todos los ids de los usarios registrados en la tabla de estudiantes
    return codsSet

#Esta función se llama cuando se quiere pedir un códido de materia existente
#Esta función muestra los códidos de materias existentes, hace ciclos que validan si el COD que digite el usuario existe, si es así sale del ciclo retorna el COD
#Esta función usa consultarTablaMaterias(con) para mostrar los códidos de materias en la BD
def pedirCodigoDeMateria(con,text):
    idSet = listaCodigosDeMaterias(con)
    while True:
        consultarTablaMaterias(con)
        id = input(text)
        if id in idSet: #verifica que el id ingresado ya esté registrado en estudiantes
            break
        else:
            print("El código ingresado no se encuentra en la lista de materias, por favor ingrese otro código")
    return id

#Función que es llamada cuando se le pude al usuario un dato numérico
#Hace ciclos hasta que el usuario digite un dato compuesto enteramente por numeros, si es así retorna el dato
def pedirDatoNumerico(text):
    while True:
        numero = input(text)
        if not numero.isnumeric():
            print('El dato ingresado no es un número')
        else:
            break
    return numero

#Función que es llamada cuando se le pude al usuario un dato de texto
#Hace ciclos hasta que el usuario digite un dato que no está compuesto enteramente por numeros, si es así retorna el dato
def pedirDatoTexto(text):
    while True:
        texto = input(text)
        if texto.isnumeric():
            print('El dato ingresado no puede contener números')
        else:
            break
    return texto

#Función que es llamada cuando se le pude al usuario un dato de fecha
#Hace ciclos hasta que el usuario digite una fecha con el formato indicado, si es así retorna la fecha
def pedirFecha(text):
    while True:
        try:
            fecha = input(f'Ingrese la fecha de {text} formato AAAA/MM/DD: ')
            testFecha = datetime.datetime.strptime(fecha, '%Y/%m/%d') #Se usa el módulo datetime para verificar si la fecha es válida
            break
        except:
            print('Ingresó una fecha incorrecta o un formato erróneo')
    return fecha

#Función que es llamada cuando se le pude al usuario un correo electrónico
#Hace ciclos hasta que el usuario digite una fecha con el formato indicado, si es así retorna la fecha
def pedirEmail():
    unal = True
    while True:
        correo = input("Ingrese el correo electrónico: ")
        if correo.endswith("@unal.edu.co"):
            break
        else:
            print("Correo inválido, verifique que su correo termine en @unal.edu.co")
    return correo



##MATERIAS

# Esta funcíon verifica si existe una tabla de materias, si no es así crea tabla de Materias
def crearTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "CREATE TABLE IF NOT EXISTS materias (codigo integer PRIMARY KEY, nombre text, facultadDicta text, departamentoDicta text, creditos integer, idioma text)"
    )
    con.commit()

#Pide al usuario información sobre las materias y la guarda en una tupla
#Verifica los datos ingresados con pedirDatoTexto y pedirDatoNumerico
#Para el código de las materias verifica si el código ingresado ya existe usando listaCodigosDeMaterias(con), así evita que hallan dos códigos iguales
def leerInfoMaterias(con):  
    while True:
        codigo = input("Codigo de la materia: ")
        if not codigo.isnumeric():
            print('El dato ingresado no es un número')
        elif codigo in listaCodigosDeMaterias(con):
            print('Este número ya está registrado en la base de datos')
        else:
            break
    codigo = codigo.ljust(12)  # ajusta a la izquierda 12 posiciones
    nombre = pedirDatoTexto("Nombre de la materia: ")
    facultadDicta = pedirDatoTexto("Facultad que la dicta: ")
    departamentoDicta = pedirDatoTexto("Departamento que la dicta: ")
    creditos = pedirDatoNumerico("Cantidad de créditos: ")
    idioma = pedirDatoTexto("Idioma en que se dicta: ")
    materia = (codigo, nombre, facultadDicta, departamentoDicta, creditos, idioma)
    #print("La información de la materia es: ", materia)
    return materia

# Esta función es llamada después de leerInfoMaterias(con)
# Inserta la información de la tupla anterior en la base de datos
def insertarTablaMaterias(con, materia):  
    cursorObj = con.cursor()  # recorremos la base de datos con el objeto de conexión
    cursorObj.execute("""INSERT INTO materias VALUES (?,?,?,?,?,?)""", materia)
    # insertamos información en la tabla materias
    con.commit()  # guarda la tabla en el drive

# Esta función inserta una materia con valores predeterminados, a excepcion del código
#Para el código de las materias verifica si el código ingresado ya existe usando listaCodigosDeMaterias(con), así evita que hallan dos códigos iguales
def insertarTablaMateria2(con):
    cursorObj = con.cursor()  # recorremos la base de datos con el objeto de conexión
    # cursorObj.execute('''INSERT INTO materias VALUES (?,?,?,?,?,?)''', materia)
    while True:
        codigo = input("Codigo de la materia: ")
        if not codigo.isnumeric():
            print('El dato ingresado no es un número')
        elif codigo in listaCodigosDeMaterias(con):
            print('Este número ya está registrado en la base de datos')
        else:
            break
    cad = 'INSERT INTO materias VALUES ("'+codigo+'", "poo", "ing", "sist", "3", "español")'
    print("El SQL a ejecutar es ", cad)
    cursorObj.execute(cad)
    # insertamos información en la tabla materias
    con.commit()  # guarda la tabla en el drive

#Esta función se usa para actualizar el idioma de una materia
def actualizarTablaMaterias(con, codMat):
    cursorObjt = con.cursor()  # cursor recorrer base de datos
    nuevoidioma = pedirDatoTexto("Actualice el idioma: ")
    actualizar = (
        'UPDATE materias SET idioma ="'
        + nuevoidioma
        + '"WHERE codigo ="'
        + codMat
        + '"'
    )
    cursorObjt.execute(actualizar)
    con.commit()  # guardamos tabla en el drive

#Esta función pide al usuario la materia que quiere borrar y la elimina de la tabla de materias
def borrarinfoTablaMaterias(con): 
    cursorObjt = con.cursor()
    materiaBorrar = pedirCodigoDeMateria("Codigo de la materia para borrar: ")
    borrar = 'DELETE FROM materias WHERE codigo ="' + materiaBorrar + '"'
    cursorObjt.execute(borrar)
    con.commit()

#Esta función calcula el promedio de los créditos de las materias
def promedioTablaMaterias(con): 
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

#Esta función de usa para mostrar los Codigos y los Nombres de las materias almacendadas en la tabla de materias
def consultarTablaMaterias(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT codigo, nombre FROM materias"
    )  # recopila el valor de las columnas "codigo" y "nombre" para cada fila
    filas = cursorObj.fetchall() # se guardan los codigos y los nombres de las materias una lista
    print("Códigos de materias y nombres de materias almacenados en la base de datos: ")
    for row in filas: # se itera la lista para imprimir el nombre y el código de cada materia
        codigo = row[0]
        nombre = row[1]
        print(f'id: {codigo:>15}       nombre: {nombre:>30}')

#Esta función muestra los datos de una materia en específico, dependiendo del código que entra como argumento
def consultarInfoMateria(con, codigo):
    cursorObj = con.cursor()
    cursorObj.execute(f"SELECT * FROM materias WHERE codigo = {codigo}") #filtra la información de la materia especificada por su código
    infoMateria = cursorObj.fetchall() # guarda la información de la materia en una lista
    for row in infoMateria: #Se itera la lista para imprimir cada característica de la materia
        print("{:<15}{:>40}".format("Código: ", row[0]))
        print("{:<15}{:>40}".format("Nombre: ", row[2]))
        print("{:<15}{:>40}".format("Facultad: ", row[2]))
        print("{:<15}{:>40}".format("Departamento: ", row[3]))
        print("{:<15}{:>40}".format("Créditos: ", row[4]))
        print("{:<15}{:>40}".format("Idioma: ", row[5]))


##ESTUDIANTE

# Esta funcíon verifica si existe una tabla de estudiantes, si no es así crea tabla de estudiantes
def crearTablaEstudiante(con):
    cursorObj = con.cursor() 
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

#Función que retorna en blob una foto, para luego ser almacenada como foro de estudiante
def importarFoto(ubicacionArchivo): #permite leer un archivo en formato binario
    with open(ubicacionArchivo, "rb") as file:
        blobFoto = file.read()
    return blobFoto

#Pide al usuario información sobre un estudiante y la guarda en una tupla
#Verifica los datos ingresados con pedirDatoTexto, pedirDatoNumerico, pedirFecha y pedirEmail
#Para el número de identificación del estudiante verifica si el NI ingresado ya existe usando listaNumerosDeIdentificacion(con), así evita que hallan dos NI iguales
def leerInfoEstudiante(con):
    while True:
        id = input("Numero de identificación: ")
        if not id.isnumeric():
            print('El dato ingresado no es un número')
        elif id in listaNumerosDeIdentificacion(con):
            print('Este número ya está registrado en la base de datos')
        else:
            break
    nombre = pedirDatoTexto("Nombre del estudiante: ")
    apellido = pedirDatoTexto("Apellido del estudiante: ")
    carrera = pedirDatoTexto("Plan de estudios: ")
    fechaNacimiento = pedirFecha("nacimiento")
    fechaIngreso = pedirFecha("ingreso")
    ciudadProcedencia = pedirDatoTexto("Ciudad de procedencia: ")
    email = pedirEmail()
    cantidadMatriculas = pedirDatoNumerico("Cantidad de matrículas: ")
    foto = pedirDatoTexto("Ubicación completa de la fotografía (PATH): ")
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

# Esta función es llamada después de leerInfoEstudiante(con)
# Inserta la información de la tupla anterior en la base de datos
def insertarTablaEstudiante(con, infoEstudiante):
    cursorObj = con.cursor()  # asigna los valores de la tupla anterior a una fila nueva en la tabla
    cursorObj.execute(
        """INSERT INTO estudiantes VALUES (?,?,?,?,?,?,?,?,?,?)""", infoEstudiante
    )
    con.commit()  # guarda la tabla en el drive

#Esta función recibe el NI de un estudiante y permite modificar un dato de un estudiante
#Hace ciclos preguntandole al usuario que dato quiere modificar de una lista. Si el dato está en la lista se le pide el nuevo valor del dato sino está se le pregunta de nuevo
#Se usan las funciones de verificación de datos dependiendo de que dato quiera modificar el usuario
def actualizarTablaEstudiante(con, idEstudiante):
    cursorObjt = con.cursor()  # dado el id de un estudiante permite actualizar los datos de una columna especificada
    while True:
        columna=input('''
        Ingrese el atributo del estudiante que desea actualizar:
        identificacion, nombre, apellido, carrera, fechaNacimiento, fechaIngreso, ciudadProcedencia, email, cantidadMatriculas, fotografia
        ''')
        if columna in ('identificacion','cantidadMatriculas'):
            nuevoValor = pedirDatoNumerico("Ingrese información actualizada: ")
            break
        elif columna in ('nombre','apellido','carrera','ciudadProcedencia','email','fotografia'):
            nuevoValor = pedirDatoTexto("Ingrese información actualizada: ")
            break
        elif columna in ('fechaNacimiento','fechaIngreso'):
            nuevoValor = pedirFecha(columna.replace('fecha','').lower())
            break
        else:
            print('Ingrese un atributo válido')
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

#Esta función de usa para mostrar los NI y el nombres compeltos de los estudiantes almacendadas en la tabla de estudiantes
def consultarTablaEstudiantes(con):
    cursorObj = con.cursor()
    cursorObj.execute(
        "SELECT identificacion, nombre, apellido FROM estudiantes" #recopila el nombre y la identificación de todos los estudiantes en una lista
    )  
    filas = cursorObj.fetchall()
    print("La información de los estudiantes es: ")
    for row in filas: #itera la lista para imprimir la información de cada estudiante
        id = row[0]
        nombrecompleto = row[1]+' '+row[2]
        print(f'id: {id:>15}       nombre: {nombrecompleto:>30}')

#Esta función muestra los datos de un estudiante en específico, dependiendo del NI que entra como argumento
def consultarInfoEstudiante(con, id):
    cursorObj = con.cursor()
    cursorObj.execute(f"SELECT * FROM estudiantes WHERE identificacion = {id}") #dado el id de un estudiante, recopila todos sus datos en una lista
    infoMateria = cursorObj.fetchall()
    for row in infoMateria: #itera la lista para imprimir dato por dato
        print("{:<24}{:>30}".format("Id: ", row[0]))
        print("{:<24}{:>30}".format("Nombre: ", row[1]+" "+row[2]))
        print("{:<24}{:>30}".format("Carrera: ", row[3]))
        print("{:<24}{:>30}".format("Fecha de nacimiento: ", row[4]))
        print("{:<24}{:>30}".format("Fecha de ingreso: ", row[5]))
        print("{:<24}{:>30}".format("Ciudad de procedencia: ", row[6]))
        print("{:<24}{:>30}".format("Email: ", row[7]))
        print("{:<24}{:>30}".format("Cantidad de matrículas: ", row[8]))



##Historia Académica

# Esta funcíon verifica si existe una tabla de historia, si no es así crea tabla de historia
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

#Pide al usuario información sobre una historia académica y la guarda en una tupla
#Verifica los datos ingresados con pedirDatoNumerico
#Usa pedirNumeroDeIdentificacion y pedirCodigoDeMateria para pedir datos ya existentes de NI de estudiante y cod de materia
def leerInfoHistoria(con): #pide al usuario datos de las materias cursadas
    id = pedirNumeroDeIdentificacion(con,"Numero de identidicación del estudiante de la historia académica: ")  # pide al usuario su número de identificación
    codigo = pedirCodigoDeMateria(con, "Código de la materia de la historia académica: ")
    notaFinal = pedirDatoNumerico("Nota final: ")
    cursorObj = con.cursor()
    cursorObj.execute(f"SELECT creditos FROM materias WHERE codigo = {codigo}")
    creditos = cursorObj.fetchall()[0][0]
    infoEstudiante = (  # guardo los datos de la materia y el usuario en una tupla
        id,
        codigo,
        notaFinal,
        creditos,
    )
    return infoEstudiante

# Esta función es llamada después de leerInfoHistoria(con)
# Inserta la información de la tupla anterior en la base de datos
def insertarTablaHistoria(con, infoHistoria):
    cursorObj = con.cursor()
    cursorObj.execute("""INSERT INTO historia VALUES (?,?,?,?)""", infoHistoria)  # agrega los datos de la tupla a la tabla
    con.commit()  # guarda la tabla en el drive

#Funcioón para consultar las historias academicas de un estudiante
#Esta función recibe un código de estudiante y muestra las historias académicas de ese estudiante (codigo de materia, nota y creditos)
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
        print("{:<22}{:>30}".format("Codigo de la materia: ", codigo))
        print("{:<22}{:>30}".format("La nota final es: ", notaFinal))
        print("{:<22}{:>30}\n".format("Número de créditos: ", creditos))

#Función para borrar una historia académica
#Esta función toma un NI de estudiante, un código de matera existentes y borra esa historia académica de la base de datos
def borrarinfoTablaHistoria(con, identificacion):
    cursorObjt = con.cursor()
    materiaBorrar = pedirCodigoDeMateria(con,"Codigo de la materia para borrar: ")
    borrar = f"DELETE FROM historia WHERE identificacion = {identificacion} AND codigo = {materiaBorrar}"  # dados un numero de id y un codigo de materia, se elimina la materia de la historia académica
    cursorObjt.execute(borrar)
    con.commit()

#Esta función toma un NI de estudiante existente, pregunta por un código de materia existente y permite acuatualizar la nota de dicha historia académica
def actualizarNota(con, identificacion): #dados un numero de id y un código de materia, se pide la nota correcta para ser corregida en la tabla
    cursorObjt = con.cursor()  
    codigoMateria = pedirCodigoDeMateria("Qué materia desea actualizar? ")
    nuevaNota = pedirDatoNumerico("Actualice la nota: ")
    actualizar = f"UPDATE historia SET notaFinal = {nuevaNota} WHERE identificacion = {identificacion} AND codigo = {codigoMateria}" #se actualiza la nota en la tabla
    cursorObjt.execute(actualizar)
    con.commit()  # guardamos tabla en el drive


##Clasificación

# Esta funcíon verifica si existe una tabla de clasificacion, si no es así crea tabla de clasificacion
def crearTablaClasificación(con): #se crea una tabla donde se van a almacenar los promedios de los estudiantes para ser clasificados de mayor a menor
    cursorObj = con.cursor()
    cursorObj.execute(
        f"""CREATE table IF NOT EXISTS clasificacion (identificacion integer PRIMARY KEY, 
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

#Muestra los datos de la tabla de clasificación
#Inicialente llama a actualizarTablaClasificacion en dado caso de que halla ocurrido algún cambio en el código
#Saca los datos de cada estudiante y los muestra en orden de promedio
def consultaClasificacion(con):
    actualizarTablaClasificacion(con)
    cursorObj = con.cursor()
    clasificacion = cursorObj.execute(
        "SELECT nombre, apellido, promedio FROM clasificacion ORDER BY promedio DESC" #se organiza la tabla de mayor a menor según el promedio de los estudiantes
    )
    posicion = 0 #
    for i in clasificacion: # itera la tabla organizada e imprime la información de los estudiantes  
        posicion += 1
        print("{:<10}{:>30}".format("Posición: ", posicion))
        print("{:<10}{:>30}".format("Nombre: ", i[0]+" "+i[1]))
        print("{:<10}{:>30}\n".format("Nota: ", i[2]))

#hace lo mismo que la función anterior pero en vez de imprimir todos los estudiantes siguiendo el orden de su promedio, imprime la informacion de un estudiante determinado y su posición en la clasificación
def consultaPosicionSegunId(con, id):
    actualizarTablaClasificacion(con)
    cursorObj = con.cursor()
    cursorObj.execute(
        f"SELECT * FROM clasificacion ORDER BY promedio DESC"
    )
    clasificacion = cursorObj.fetchall()
    posicion = 0
    for i in clasificacion:
        posicion += 1
        if id == str(i[0]):
            print("{:<31}{:>30}".format("Posición: ", posicion))
            print("{:<31}{:>30}".format("Nombre: ", i[1]+" "+i[2]))
            print("{:<31}{:>30}".format("Cantidad de materias cursadas: ", i[3]))
            print("{:<31}{:>30}".format("Créditos acumulados: ", i[4]))
            print("{:<31}{:>30}".format("Promedio: ", i[5]))
            break

#Funcion para cerrar la base de datos
def cerrarBD(con):
    con.close()

#Funcion de menú
#Permite navegar entre los menús
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
                3. Consultar Tabla Materias
                4. Consultar Materia
                5. Actualizar Materia
                6. Borrar Materia
                7. Calcular promedio de los créditos
                8. Salir
                Seleccione opción>>>: """
                )
                if opcionMaterias == "1":
                    miMateria = leerInfoMaterias(con)
                    insertarTablaMaterias(con, miMateria)
                elif opcionMaterias == "2":
                    insertarTablaMateria2(con)
                elif opcionMaterias == "3":
                    consultarTablaMaterias(con)
                elif opcionMaterias == "4":
                    codmatact = pedirCodigoDeMateria(con,"Código de materia a consultar: ")
                    consultarInfoMateria(con,codmatact)
                elif opcionMaterias == "5":
                    codmatact = pedirCodigoDeMateria(con,"Codigo de la materia a actualizar: ")
                    actualizarTablaMaterias(con, codmatact)
                elif opcionMaterias == "6":
                    borrarinfoTablaMaterias(con)
                elif opcionMaterias == "7":
                    promedioTablaMaterias(con)
                elif opcionMaterias == "8":
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
                    estudiante = leerInfoEstudiante(con)
                    insertarTablaEstudiante(con, estudiante)
                elif opcionEstudiantes == "2":
                    id = pedirNumeroDeIdentificacion(con,"Número de identificación del estudiante a actualizar datos: ")
                    actualizarTablaEstudiante(con, id)
                elif opcionEstudiantes == "3":
                    consultarTablaEstudiantes(con)
                elif opcionEstudiantes == "4":
                    id = pedirNumeroDeIdentificacion(con, "Número de identificación del estudante a consultar datos: ")
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
                    identificacion = pedirNumeroDeIdentificacion(
                        con, "Número de identificación del estudiante a consultar la historia académica: "
                    )
                    consultarHistoriaAcademica(con, identificacion)
                elif opcionHistoriaAcademica == "3":
                    identificacion = pedirNumeroDeIdentificacion(
                        con, "Número de identificación del estudiante que se borrará la historia académica: "
                    )
                    borrarinfoTablaHistoria(con, identificacion)
                elif opcionHistoriaAcademica == "4":
                    identificacion = pedirNumeroDeIdentificacion(
                        con, "Número de identificación del estudiante para actualizar la nota: "
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
                1. Consulta tabla de clasificación
                2. Consulta calsificación del estudiante
                3. Salir
                Seleccione opción>>>: """
                )
                if opcionClasificacion == "1":
                    consultaClasificacion(con)
                elif opcionClasificacion == "2":
                    identificacion = pedirNumeroDeIdentificacion(
                        con, "Número de identificación del estudiante a consultar su clasificación: "
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
