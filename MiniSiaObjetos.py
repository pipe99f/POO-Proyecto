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

def cerrarBD(con):
    con.close()

class baseDeDatos:
    def __init__(self, con):
        self.con = con

###VALIDACIONES DE DATOS

#Esta función retorna la lista de los números de identificación que estan almacenados en la tabla de estudiantes
#Será útil para verificar si algún NI ya existe o no
    def listaNumerosDeIdentificacion(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("""SELECT identificacion FROM estudiantes""")
        ids = cursorObj.fetchall()
        idSet = {str(i[0]) for i in ids} #se crea un conjunto con todos los ids de los usarios registrados en la tabla de estudiantes
        return idSet

#Esta función se llama cuando se quiere pedir un número de identificación existente
#Esta función muestra los números de identificación existentes, hace ciclos que validan si el NI que digite el usuario existe, si es así sale del ciclo y retorna el NI
#Esta función usa consultarTablaEstudiantes(con) para mostrar los NI almacenados en la BD

#Esta función de usa para mostrar los NI y el nombres compeltos de los estudiantes almacendadas en la tabla de estudiantes
    def consultarTablaEstudiantes(self):
        cursorObj = self.con.cursor()
        cursorObj.execute(
            "SELECT identificacion, nombre, apellido FROM estudiantes" #recopila el nombre y la identificación de todos los estudiantes en una lista
        )  
        filas = cursorObj.fetchall()
        print("La información de los estudiantes es: ")
        for row in filas: #itera la lista para imprimir la información de cada estudiante
            id = row[0]
            nombrecompleto = row[1]+' '+row[2]
            print(f'id: {id:>15}       nombre: {nombrecompleto:>30}')

    def pedirNumeroDeIdentificacion(self, text):
        idSet = self.listaNumerosDeIdentificacion()
        while True:
            self.consultarTablaEstudiantes()
            id = input(text)
            if id in idSet: #verifica que el id ingresado ya esté registrado en estudiantes
                break
            else:
                print('El número de identificación ingresado no aparece en la lista')
        return id

#Esta función retorna la lista de los códigos de materias que estan almacenados en la tabla de materias
#Será útil para verificar si algún códido de materia ya existe o no
    def listaCodigosDeMaterias(self):
        cursorObj = self.con.cursor()
        cursorObj.execute("""SELECT codigo FROM materias""")
        cods = cursorObj.fetchall()
        codsSet = {str(i[0]) for i in cods} #se crea un conjunto con todos los ids de los usarios registrados en la tabla de estudiantes
        return codsSet

#Esta función de usa para mostrar los Codigos y los Nombres de las materias almacendadas en la tabla de materias
    def consultarTablaMaterias(self):
        cursorObj = self.con.cursor()
        cursorObj.execute(
            "SELECT codigo, nombre FROM materias"
        )  # recopila el valor de las columnas "codigo" y "nombre" para cada fila
        filas = cursorObj.fetchall() # se guardan los codigos y los nombres de las materias una lista
        print("Códigos de materias y nombres de materias almacenados en la base de datos: ")
        for row in filas: # se itera la lista para imprimir el nombre y el código de cada materia
            codigo = row[0]
            nombre = row[1]
            print(f'id: {codigo:>15}       nombre: {nombre:>30}')
#Esta función se llama cuando se quiere pedir un códido de materia existente
#Esta función muestra los códidos de materias existentes, hace ciclos que validan si el COD que digite el usuario existe, si es así sale del ciclo retorna el COD
#Esta función usa consultarTablaMaterias(con) para mostrar los códidos de materias en la BD
    def pedirCodigoDeMateria(self, text):
        idSet = self.listaCodigosDeMaterias()
        while True:
            self.consultarTablaMaterias()
            id = input(text)
            if id in idSet: #verifica que el id ingresado ya esté registrado en estudiantes
                break
            else:
                print("El código ingresado no se encuentra en la lista de materias, por favor ingrese otro código")
        return id

#Función que es llamada cuando se le pude al usuario un dato numérico
#Hace ciclos hasta que el usuario digite un dato compuesto enteramente por numeros, si es así retorna el dato
    def pedirDatoNumerico(self, text):
        while True:
            numero = input(text)
            if not numero.isnumeric():
                print('El dato ingresado no es un número')
            else:
                break
        return numero

#Función que es llamada cuando se le pude al usuario un dato de texto
#Hace ciclos hasta que el usuario digite un dato que no está compuesto enteramente por numeros, si es así retorna el dato
    def pedirDatoTexto(self, text):
        while True:
            texto = input(text)
            if texto.isnumeric():
                print('El dato ingresado no puede contener números')
            else:
                break
        return texto

#Función que es llamada cuando se le pude al usuario un dato de fecha
#Hace ciclos hasta que el usuario digite una fecha con el formato indicado, si es así retorna la fecha
    def pedirFecha(self, text):
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
    def pedirEmail(self):
        unal = True
        while True:
            correo = input("Ingrese el correo electrónico: ")
            if correo.endswith("@unal.edu.co"):
                break
            else:
                print("Correo inválido, verifique que su correo termine en @unal.edu.co")
        return correo

class Materias(baseDeDatos):
    def __init__(self, con):
        super().__init__(con) #se usa para que esta clase tambien tenga el atributo "self.con"

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
    menu(miCon)
    cerrarBD(miCon)

main()

