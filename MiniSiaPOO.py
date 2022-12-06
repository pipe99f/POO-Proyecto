import sqlite3
from sqlite3 import Error
import datetime
import guiMiniSia

###Clase DataBase
#Al inicializar un objeto con esta clase este actuará como una referencia a nuestra base de datos
#Esta clase tambien contiene metodos privados y de solo lectura (getter) para evitar cambios externos
class DataBase():
    def __init__(self):
        try:
            self.__con = sqlite3.connect('MiBaseDatos.db')
        except Error:
            print(Error)
    
    def cerrarBD(self):
        self.__con.close()
    
    #Solo lectura de una conección a la base de datos
    @property
    def con(self):
        return self.__con

###_MetodosSuper  (IMPORTANTE)
#Esta clase contiene metodos usados por todas las clases como lo son las verificaciones en el tipo de informacion ingresada
class _MetodosSuper():
    ###IMPORTANTE
    #Esta funcion __init__ se hereda a todas las clases como ClaseMaterias, ClaseEstudiantes, etc..

    #Como se puede ver esta función recibe una base de datos como argumento, esto es por si se quiere trabajar con dos bases de datos
    #si es así, solo basta con inicializar diferentes objetos materias, estudiantes, etc.. con distintas bases de datos
    def __init__(self, DB):
        ##Conexiones a una única base de datos
        self._DB = DB
        self._con = DB.con
        self._cursorObj = self._con.cursor()
        ##Cada subclase tendrá difetentes _tipoTabla y _datosTabla, estos se pasan por medio de self 
        self._cursorObj.execute(f'CREATE TABLE IF NOT EXISTS {self._tipoTabla} ({self._datosTabla})')

    
    #esta funcion _insertarTabla tambien se hereda
    #Esta función inserta en la respectiva tabla los valores del _arrayDatos
    #Se usa en funciones insertarMateria, insertarEstudiante y demás
    def _insertarTabla(self, arrayDatos):
        self._cursorObj.execute(f'''INSERT INTO {self._tipoTabla} VALUES ("{'","'.join(arrayDatos)}")''')
        # insertamos información en la tabla materias
        self._con.commit()  # guarda la tabla en el drive

    #Función que es llamada cuando se le pude al usuario un dato numérico
    #Hace ciclos hasta que el usuario digite un dato compuesto enteramente por numeros, si es así retorna el dato
    #Esta función se hereda y es @static porque es una verificación que no necesita de parametros de instancia o clase
    @staticmethod
    def _pedirDatoNumerico(text):
        while True:
            numero = input(text)
            if not numero.isnumeric():
                print('El dato ingresado no es un número')
            else:
                break
        return numero

    #Función que es llamada cuando se le pude al usuario un dato de texto
    #Hace ciclos hasta que el usuario digite un dato que no está compuesto enteramente por numeros, si es así retorna el dato
    #Esta función se hereda y es @static porque es una verificación que no necesita de parametros de instancia o clase
    @staticmethod
    def _pedirDatoTexto(text):
        while True:
            texto = input(text)
            if texto.isnumeric():
                print('El dato ingresado no puede contener números')
            else:
                break
        return texto

    #Función que es llamada cuando se le pude al usuario un dato de fecha
    #Hace ciclos hasta que el usuario digite una fecha con el formato indicado, si es así retorna la fecha
    #Esta función se hereda y es @static porque es una verificación que no necesita de parametros de instancia o clase
    @staticmethod
    def _pedirFecha(text):
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
    #Esta función se hereda y es @static porque es una verificación que no necesita de parametros de instancia o clase
    @staticmethod
    def _pedirEmail():
        while True:
            correo = input('Ingrese el correo electrónico: ')
            if correo.endswith('@unal.edu.co'):
                break
            else:
                print('Correo inválido, verifique que su correo termine en @unal.edu.co')
        return correo

    #Función que es llamada cuando se le pude al usuario una foto
    #Esta función se hereda y es @static porque es una verificación que no necesita de parametros de instancia o clase
    @staticmethod
    def _importarFoto(ubicacionArchivo): #permite leer un archivo en formato binario
        try:
            with open(ubicacionArchivo, "rb") as file:
                blobFoto = file.read()
                return blobFoto
        except:
            print("Dirección de la foto inválida, omitiendo paso")
            return("N/A")


#### CLASE MATERIAS
class ClaseMaterias(_MetodosSuper):
    ##Importante:
    #Estos son datos que se usan en el __init__ y _insertarTabla que heredamos de _MetodosSuper
    _tipoTabla = 'materias'
    _datosTabla = '''codigo integer PRIMARY KEY, 
                    nombre text, 
                    facultadDicta text, 
                    departamentoDicta text, 
                    creditos integer, 
                    idioma text'''
    
    #Esta función retorna la lista de los códigos de materias que estan almacenados en la tabla de materias
    #Será útil para verificar si algún códido de materia ya existe o no
    #Se usa property para acceder a esta mas facilmente como __listaCodigosDeMaterias en vez de __listaCodigosDeMaterias()
    @property
    def __listaCodigosDeMaterias(self):
        self._cursorObj.execute('SELECT codigo FROM materias')
        cods = self._cursorObj.fetchall()
        codsSet = {str(i[0]) for i in cods} #se crea un conjunto con todos los ids de los usarios registrados en la tabla de estudiantes
        return codsSet

    #Esta función se llama cuando se quiere pedir un códido de materia existente
    #Esta función muestra los códidos de materias existentes, hace ciclos que validan si el COD que digite el usuario existe, si es así sale del ciclo retorna el COD
    #Esta función usa consultarTablaMaterias(con) para mostrar los códidos de materias en la BD
    @classmethod
    def _pedirCodigoDeMateria(cls,DB,text):
        tempMaterias = cls(DB)
        idSet = tempMaterias.__listaCodigosDeMaterias
        while True:
            tempMaterias.consultarTablaMaterias()
            id = input(text)
            if id in idSet: #verifica que el id ingresado ya esté registrado en estudiantes
                break
            else:
                print('El código ingresado no se encuentra en la lista de materias, por favor ingrese otro código')
        return id
    
    #Esta función de usa para mostrar los Codigos y los Nombres de las materias almacendadas en la tabla de materias
    def consultarTablaMaterias(self):
        self._cursorObj.execute('SELECT codigo, nombre FROM materias')  # recopila el valor de las columnas "codigo" y "nombre" para cada fila
        filas = self._cursorObj.fetchall() # se guardan los codigos y los nombres de las materias una lista
        print('Códigos de materias y nombres de materias almacenados en la base de datos: ')
        for row in filas: # se itera la lista para imprimir el nombre y el código de cada materia
            codigo = row[0]
            nombre = row[1]
            print(f'id: {codigo:>15}       nombre: {nombre:>30}')

    #Pide al usuario información sobre las materias y la guarda en una tupla
    #Verifica los datos ingresados con pedirDatoTexto y pedirDatoNumerico
    #Para el código de las materias verifica si el código ingresado ya existe usando listaCodigosDeMaterias, así evita que hallan dos códigos iguales
    # Inserta la información de la tupla anterior en la base de datos usando el metodo heredado _insertarTabla
    def insertarMateria(self):
        while True:
            codigo = input('Codigo de la materia: ')
            if not codigo.isnumeric():
                print('El dato ingresado no es un número')
            elif codigo in self.__listaCodigosDeMaterias:
                print('Este número ya está registrado en la base de datos')
            else:
                break
        codigo = codigo.ljust(12)  # ajusta a la izquierda 12 posiciones
        nombre = self._pedirDatoTexto('Nombre de la materia: ')
        facultadDicta = self._pedirDatoTexto('Facultad que la dicta: ')
        departamentoDicta = self._pedirDatoTexto('Departamento que la dicta: ')
        creditos = self._pedirDatoNumerico('Cantidad de créditos: ')
        idioma = self._pedirDatoTexto('Idioma en que se dicta: ')
        materia = (
                codigo,
                nombre, 
                facultadDicta, 
                departamentoDicta, 
                creditos, 
                idioma
        )
        self._insertarTabla(materia)

    #Esta función muestra los datos de una materia en específico, dependiendo del código que entra como argumento
    def consultarInfoMateria(self):
        codigo = ClaseMaterias._pedirCodigoDeMateria(self._DB,"Código de materia a consultar: ")
        self._cursorObj.execute(f"SELECT * FROM materias WHERE codigo = {codigo}") #filtra la información de la materia especificada por su código
        infoMateria = self._cursorObj.fetchall() # guarda la información de la materia en una lista
        for row in infoMateria: #Se itera la lista para imprimir cada característica de la materia
            print("{:<15}{:>40}".format("Código: ", row[0]))
            print("{:<15}{:>40}".format("Nombre: ", row[2]))
            print("{:<15}{:>40}".format("Facultad: ", row[2]))
            print("{:<15}{:>40}".format("Departamento: ", row[3]))
            print("{:<15}{:>40}".format("Créditos: ", row[4]))
            print("{:<15}{:>40}".format("Idioma: ", row[5]))

    #Esta función se usa para actualizar el idioma de una materia
    def actualizarTablaMaterias(self):
        codMat = ClaseMaterias._pedirCodigoDeMateria(self._DB,'Codigo de la materia a actualizar: ')
        nuevoidioma = self._pedirDatoTexto('Actualice el idioma: ')
        self._cursorObj.execute(f'UPDATE materias SET idioma ="{nuevoidioma}" WHERE codigo ="{codMat}"')
        self._con.commit()  # guardamos tabla en el drive
    
    #Esta función pide al usuario la materia que quiere borrar y la elimina de la tabla de materias
    def borrarinfoTablaMaterias(self): 
        materiaBorrar = ClaseMaterias._pedirCodigoDeMateria(self._DB,"Codigo de la materia para borrar: ")
        self._cursorObj.execute(f'DELETE FROM materias WHERE codigo ="{materiaBorrar}"')
        self._con.commit()
    
    #Esta función calcula el promedio de los créditos de las materias
    def promedioTablaMaterias(self): 
        self._cursorObj.execute("SELECT count (*) FROM materias")  # cuenta el total de las materias inscritas
        cantidadMaterias = self._cursorObj.fetchall() # guarda el valor anterior en una lista
        for row in cantidadMaterias:
            cantidad = row[0]
        self._cursorObj.execute("SELECT sum(creditos) FROM materias")  # calcula la suma de los creditos de todas las materias inscritas
        sumatoriaCreditos = self._cursorObj.fetchall()
        for row in sumatoriaCreditos:
            sumatoria = row[0]
        promedio = sumatoria / cantidad
        print("El promedio de los creditos de las materias es: ", promedio)
    
class ClaseEstudiantes(_MetodosSuper):
    ##Importante:
    #Estos son datos que se usan en el __init__ y _insertarTabla que heredamos de _MetodosSuper
    _tipoTabla = 'estudiantes'
    _datosTabla = '''identificacion integer PRIMARY KEY, 
                    nombre text, 
                    apellido text, 
                    carrera text, 
                    fechaNacimiento text, 
                    fechaIngreso text,
                    ciudadProcedencia text, 
                    email text, 
                    cantidadMatriculas integer,
                    fotografia blob'''

    #Esta función retorna la lista de los números de identificación que estan almacenados en la tabla de estudiantes
    #Será útil para verificar si algún NI ya existe o no
    @property
    def __listaNumerosDeIdentificacion(self):
        self._cursorObj.execute('SELECT identificacion FROM estudiantes')
        ids = self._cursorObj.fetchall()
        idSet = {str(i[0]) for i in ids} #se crea un conjunto con todos los ids de los usarios registrados en la tabla de estudiantes
        return idSet

    #Esta función se llama cuando se quiere pedir un número de identificación existente
    #Esta función muestra los números de identificación existentes, hace ciclos que validan si el NI que digite el usuario existe, si es así sale del ciclo y retorna el NI
    #Esta función usa consultarTablaEstudiantes para mostrar los NI almacenados en la BD
    @classmethod
    def _pedirNumeroDeIdentificacion(cls,DB,text):
        tempEstudiante = cls(DB)
        idSet = tempEstudiante.__listaNumerosDeIdentificacion
        while True:
            tempEstudiante.consultarTablaEstudiantes()
            id = input(text)
            if id in idSet: #verifica que el id ingresado ya esté registrado en estudiantes
                break
            else:
                print('El número de identificación ingresado no aparece en la lista')
        return id

    #Esta función de usa para mostrar los NI y el nombres compeltos de los estudiantes almacendadas en la tabla de estudiantes
    def consultarTablaEstudiantes(self):
        self._cursorObj.execute("SELECT identificacion, nombre, apellido FROM estudiantes") #recopila el nombre y la identificación de todos los estudiantes en una lista
        filas = self._cursorObj.fetchall()
        print("La información de los estudiantes es: ")
        for row in filas: #itera la lista para imprimir la información de cada estudiante
            id = row[0]
            nombrecompleto = row[1]+' '+row[2]
            print(f'id: {id:>15}       nombre: {nombrecompleto:>30}')

    #Pide al usuario información sobre un estudiante y la guarda en una tupla
    #Verifica los datos ingresados con pedirDatoTexto, pedirDatoNumerico, pedirFecha y pedirEmail
    #Para el número de identificación del estudiante verifica si el NI ingresado ya existe usando listaNumerosDeIdentificacion, así evita que hallan dos NI iguales
    # Inserta la información de la tupla anterior en la base de datos usando el metodo heredado _insertarTabla
    def insertarEstudiante(self):
        while True:
            id = input("Numero de identificación: ")
            if not id.isnumeric():
                print('El dato ingresado no es un número')
            elif id in self.__listaNumerosDeIdentificacion:
                print('Este número ya está registrado en la base de datos')
            else:
                break
        nombre = self._pedirDatoTexto("Nombre del estudiante: ")
        apellido = self._pedirDatoTexto("Apellido del estudiante: ")
        carrera = self._pedirDatoTexto("Plan de estudios: ")
        fechaNacimiento = self._pedirFecha("nacimiento")
        fechaIngreso = self._pedirFecha("ingreso")
        ciudadProcedencia = self._pedirDatoTexto("Ciudad de procedencia: ")
        email = self._pedirEmail()
        cantidadMatriculas = self._pedirDatoNumerico("Cantidad de matrículas: ")
        foto = self._pedirDatoTexto("Ubicación completa de la fotografía (PATH): ")
        blobFoto = self._importarFoto(foto) #la imagen en formato binario se asigna a una variable
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
        self._insertarTabla(infoEstudiante)

    #Esta función recibe el NI de un estudiante y permite modificar un dato de un estudiante
    #Hace ciclos preguntandole al usuario que dato quiere modificar de una lista. Si el dato está en la lista se le pide el nuevo valor del dato sino está se le pregunta de nuevo
    #Se usan las funciones de verificación de datos dependiendo de que dato quiera modificar el usuario
    def actualizarTablaEstudiante(self):
        idEstudiante = ClaseEstudiantes._pedirNumeroDeIdentificacion(self._DB,"Número de identificación del estudiante a actualizar datos: ")
        # dado el id de un estudiante permite actualizar los datos de una columna especificada
        while True:
            columna=input('''
            Ingrese el atributo del estudiante que desea actualizar:
            nombre, apellido, carrera, fechaNacimiento, fechaIngreso, ciudadProcedencia, email, cantidadMatriculas, fotografia
            ''')
            if columna in ('identificacion','cantidadMatriculas'):
                nuevoValor = self._pedirDatoNumerico("Ingrese información actualizada: ")
                break
            elif columna in ('nombre','apellido','carrera','ciudadProcedencia','email','fotografia'):
                nuevoValor = self._pedirDatoTexto("Ingrese información actualizada: ")
                break
            elif columna in ('fechaNacimiento','fechaIngreso'):
                nuevoValor = self._pedirFecha(columna.replace('fecha','').lower())
                break
            else:
                print('Ingrese un atributo válido')
        self._cursorObj.execute(f'UPDATE estudiantes SET "{columna}" = "{nuevoValor}" WHERE identificacion = "{idEstudiante}"')
        self._con.commit()  # guardamos tabla en el drive

    #Esta función muestra los datos de un estudiante en específico, dependiendo del NI que entra como argumento
    def consultarInfoEstudiante(self):
        id = ClaseEstudiantes._pedirNumeroDeIdentificacion(self._DB,"Número de identificación del estudante a consultar datos: ")
        self._cursorObj.execute(f"SELECT * FROM estudiantes WHERE identificacion = {id}") #dado el id de un estudiante, recopila todos sus datos en una lista
        infoMateria = self._cursorObj.fetchall()
        for row in infoMateria: #itera la lista para imprimir dato por dato
            print("{:<24}{:>30}".format("Id: ", row[0]))
            print("{:<24}{:>30}".format("Nombre: ", row[1]+" "+row[2]))
            print("{:<24}{:>30}".format("Carrera: ", row[3]))
            print("{:<24}{:>30}".format("Fecha de nacimiento: ", row[4]))
            print("{:<24}{:>30}".format("Fecha de ingreso: ", row[5]))
            print("{:<24}{:>30}".format("Ciudad de procedencia: ", row[6]))
            print("{:<24}{:>30}".format("Email: ", row[7]))
            print("{:<24}{:>30}".format("Cantidad de matrículas: ", row[8]))

class ClaseHistoriaAcademica(_MetodosSuper):
    ##Importante:
    #Estos son datos que se usan en el __init__ y _insertarTabla que heredamos de _MetodosSuper
    _tipoTabla = 'historia'
    _datosTabla = '''identificacion integer , 
                    codigo integer, 
                    notaFinal real, 
                    creditos integer, 
                    PRIMARY KEY(identificacion, codigo)'''

    ##Funcion privada que sirve para comprobar si una historia academica existe o no
    def __historiaExiste(self,id,mat):
        self._cursorObj.execute(f'SELECT * from historia where identificacion = "{id}" AND codigo = "{mat}"')
        if len(self._cursorObj.fetchall()) != 0:
            return True
        else:
            return False

    def insertarHistoria(self): #pide al usuario datos de las materias cursadas
        id = ClaseEstudiantes._pedirNumeroDeIdentificacion(self._DB,"Numero de identidicación del estudiante de la historia académica: ")  # pide al usuario su número de identificación
        codigo = ClaseMaterias._pedirCodigoDeMateria(self._DB, "Código de la materia de la historia académica: ")
        if self.__historiaExiste(id,codigo):
            print('No puede crear esa historia académica debido a que ya existe')
            return
        notaFinal = self._pedirDatoNumerico("Nota final: ")
        self._cursorObj.execute(f"SELECT creditos FROM materias WHERE codigo = {codigo}")
        creditos = str(self._cursorObj.fetchall()[0][0])
        infoHistoria = (  # guardo los datos de la materia y el usuario en una tupla
            id,
            codigo,
            notaFinal,
            creditos,
        )
        self._insertarTabla(infoHistoria)

    #Funcioón para consultar las historias academicas de un estudiante
    #Esta función recibe un código de estudiante y muestra las historias académicas de ese estudiante (codigo de materia, nota y creditos)
    def consultarHistoriaAcademica(self):
        identificacion = ClaseEstudiantes._pedirNumeroDeIdentificacion(self._DB,"Número de identificación del estudiante a consultar la historia académica: ")
        self._cursorObj.execute(f"SELECT codigo, notaFinal, creditos FROM historia WHERE identificacion = {identificacion}") # recopila la nota, los creditos y el codigo de todas las materias que el usuario ha visto en una lista 
        filas = self._cursorObj.fetchall()
        for row in filas: #itera la lista e imprime la información básica de las materias cursadas
            codigo = row[0]
            notaFinal = row[1]
            creditos = row[2]
            print("{:<28}{:>30}".format("Codigo de la materia: ", codigo))
            self._cursorObj.execute(f"SELECT nombre FROM materias WHERE codigo = {codigo}")
            print("{:<28}{:>30}".format("El nombre de la materia es: ",self._cursorObj.fetchall()[0][0]))
            print("{:<28}{:>30}".format("La nota final es: ", notaFinal))
            print("{:<28}{:>30}\n".format("Número de créditos: ", creditos))

    #Función para borrar una historia académica
    #Esta función toma un NI de estudiante, un código de matera existentes y borra esa historia académica de la base de datos
    def borrarinfoTablaHistoria(self):
        identificacion = ClaseEstudiantes._pedirNumeroDeIdentificacion(self._DB, "Número de identificación del estudiante que se borrará la historia académica: ")
        materiaBorrar = ClaseMaterias._pedirCodigoDeMateria(self._DB,"Codigo de la materia para borrar: ")
        if not self.__historiaExiste(identificacion,materiaBorrar):
            print('No puede borrar ya que no hay una historia académica con ese NI de estudiante y Código de materia')
            return
        self._cursorObj.execute(f"DELETE FROM historia WHERE identificacion = {identificacion} AND codigo = {materiaBorrar}") # dados un numero de id y un codigo de materia, se elimina la materia de la historia académica
        self._con.commit()

    #Esta función toma un NI de estudiante existente, pregunta por un código de materia existente y permite acuatualizar la nota de dicha historia académica
    def actualizarNota(self): #dados un numero de id y un código de materia, se pide la nota correcta para ser corregida en la tabla
        identificacion = ClaseEstudiantes._pedirNumeroDeIdentificacion(self._DB, "Número de identificación del estudiante para actualizar la nota: ")
        codigoMateria = ClaseMaterias._pedirCodigoDeMateria(self._DB,"Qué materia desea actualizar? ")
        if not self.__historiaExiste(identificacion,codigoMateria):
            print('No puede actualizar la nota ya que no hay una historia académica con ese NI de estudiante y Código de materia')
            return
        nuevaNota = self._pedirDatoNumerico("Actualice la nota: ")
        self._cursorObj.execute(f"UPDATE historia SET notaFinal = {nuevaNota} WHERE identificacion = {identificacion} AND codigo = {codigoMateria}") #se actualiza la nota en la tabla
        self._con.commit()  # guardamos tabla en el drive

class ClaseClasificacion(_MetodosSuper):
    ##Importante:
    #Estos son datos que se usan en el __init__ y _insertarTabla que heredamos de _MetodosSuper
    _tipoTabla = 'clasificacion'
    _datosTabla = '''identificacion integer PRIMARY KEY, 
                    nombre text, 
                    apellido text, 
                    cantidadMateriasTomadas integer, 
                    creditosAcumulados integer,
                    promedio real'''
    
    # cuando queremos añadir las materias junto con sus notas y créditos para cada estudiante, toca hacerlo en la tabla de historia académica. También sabemos que 
    # # hay una tabla de estudiantes donde se guardan sus datos personales. Es decir, que el id como PRIMARY KEY está en la tabla de historia académica y en la tabla
    # estudiantes, por tanto, para evitar que se creen historias académicas de estudiantes que no están registrados
    # en la tabla de estudiantes, es necesaria la siguiente función.
    def __actualizarTablaClasificacion(self):
        self._cursorObj.execute("DELETE FROM clasificacion") #todos los valores de la tabla de clasificación se calculan con los valores de las tablas 'estudiante' e 'historia'
        #entonces cada vez que se quiere actualizar la clasificación es más fácil borrar todos los valores de esta tabla e insertar de nuevo todos los valores 
        #que se obtienen a partir de 'estudiante' e 'historia'
        self._cursorObj.execute("""SELECT identificacion FROM historia""") #recolecta los ids de los usuarios que tienen historia académica

        ids = self._cursorObj.fetchall()
        # como los ids se repiten en la tabla de historia académica, se crea un conjunto para que aparezcan solo una vez
        idSet = {i[0] for i in ids}

        for i in idSet: # se itera el conjunto de los usuarios que tienen historia académica
            #se hacen los cálculos respectivos a partir de la historia académica para obtener promedios, creditos totales, etc. y se extrae el nombre y el apellido
            #para cada estudiante a partir de la tabla 'estudiante'

            sumaCreditos = self._cursorObj.execute(
                f"""SELECT  SUM(creditos) FROM historia WHERE identificacion = {i}"""
            )
            sumaCreditos = sumaCreditos.fetchall()

            promedio = self._cursorObj.execute(
                f"""SELECT  AVG(notaFinal) FROM historia WHERE identificacion = {i}"""
            )
            promedio = promedio.fetchall()

            cantidadMaterias = self._cursorObj.execute(
                f"""SELECT  COUNT(identificacion) FROM historia WHERE identificacion = {i}"""
            )
            cantidadMaterias = cantidadMaterias.fetchall()

            nombre = self._cursorObj.execute(
                f"""SELECT  nombre FROM estudiantes WHERE identificacion = {i}"""
            )
            nombre = nombre.fetchall()

            apellido = self._cursorObj.execute(
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
            self._cursorObj.execute("INSERT INTO clasificacion VALUES (?,?,?,?,?,?)", row) # se agrega la tupla a la tabla
        self._con.commit()

    #Muestra los datos de la tabla de clasificación
    #Inicialente llama a actualizarTablaClasificacion en dado caso de que halla ocurrido algún cambio en el código
    #Saca los datos de cada estudiante y los muestra en orden de promedio
    def consultaClasificacion(self):
        self.__actualizarTablaClasificacion()
        cursorObj = self._con.cursor()
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
    def consultaPosicionSegunId(self):
        id = ClaseMaterias._pedirCodigoDeMateria(self._DB,"Número de identificación del estudiante a consultar su clasificación: ")
        self.__actualizarTablaClasificacion()
        self._cursorObj.execute(
            f"SELECT * FROM clasificacion ORDER BY promedio DESC"
        )
        clasificacion = self._cursorObj.fetchall()
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

    def creaTupletPosiciones(self):
        self.__actualizarTablaClasificacion()
        # cursorObj = self._con.cursor()
        self._cursorObj.execute(
            f"SELECT * FROM clasificacion ORDER BY promedio DESC"
        )
        clasificacion = self._cursorObj.fetchall()
        data = []
        posicion = 0
        for i in clasificacion:
            posicion += 1
            if id == str(i[0]):
                data.append((i[0], i[1], i[2], i[3], i[4], i[5]))
                break
        return clasificacion


def menu(materias,estudiantes,historiasAcademicas,clasificaciones):
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
                2. Consultar Tabla Materias
                3. Consultar Materia
                4. Actualizar Materia
                5. Borrar Materia
                6. Calcular promedio de los créditos
                7. Salir
                Seleccione opción>>>: """
                )
                if opcionMaterias == "1":
                    materias.insertarMateria()
                elif opcionMaterias == "2":
                    materias.consultarTablaMaterias()
                elif opcionMaterias == "3":
                    materias.consultarInfoMateria()
                elif opcionMaterias == "4":
                    materias.actualizarTablaMaterias()
                elif opcionMaterias == "5":
                    materias.borrarinfoTablaMaterias()
                elif opcionMaterias == "6":
                    materias.promedioTablaMaterias()
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
                    estudiantes.insertarEstudiante()
                elif opcionEstudiantes == "2":
                    estudiantes.actualizarTablaEstudiante()
                elif opcionEstudiantes == "3":
                    estudiantes.consultarTablaEstudiantes()
                elif opcionEstudiantes == "4":
                    estudiantes.consultarInfoEstudiante()
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
                    historiasAcademicas.insertarHistoria()
                elif opcionHistoriaAcademica == "2":
                    historiasAcademicas.consultarHistoriaAcademica()
                elif opcionHistoriaAcademica == "3":
                    historiasAcademicas.borrarinfoTablaHistoria()
                elif opcionHistoriaAcademica == "4":
                    historiasAcademicas.actualizarNota()
                elif opcionHistoriaAcademica == "5":
                    salirHistoriaAcademica = True

        elif opcPrincipal == "4":
            salirClasificacion = False
            while not salirClasificacion:
                opcionClasificacion = input(
                    """
                Menu de Clasificación
                1. Consulta tabla de clasificación
                2. Consulta clasificación del estudiante
                3. Consulta clasificación del estudiante (GUI)
                4. Salir
                Seleccione opción>>>: """
                )
                if opcionClasificacion == "1":
                    clasificaciones.consultaClasificacion()
                elif opcionClasificacion == "2":
                    clasificaciones.consultaPosicionSegunId()
                elif opcionClasificacion == "3":
                    data = clasificaciones.creaTupletPosiciones()
                    print(data)
                    guiMiniSia.main(data)
                elif opcionClasificacion == "4":
                    salirClasificacion = True

        elif opcPrincipal == "5":
            salirPrincipal = True
    print(
        """
        Programa Finalizado. Gracias por utilizar nuestros servicios
    """
    )


def main():
    #Se crea la base de datos
    baseDeDatos = DataBase()
    #Se crea la tabla materias en la base de datos, inicializando materias como objeto de ClaseMaterias
    #Ahora materias es un objeto cuyos métodos modifican unicamente a la base de datos baseDeDatos
    materias = ClaseMaterias(baseDeDatos)
    #Se hace lo mismo con los otros objetos
    estudiantes = ClaseEstudiantes(baseDeDatos)
    historiasAcademicas = ClaseHistoriaAcademica(baseDeDatos)
    clasificaiones = ClaseClasificacion(baseDeDatos)
    menu(materias,estudiantes,historiasAcademicas,clasificaiones)
    baseDeDatos.cerrarBD()

if __name__ == '__main__':
    main()
