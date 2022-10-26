def menu(con):
    salirPrincipal = False
    while not salirPrincipal:
        opcPrincipal = input('''
        Menu de opciones

        1. Materias
        2. Estudiante
        3. Historia Académica
        4. Clasificación
        5. Salir

        Seleccione opción>>>: ''')
        if (opcPrincipal=='1'):
            salirMaterias = False
            while not salirMaterias:
                opcionMaterias = input('''
                Menu de Materias

                1. Insertar Materia leyendo información
                2. Insertar Materia sin leer infromación
                3. Consultar Materia
                4. Actualizar Materia
                5. Borrar Materia
                6. Calcular promedio de los créditos
                7. Salir

                Seleccione opción>>>: ''')
                if (opcionMaterias == '1'):
                    miMateria = leerInfoMaterias()
                    insertarTablaMaterias(con, miMateria)
                elif (opcionMaterias == '2'):
                    insertarTablaMaterias2(con)
                elif (opcionMaterias == '3'):
                    consultarTablaMaterias(con)
                elif (opcionMaterias == '4'):
                    codmatact = input('Codigo de la materia a actualizar: ')
                    actualizarTablaMaterias(con, codmatact)
                elif (opcionMaterias == '5'):
                    borrarInfoTablaMaterias(con)
                elif (opcionMaterias == '6'):
                    promedioTablaMaterias(con)
                elif (opcionMaterias == '7'):
                    salirMaterias = True
        
        elif (opcPrincipal=='2'):
            salirEstudiantes = False
            while not salirEstudiantes:
                opcionEstudiantes = input('''
                Menu de Estudiantes

                1. Crear Estudiante
                2. Actualizar Estudiante
                3. Consultar tabla de estudiantes
                4. Consultar Estudiante
                5. Salir

                Seleccione opción>>>: ''')
                if (opcionEstudiantes == '1'):
                    estudiante = leerInfoEstudiantes
                    insertarTablaEstudiantes(con, estudiante)
                elif (opcionEstudiantes == '2'):
                    id = input('Ingrese el número de identificación del estudiante que quiere actualizar: ')
                    dato = input('Ingrese el atributo del estudiante que desea actualizar: ')
                    actualizarTablaEstudiante(con, id, dato)
                elif (opcionEstudiantes == '3'):
                    consultarTablaEstudiantes(con)
                elif (opcionEstudiantes == '4'):
                    id = input('Ingrese el número de identificación del estudiante que quiere consultar: ')
                    consultarInfoEstudiante(con, id)
                elif (opcionEstudiantes == '5'):
                    salirEstudiantes = True
        
        elif (opcPrincipal=='3'):
            salirHistoriaAcademica = False
            while not salirHistoriaAcademica:
                opcionHistoriaAcademica = input('''
                Menu de Historia Academica

                1. Crear nueva historia academica
                2. Consultar historia académica de estudiante
                3. Borrar materia de la historia académica de un estudiante
                4. Actualizar nota de materia de un estudiante
                5. Salir

                Seleccione opción>>>: ''')
                if (opcionHistoriaAcademica == '1'):
                    codigo = input('Ingrese el  código de la materia de la historia académica: ')
                    identificacion = ('Ingrese la identificación del estudiante de la historia académica: ')
                    crearNuevaHistoriaAcademica(con,codigo,identificacion)
                elif (opcionHistoriaAcademica == '2'):
                    identificacion = ('Ingrese la identificación del estudiante de la historia académica que desea consultar: ')
                    consultarInformacion(identificacion)
                elif (opcionHistoriaAcademica == '3'):
                    identificacion = ('Ingrese la identificación del estudiante al que le quiere borrar una materia de la historia académica: ')
                    codigo = ('Ingrese el código de la materia que desea eliminar de la historia académica: ')
                    borrarMaterias(con, identificacion, codigo)
                elif (opcionHistoriaAcademica == '4'):
                    identificacion = ('Ingrese la identificación del estudiante al que le quiere actualizar la nota: ')
                    codigo = ('Ingrese el código de la materia al que le quiere acualizar la nota: ')
                    actualizarNota(con, codigo, identificacion)
                elif (opcionHistoriaAcademica == '5'):
                    salirHistoriaAcademica = True
        
        elif (opcPrincipal=='4'):
            salirClasificacion = False
            while not salirClasificacion:
                opcionClasificacion = input('''
                Menu de Clasificación

                1. Consulta clasificación
                2. Salir

                Seleccione opción>>>: ''')
                if (opcionClasificacion == '1'):
                    consultaClasificacion()
                elif (opcionClasificacion == '2'):
                    salirClasificacion = True
        
        elif (opcPrincipal=='5'):
            salirPrincipal=True
    print('''
        Programa Finalizado. Gracias por utilizar nuestros servicios
    ''')