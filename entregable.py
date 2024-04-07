from enum import Enum
from abc import ABCMeta, abstractmethod

# enumeraciones
class Departamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

class Sexo(Enum):
    HOMBRE = 1
    MUJER = 2

# excepciones personalizadas
class DniNotFound(Exception):
    pass
# MiembroDepartamento
class MiembroExists(Exception):
    pass

class MiembroNotExists(Exception):
    pass

class NotInvestigador(Exception):
    pass

class NotProfesor(Exception):
    pass

class Persona(metaclass=ABCMeta):
    def __init__(self, nombre, dni, direccion, sexo :  Sexo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        self.sexo = sexo

    @abstractmethod
    def devuelve_datos(self):
        pass

class Profesor(Persona, metaclass = ABCMeta):
    def __init__(self, nombre, dni, direccion, sexo :  Sexo, departamento : Departamento, asignaturas):
        super().__init__(nombre, dni, direccion, sexo) 
        self.departamento = departamento
        self.asignaturas = asignaturas

    @abstractmethod
    def devuelve_datos(self):
        pass

    @abstractmethod
    def _añadir_asignatura(self, asignatura):
        pass

    @abstractmethod   
    def _eliminar_asignatura(self, asignatura):
        pass

    @abstractmethod
    def devuelve_asignaturas(self):
        pass


class MiembroDepartamento(): 
    def __init__(self, miembros = {}): #diccionario que contiene como clave el departamento, y como valor, una lista de personas
        self.miembros = miembros
                                            #cada profesor/investigador está asociado a un único departamento

    def _añadir_miembro(self, persona):        #solo la universidad tiene acceso a estos métodos
        try:
            for m in self.miembros[persona.departamento.value]:
                if persona.dni == m.dni:
                    raise MiembroExists(f"{persona.nombre} ya es miembro del departamento {persona.departamento.name}")
                    
            self.miembros[persona.departamento.value].append(persona)
            return f"{persona.nombre} ha sido añadido como miembro del departamento {persona.departamento.name}"
            
        except Exception as e:
            # cualquier excepción
            print(f"No se pudo añadir a {persona.nombre} como miembro de departamento: {e}")

    def _eliminar_miembro(self, persona):

        try:
            lista = self.miembros[persona.departamento.value]
            for p in lista:  # Iterar sobre una copia para evitar modificar la lista mientras iteras
                if p.dni == persona.dni:
                    lista.remove(p)
                    self.miembros[persona.departamento.value] = lista
                    print(f"{persona.nombre} ha sido eliminado del departamento {persona.departamento.value}")
                    return
                raise MiembroNotExists(f"{persona.nombre} no es miembro del departamento {persona.departamento.name}")
        except Exception as e:
            print(f"Ocurrió un error al intentar eliminar a {persona.nombre}: {e}")
             
    def _cambiar_miembro(self, persona, nuevo_departamento : Departamento):
            
        try:
            departamento_actual = persona.departamento
            if departamento_actual is not None:
                if departamento_actual.value != nuevo_departamento.value:
                    # Intentar remover a la persona del departamento actual y añadirla al nuevo.
                    removido = False
                    for p in self.miembros[departamento_actual.value]:
                        if p.dni == persona.dni:
                            self.miembros[departamento_actual.value].remove(p)
                            removido = True
                            break  # Salir del bucle una vez encontrado y removido.
                    if removido:
                        persona.departamento = nuevo_departamento
                        self._añadir_miembro(persona)
                        print(f"{persona.nombre} ha sido trasladado del departamento {departamento_actual.name} al departamento {nuevo_departamento.name}")
                    else:
                        print(f"No se pudo encontrar a {persona.nombre} en el departamento {departamento_actual.name} para removerlo.")
                else:
                    print(f"{persona.nombre} ya pertenece al departamento {nuevo_departamento.name}")
            else:
                print(f"{persona.nombre} no es miembro de ningún departamento") # puede suceder para estudiantes por ejemplo
        except AttributeError as e:
            print(f"Error de atributo: {e}")
        except KeyError as e:
            print(f"Error de clave: {e}. Verifica que los departamentos existan.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

class Estudiante(Persona): #Todo estudiante está matriculado de alguna asignatura, por lo que es obligatorio pasar un listado de asignaturas matriculadas
    def __init__(self, nombre, dni, direccion, sexo : Sexo, asignaturas_matriculadas :  list):

        Persona.__init__(self, nombre, dni, direccion, sexo)
        self.asignaturas_matriculadas = asignaturas_matriculadas

    def devuelve_datos(self):
        return f"Estudiante \tNombre:{self.nombre} \tDNI:{self.dni} \tDireccion:{self.direccion} \tSexo:{self.sexo.name} "

    def _matricular_asignatura(self, asignatura):
        self.asignaturas_matriculadas.append(asignatura)
 
    def _desmatricular_asignatura(self, asignatura):
        self.asignaturas_matriculadas.remove(asignatura)
 
    def devuelve_asignaturas(self):
            nombres_asignaturas = ', '.join([asignatura.nombre for asignatura in self.asignaturas_matriculadas])
            return f'\nEl estudiante {self.nombre} está matriculado de las siguientes asignaturas:{nombres_asignaturas}'
            

class Investigador(Persona):

    def __init__(self, nombre, dni, direccion, sexo : Sexo, departamento : Departamento, area_investigacion):
        try:
            # comprobamos estos tres métodos ya que el dni es muy significativo y los otros dos pertenecen a una clase (enumeración)
            if not isinstance(dni, str):
                raise TypeError('dni debe ser una cadena de texto')
            if not isinstance(sexo, Sexo):
                raise TypeError(f'sexo debe ser una instancia de la clase Sexo; {sexo} es inválido')
            if not isinstance(departamento, Departamento):
                raise TypeError(f'departamento debe ser una instancia de la clase Departamento; {departamento} es inválido')
                
            super().__init__(nombre, dni, direccion, sexo)
            self.area_investigacion = area_investigacion
            self.departamento = departamento
        except TypeError as t:
            print(f"Tipo de dato incorrecto: Asegure que {t}")

    def devuelve_datos(self):
        return f"Investigador \tNombre:{self.nombre} \tDNI:{self.dni} \tDireccion:{self.direccion} \tSexo:{self.sexo.name} \tÁreas de Investigacion:{', '.join([area for area in self.area_investigacion])} \tDepartamento:{self.departamento.name}"

          
class ProfesorAsociado(Profesor):
    def __init__(self, nombre, dni, direccion, sexo, departamento : Departamento, asignaturas : list):
        try:
            if not isinstance(dni, str):
                raise TypeError('dni debe ser una cadena de texto')
            if not isinstance(sexo, Sexo):
                raise TypeError(f'sexo debe ser una instancia de la clase Sexo; {sexo} es inválido')
            if not isinstance(departamento, Departamento):
                raise TypeError(f'departamento debe ser una instancia de la clase Departamento; {departamento} es inválido')
            super().__init__(nombre, dni, direccion, sexo, departamento, asignaturas) #ojo sin super no funciona
        except TypeError as t:
            print(f"Tipo de dato incorrecto: Asegúrese de que {t}")


    def _añadir_asignatura(self, asignatura):
        self.asignaturas.append(asignatura)
        
    def _eliminar_asignatura(self, asignatura):
        if asignatura in self.asignaturas:
            self.asignaturas.remove(asignatura) 

    def devuelve_datos(self):
        return f"Profesor Asociado \tNombre:{self.nombre} \tDNI:{self.dni} \tDireccion:{self.direccion} \tSexo:{self.sexo.name} \tDepartamento:{self.departamento.name} \tAsignaturas:{', '.join([asignatura.nombre for asignatura in self.asignaturas])}"

    def devuelve_asignaturas(self):
        print(f"El profesor imparte las siguientes asignaturas {self.asignaturas}")
        for i in self.asignaturas:
            print(i.devuelve_datos())


class ProfesorTitular(Profesor): 
    def __init__(self, nombre, dni, direccion, sexo, departamento : Departamento, asignaturas : list, area_investigacion):
        try:
            if not isinstance(dni, str):
                raise TypeError('dni debe ser una cadena de texto')
            if not isinstance(sexo, Sexo):
                raise TypeError(f'sexo debe ser una instancia de la clase Sexo; {sexo} es inválido')
            if not isinstance(departamento, Departamento):
                raise TypeError(f'departamento debe ser una instancia de la clase Departamento; {departamento} es inválido')

            super().__init__(nombre, dni, direccion, sexo, departamento, asignaturas)
            self.area_investigacion = area_investigacion


        except TypeError as t:
            print(f"Tipo de dato incorrecto: Asegúrese de que {t}")

       
    def _añadir_asignatura(self, asignatura):
        self.asignaturas.append(asignatura)

    def _eliminar_asignatura(self, asignatura):
        if asignatura in self.asignaturas:
            self.asignaturas.remove(asignatura)
    
    def devuelve_asignaturas(self):
        print(f"El profesor imparte las siguientes asignaturas")
        for i in self.asignaturas:
            print(i.devuelve_datos())

    def devuelve_datos(self):
        return f"Profesor Titular \tNombre:{self.nombre} \tDNI:{self.dni} \tDireccion:{self.direccion} \tSexo:{self.sexo.name} \tÁreas de Investigacion:{', '.join([area for area in self.area_investigacion])} \tDepartamento:{self.departamento.name} \tAsignaturas:{', '.join([asignatura.nombre for asignatura in self.asignaturas])}"

class Asignatura:
    def __init__(self, id,nombre, creditos, modalidad : Departamento):
        self.id = id
        self.nombre = nombre
        self.creditos = creditos
        self.modalidad = modalidad
        self.docentes = []

    def devuelve_datos(self):#
        return f"ID: {self.id}, Nombre: {self.nombre}, Créditos: {self.creditos}, Modalidad: {self.modalidad.value}"
    
    def _añadir_docente(self, profesor):
        # Añade el profesor a la lista de docentes solo si aún no está en la lista
        if profesor not in self.docentes:
            self.docentes.append(profesor)
            print(f'{profesor.nombre} ha sido añadido como docente de {self.nombre}')
        else:
            print(f'{profesor.nombre} ya es docente de {self.nombre}')

    def _eliminar_docente(self, profesor):
        # Intenta eliminar el profesor de la lista de docentes
        try:
            self.docentes.remove(profesor)
            print(f'El profesor {profesor.nombre} ha sido eliminado de la asignatura {self.nombre}')
        except ValueError:
            print(f'El profesor {profesor.nombre} no imparte la asignatura {self.nombre}')

    def _eliminar_docente(self, profesor):
        if profesor in self.docentes: # no me detecta profesor que si estan
            self.docentes.remove(profesor)
            print(f'{profesor.nombre} ha sido eliminado como docente de {self.nombre}')
        else:
            raise ValueError(f'El profesor {profesor.nombre} no imparte {self.nombre}')

class Universidad:
    def __init__(self, nombre, id, asignaturas, departamentos, areas_investigacion):
        self.nombre = nombre
        self.id = int(id)
        self.asignaturas = list(asignaturas)
        self.estudiantes = []
        self.profesores = {"asociados" : [], "titulares" : []} #diccionario de profesores con asociados y titulares
        self.investigadores = []
        self.areas_investigacion = areas_investigacion
        self.departamentos = departamentos
        self.miembros_departamento = MiembroDepartamento()
        for dep in self.departamentos:
            self.miembros_departamento.miembros[dep.value] = []

    def get_miembros_departamento(self, dep = None):
            try:
                if dep is not None and not isinstance(dep, Departamento):
                    raise TypeError("El departamento debe pertenecer a la clase Departamento")
                elif dep is not None:
                    print(f"\n\n------Departamento : {dep.name}------")
                    for e in self.miembros_departamento.miembros[dep.value]:
                        print(e.devuelve_datos())
                else:
                    for dep in self.departamentos:
                        print(f"\n\n------Departamento : {dep.name}------")
                        for e in self.miembros_departamento.miembros[dep.value]:
                            print(e.devuelve_datos())
            except Exception as e:
                print(f'Ocurrio un error inesperado:{e}')



    def matricular_estudiante(self, estudiante):
        try:
            # Verificar si el estudiante ya está matriculado
            for e in self.estudiantes:
                if e.dni == estudiante.dni:
                    raise ValueError(f'El alumno con dni {estudiante.dni} ya está matriculado')
            
            self.estudiantes.append(estudiante)
            print(f'{estudiante.nombre} ha sido matriculado correctamente')

        except Exception as e:
            # Capturar y manejar cualquier otra excepción inesperada
            print(f"Error inesperado al matricular a {estudiante.nombre}: {e}")


    def eliminar_estudiante(self, dni):
        try:
            if not isinstance(dni, str):
                raise TypeError('El tipo de dato introducido para el DNI no es correcto. Debe ser una cadena de texto')
            for p in self.estudiantes:
                if p.dni == dni:
                    self.estudiantes.remove(p)
                    print(f"{p.nombre} ha sido eliminado como estudiante correctamente.")
                    return
            raise DniNotFound(f'El dni {dni} no se encuentra en la base de datos')
        except Exception as e:
            print(f"Error inesperado: {e}")

    def contratar_profesor(self, profesor):#
        try:
            for p in self.profesores['titulares']:
                if p.dni == profesor.dni:
                        raise ValueError(f'{p.nombre} ya está contratado como profesor titular')
            for p in self.profesores['asociados']:
                if p.dni == profesor.dni:
                    raise ValueError(f'{p.nombre} ya está contratado como profesor asociado')

            for i in self.investigadores:
                if i.dni == profesor.dni:
                    raise NotProfesor('Un investigador no puede ser profesor asociado')
                
            if isinstance(profesor, ProfesorAsociado):
                # Verifica si el DNI ya pertenece a un profesor titular
                for p in self.profesores['asociados']:
                    if p.dni == profesor.dni:
                        raise ValueError('Un profesor titular no puede ser contratado simultáneamente como profesor asociado')
                # Crear y añadir el profesor asociado
                self.profesores["asociados"].append(profesor)
                self.miembros_departamento._añadir_miembro(profesor)
                for a in profesor.asignaturas:
                    a._añadir_docente(profesor)
                print(f'{profesor.nombre} ha sido contratado como profesor asociado')                
            if isinstance(profesor, ProfesorTitular):
                # Verifica si el DNI ya pertenece a un profesor titular
                for p in self.profesores['titulares']:
                    if p.dni == profesor.dni:
                        raise ValueError(f'{p.nombre} ya está contratado como profesor titular')
                for p in self.profesores['asociados']:
                    if p.dni == profesor.dni:
                        raise ValueError(f'{p.nombre} ya está contratado como profesor asociado')
                
                self.profesores["titulares"].append(profesor)
                self.miembros_departamento._añadir_miembro(profesor)
                for a in profesor.asignaturas:
                    a._añadir_docente(profesor) # deberia funcionar
                print(f'{profesor.nombre} ha sido contratado como profesor titular')

        except Exception as e:
            print(f"Error inesperado al contratar al profesor asociado: {e}")
    
    def contratar_investigador(self, investigador):#

        try:
            for t in self.profesores:
                for p in self.profesores[t]:
                    if p.dni == investigador.dni:
                        raise NotInvestigador('Un profesor no puede ser contratado como investigador')
        
            self.investigadores.append(investigador)
            self.miembros_departamento._añadir_miembro(investigador)
            print(f'{investigador.nombre} ha sido contratado como investigador')
        except Exception as e:
            print(f"Error inesperado al contratar al investigador: {e}")

    def despedir_profesor(self, dni):#            
        try:
            if not isinstance(dni, str):
                raise TypeError('El tipo de dato introducido para el DNI no es correcto. Debe ser una cadena de texto')
            for lista in self.profesores.values():
                for p in lista:
                    if p.dni == dni:
                        lista.remove(p)  # Elimina el profesor de la lista.
                        self.miembros_departamento._eliminar_miembro(p)  # Elimina el profesor como miembro del departamento.
                        # se debe borrar como docente de las asignaturas que imparte

                        # for asignatura in reversed(p.asignaturas):
                        #     self.eliminar_profesor_asignatura(p, asignatura)

                        copia = p.asignaturas.copy()
                        for asignatura in copia: #eliminar como docente de las asignaturas
                            self.eliminar_profesor_asignatura(p, asignatura)
                        print(f'{p.nombre} ha sido despedido correctamente.')
                        return           
            raise DniNotFound((f'El dni {dni} no se encuentra en la base de datos'))

        except Exception as e:
            # Captura cualquier otra excepción inesperada y muestra el mensaje.
            print(f"Error inesperado: {e}")
    
    def despedir_investigador(self, dni):#
        try:
            if not isinstance(dni, str):
                raise TypeError('El tipo de dato introducido para el DNI no es correcto. Debe ser una cadena de texto')
            for p in self.investigadores:
                if p.dni == dni:
                    self.investigadores.remove(p)
                    self.miembros_departamento._eliminar_miembro(p)  # Elimina el investigador como miembro del departamento.
                    print(f'{p.nombre} fue despedido correctamente')
                    return
            raise DniNotFound((f'El dni {dni} no se encuentra en la base de datos'))

        except Exception as e: # excepcion informada
            print(f"Error inesperado: {e}")
        
    def asignar_profesor_asignatura(self, profesor, *asignaturas): #
        
        dni_profesores_asociados = [p.dni for p in self.profesores["asociados"]]
        dni_profesores_titulares = [p.dni for p in self.profesores["titulares"]]

        try:
            if not (isinstance(profesor, ProfesorTitular) or  isinstance(profesor, ProfesorAsociado)):
                raise TypeError('No pertenece a la clase ProfesorAsociado o ProfesorTitular')
            if not (profesor.dni in dni_profesores_asociados or profesor.dni in dni_profesores_titulares):
                raise DniNotFound(f'El profesor con dni {profesor.dni} no se encuentra en la base de datos, compruebe errores tipograficos o agregue previamente al profesor')
            
            for asignatura in asignaturas:
                if not isinstance(asignatura, Asignatura):
                    raise TypeError(f'{asignatura} debe pertencer a la clase Asignatura')
                # Verifica si la asignatura está disponible
                if asignatura in self.asignaturas:
                    if asignatura in profesor.asignaturas: # comprueba que no se asigna una asignatura de la que ya es docente
                        raise ValueError(f'{profesor.nombre} ya es docente en {asignatura.nombre}')

                    # Intenta añadir el docente a la asignatura y viceversa
                    asignatura._añadir_docente(profesor)
                    profesor._añadir_asignatura(asignatura)
                    print(f'La asignatura {asignatura.nombre} ha sido asignada correctamente a {profesor.nombre}')
                else:
                    # Si la asignatura no está disponible, levantar una excepción
                    raise ValueError(f"Asignatura {asignatura.nombre} no está disponible")
        except ValueError as v:
            # Maneja el caso de asignaturas no disponibles
            print(v)
        except DniNotFound as d:
            print(f'No se ha podido asignar las asignaturas:{d}')
        except Exception as e:
            # Captura cualquier otra excepción inesperada
            print(f"Error inesperado al asignar al {profesor.nombre} las asignaturas {','.join([asignatura.nombre for asignatura in asignaturas])}: {e}")


    def eliminar_profesor_asignatura(self, profesor, *asignaturas):#
        try:
            for asignatura in asignaturas:
                if not (isinstance(profesor, ProfesorAsociado) or isinstance(profesor, ProfesorTitular)):
                    raise TypeError(f'El tipo de dato introducido ({profesor}) para identificar al profesor no es valido. Debe ser una instancia de la clase Profesor')
                # Verificamos si la asignatura está en la lista de asignaturas disponibles.
                if not isinstance(asignatura, Asignatura):
                    raise TypeError(f'El tipo de dato introducido ({asignatura}) no es valido. Debe ser una instancia de la clase Asignatura')
                if asignatura not in self.asignaturas:
                    raise ValueError(f"Asignatura {asignatura.nombre} no está disponible")
                
                # Intentamos eliminar el docente de la asignatura y viceversa.
                asignatura._eliminar_docente(profesor)
                profesor._eliminar_asignatura(asignatura)
            return
        except Exception as e:
            print(f"Error inesperado:{e}")

    def get_datos_universidad(self):#
        cont = 0
        for i in self.profesores.values():
            cont += len(i)
        datos = {
            'nombre': self.nombre,
            'id': self.id,
            'n_estudiantes': len(self.estudiantes),
            'n_profesores': cont,
            'n_investigadores':len(self.investigadores)
        }
        print("\nDatos universidad:")
        for d in datos:
            print(d, datos[d])

    def matricular_asignaturas(estudiante, *asignaturas):
            asignaturas_matriculadas = []
            asignaturas_no_encontradas = []
            try:
                if not isinstance(asignatura, Asignatura):
                    raise TypeError('El tipo de dato introducido en el campo asignaturas incorreto. Debe pertenecer a la clase Asignatura')
                if not isinstance(estudiante, Estudiante):
                    raise TypeError('El tipo de dato introducido en el campo estudiante incorreto. Debe pertenecer a la clase Estudiante')        
                for asignatura in asignaturas:
                    
                    if asignatura in estudiante.asignaturas_matriculadas: 
                        raise ValueError(f'{estudiante.nombre} ya está matriculado en {asignatura}')
                    else:
                        estudiante._matricular_asignatura(asignatura)
                        asignaturas_matriculadas.append(asignatura.nombre)
                        
                
                if asignaturas_matriculadas:
                    print(f"Se han desmatriculado las siguientes asignaturas: {', '.join(asignaturas_matriculadas)}.")
                if asignaturas_no_encontradas:
                    print(f"El estudiante no se encuentra matriculado de las siguientes asignaturas: {', '.join(asignaturas_no_encontradas)}.")

            except Exception as e: # Mantener la captura genérica si no se anticipan errores específicos
                print(f"Error inesperado: {e}")

    def desmatricular_asignaturas(self,estudiante, *asignaturas):
        asignaturas_desmatriculadas = []
        asignaturas_no_encontradas = []
        try:
            for asignatura in asignaturas:
                if not isinstance(asignatura, Asignatura):
                    raise TypeError('El tipo de dato introducido en el campo asignaturas incorreto. Debe pertenecer a la clase Asignatura')
                if not isinstance(estudiante, Estudiante):
                    raise TypeError('El tipo de dato introducido en el campo estudiante incorreto. Debe pertenecer a la clase Estudiante')        
                
                if asignatura in estudiante.asignaturas_matriculadas: 
                    estudiante._desmatricular_asignatura(asignatura)
                    asignaturas_desmatriculadas.append(asignatura.nombre)
                else:
                    asignaturas_no_encontradas.append(asignatura.nombre)
            
            if asignaturas_desmatriculadas:
                print(f"Se han desmatriculado las siguientes asignaturas: {', '.join(asignaturas_desmatriculadas)}.")
            if asignaturas_no_encontradas:
                print(f"El estudiante no se encuentra matriculado de las siguientes asignaturas: {', '.join(asignaturas_no_encontradas)}.")
        except Exception as e: # Mantener la captura genérica si no se anticipan errores específicos
            print(f"Error inesperado: {e}")

    def agregar_miembro_departamento(self, persona, departamento):# #agregar una persona a un departamento no tendria sentido
        self.miembros_departamento.añadir_miembro(persona, departamento)         #ya que los miembros (profesores, investigadores...) se añaden automaticamente
                                                      #al crearlos. Lo que si tiene sentido es su modificacion (enunciado)
    
    def eliminar_miembro_departamento(self, persona, departamento):#
        self.miembros_departamento.eliminar_miembro(persona, departamento)

    def cambio_departamento(self, persona, nuevo_departamento):#
        self.miembros_departamento._cambiar_miembro(persona, nuevo_departamento)

    def get_profesores(self):#
        print("\nProfesores:")
        for profesor in self.profesores["asociados"] + self.profesores["titulares"]:
            print(profesor.devuelve_datos())

    def get_investigadores(self):#
        print("\nInvestigadores:")
        for investigador in self.investigadores:
            print(investigador.devuelve_datos())

    def get_miembros(self):
        print('\nMiembros de departamentos')
        self.miembros_departamento._datos_departamentos()
        
    def get_alumnos(self):#
        print("\nAlumnos:")
        for alumno in self.estudiantes:
            print(alumno.devuelve_datos())

    def asignaturas_alumno(self, dni):#
        for a in self.estudiantes:
            if a.dni == dni:
                print(a.devuelve_asignaturas())
                return
        raise DniNotFound(f'El alumno con dni {dni} no se encuentra en la base de datos, revise los datos introducidos')
    
    def definir_asignatura(self, id,nombre, creditos, modalidad : Departamento): # 
            try:
                for a in self.asignaturas:
                    if a.id == id: # los id's se asignan de manera automatica
                        raise ValueError(f'La asignatura {a.nombre} asociada al identificador {a.id} ya estaba registrada previamente')
                self.asignaturas.append(Asignatura(id,nombre, creditos, modalidad))
                print(f'{nombre} con id {id} ha sido añadida correctamente como asignatura')
            except Exception as e:
                print(f"Ocurrio un error inesperado:{e}")

    
    def eliminar_asignatura(self, id):
        try:
            if not isinstance(id, int):
                raise TypeError('Debe introducir el id (número entero) asociado a la asignatura')

            asignatura_encontrada = None
            for a in self.asignaturas:
                if a.id == id:
                    asignatura_encontrada = a
                    break
            
            if asignatura_encontrada is None:
                raise ValueError(f"La asignatura con id asociado {id} no figura en la base de datos")

            for lista in self.profesores.values():
                for p in lista:
                    if asignatura_encontrada in p.asignaturas:
                        raise ValueError('Existe algún profesor que imparte la asignatura')
                    
            for e in self.estudiantes:
                if asignatura_encontrada in e.asignaturas_matriculadas:
                    raise ValueError('Existe algún estudiante que cursa la asignatura')

            self.asignaturas.remove(asignatura_encontrada)
            print(f"Asignatura con id asociado {id} eliminada correctamente.")
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(f"Ocurrió un error inesperado al eliminar la asignatura: {e}")
    

    def definir_areas_investigacion(self, area):#
        if area in self.areas_investigacion:
            print('Este area ya se encuentra en la base de datos')
        else:
            self.areas_investigacion.append(area)
            print(f'{area} ha sido añadido como area de investigación')

    def eliminar_area_investigacion(self, area):#
        try:
            self.areas_investigacion.remove(area)
        except ValueError as e:
            print(f'{area} no figura en la base de datos')
        except Exception as e:
            print(f'No se puedo eliminar {area}, problema asociado: {e}')

    def _del_(self):
            try:
                # Eliminar todos los estudiantes
                copia = self.estudiantes.copy()
                for estudiante in copia:
                    self.eliminar_estudiante(estudiante.dni)

                # Eliminar todos los profesores asociados
                copia = self.profesores["asociados"].copy() + self.profesores["titulares"].copy()
                for profesor in copia:
                    self.despedir_profesor(profesor.dni)

                # Eliminar todos los investigadores
                copia = self.investigadores.copy()
                for investigador in copia:
                    self.despedir_investigador(investigador.dni)

                # Eliminar todas las asignaturas
                copia = self.asignaturas.copy()
                for asignatura in copia:
                    self.eliminar_asignatura(asignatura.id)

                print(f"Todos los miembros y asignaturas de la universidad {self.nombre} han sido eliminados.")
            except Exception as e:
                print(f"Ocurrió un error al eliminar la universidad {self.nombre}: {e}")
            finally:
                # Eliminar la universidad
            
                del self



# Ejemplo de uso:
if __name__ == "__main__":
    #############################################################################################
    
    # CREACION
    # Areas de investigacion
    areas = [
    "Aprendizaje automático y análisis predictivo",
    "Procesamiento del lenguaje natural y análisis de sentimientos",
    "Visualización de datos y análisis de redes complejas"
    ]

    # Asignaturas
    MLI = Asignatura(1,'Machine Learning I', 6, Departamento.DIIC)
    PCD = Asignatura(2,'Programacion Para Ciencia De Datos', 6, Departamento.DIIC)
    AEM = Asignatura(3,'Analisis Estadistico Multivariante', 6, Departamento.DIS)
    BDII = Asignatura(4,'Base de datos II', 6, Departamento.DITEC)
    SYS = Asignatura(5,'Señales y Sistemas', 6, Departamento.DIS) 

    
    
    # Profesores Asociados
    profesor_asociado1 = ProfesorAsociado('Benito Ubeda', '49445325M', 'C/Angeles, N10',Sexo.HOMBRE, Departamento.DIS, [SYS])
    profesor_asociado2 = ProfesorAsociado('Raquel Martinez España', '49445731E', 'C/Lorca, N1',Sexo.MUJER, Departamento.DIIC, [MLI, AEM, BDII])
    profesor_asociado3 = ProfesorAsociado('Antonio Guillen Teruel', '4865421J', 'C/Murcia, N53',Sexo.HOMBRE, Departamento.DITEC, [MLI])
    profesor_asociado4 = ProfesorAsociado('Daniel Sevilla Ruiz', '44465725S', 'C/Correos, N5',Sexo.HOMBRE, Departamento.DITEC, [BDII])
    profesor_asociado5 = ProfesorAsociado('Humberto Martinez Barbera', '44465725S', 'C/Apostol, N3',Sexo.HOMBRE, Departamento.DIIC, [PCD])
    profesor_asociado6 = ProfesorAsociado('Jorge Luis Navarro Camacho', '34361735I', 'C/Lonja, N12',Sexo.HOMBRE, Departamento.DIS, [AEM])
##comentario: Las areas de investigacion pueden ser más de una, por lo que SIEMPRE tienen que ser una lista (aunque haya solo un área de investigacion)

    # Profeores Titulares
    profesor_titular1 = ProfesorTitular('Jorge Bernal Bernabe', '54365725H', 'C/Sajon, N31',Sexo.HOMBRE, Departamento.DIIC, [PCD], areas[:2]) 
    profesor_titular2 = ProfesorTitular('Concepcion Dominguez Sanchez', '43261725F', 'C/Lomega, N21',Sexo.MUJER, Departamento.DIIC, [AEM], areas[1:3])

    # Investigadores
    investigador1 = Investigador('Jose Perez Ruiz', '23543276P', 'C/Despanto, N12', Sexo.HOMBRE, Departamento.DIS, areas[:1])
    investigador2 = Investigador('Lucia Sanchez Carril', '53514321T', 'C/Despanto, N12', Sexo.MUJER, Departamento.DIIC, areas[:1]) 

    # Estudiantes
    estudiante1 = Estudiante('Jorge Ballesta Cerezo', '49336768E', 'C/Aljufera, N12', Sexo.HOMBRE, [MLI, PCD,BDII])
    estudiante2 = Estudiante('Nasim El Arifi Ahmed', '42436768M', 'C/Albatro, N13', Sexo.HOMBRE, [MLI, AEM, SYS,])

    # Universidad
    universidad = Universidad('UMU', 1,[MLI,PCD, AEM, BDII, SYS],[Departamento.DIIC, Departamento.DIS, Departamento.DITEC],areas)

    # Contratacion de profesores asociados
    
    universidad.contratar_profesor(profesor_asociado1)
    
    universidad.contratar_profesor(profesor_asociado2)
    
    universidad.contratar_profesor(profesor_asociado6)

    # Contratación de profesores titulares

    universidad.contratar_profesor(profesor_titular1)
    
    universidad.contratar_profesor(profesor_titular2)

    # Contratar investigadores
    # Solo investigador
    universidad.contratar_investigador(investigador1)
    universidad.contratar_investigador(profesor_titular1)
    # Profesor Asociado (no deja)
    #universidad.contratar_investigador(profesor_asociado1.nombre, profesor_asociado1.dni, profesor_asociado1.direccion, profesor_asociado1.sexo,
    #                                   areas[0], profesor_asociado1.departamento) 
    
    # si contratamos un investigador y luego se convierte en profesor asociado, no saltara excepcion
    
    universidad.contratar_investigador(investigador2)
    
    profesor_asociado6 = ProfesorAsociado('Lucia Sanchez Carril', '53514321T', 'C/Despanto, N12', Sexo.MUJER, Departamento.DIIC, [SYS])

    universidad.contratar_profesor(profesor_asociado6)

    # Matricular estudiante
    
    universidad.matricular_estudiante(estudiante1)
    universidad.matricular_estudiante(estudiante1)

    universidad.matricular_estudiante(estudiante2)

    # Asignar asignaturas profesor
    universidad.asignar_profesor_asignatura(profesor_asociado1, MLI, SYS) 


    # Imprimir datos
    universidad.get_datos_universidad()
    universidad.get_profesores()
    universidad.get_investigadores()
    universidad.get_alumnos()
    universidad.get_miembros_departamento()
    universidad.get_miembros_departamento(Departamento.DIIC)
    universidad.get_miembros_departamento('dicc')
    # Asignaturas alumnos
    universidad.asignaturas_alumno('49336768E')

    # Definicion de asignaturas
    universidad.definir_asignatura(6, "Optimizacion II", 6, Departamento.DIS)
    print([asignatura.nombre for asignatura in universidad.asignaturas])

    universidad.definir_asignatura(2, "Optimizacion II", 6, Departamento.DIS)

    # Definicion de areas de investigacion

    universidad.definir_areas_investigacion('Aprendizaje Reforzado')

    # Cambiar departamento
    print(profesor_asociado1.departamento)
    universidad.cambio_departamento(profesor_asociado1, Departamento.DIS)
    universidad.cambio_departamento(profesor_asociado1, Departamento.DIIC)
    print(profesor_asociado1.departamento)
    print(universidad.profesores)
#############################################################################################
    # ELIMINACION
    # Eliminar areas de investigacion
    print(universidad.areas_investigacion)
    universidad.eliminar_area_investigacion('Aprendizaje automático y análisis predictivo')
    print(universidad.areas_investigacion)
    # Eliminar Asignaturas
    print([asignatura.nombre for asignatura in universidad.asignaturas])
    universidad.eliminar_asignatura(MLI.id) #NO DEJAR ELIMINAR UNA ASIGNATURA SI HAY PROFESOR QUE LA IMPARTEN O ALUMNOS QUE LA CURSAN
    print([asignatura.nombre for asignatura in universidad.asignaturas])
    universidad.eliminar_asignatura(MLI.nombre) 
    universidad.eliminar_asignatura(1243) 
    # Eliminar Profesores
    universidad.despedir_profesor(profesor_asociado1.dni)
    universidad.despedir_profesor(134324234) 
    universidad.despedir_profesor('49834895E') 


    # Eliminar investigadores
    universidad.despedir_investigador(investigador2.dni)
    universidad.despedir_investigador(134324234)
    universidad.despedir_investigador('49834895E')

    # Eliminar estudiantes
    universidad.eliminar_estudiante(estudiante1.dni)
    universidad.eliminar_estudiante(134324234)
    universidad.eliminar_estudiante('49834895E')

    # Eliminar asignatura para profesor
    universidad.eliminar_profesor_asignatura(profesor_asociado2, AEM, PCD, BDII)
    universidad.eliminar_profesor_asignatura('Pepe', MLI)
    universidad.eliminar_profesor_asignatura(profesor_asociado2, 'Optimizacion II')

    
    # Eliminar asignaturas para alumno
    universidad.desmatricular_asignaturas(estudiante1, BDII) # hay que implementaar un metodo que permita desmatricular en Estudiante


    # agregar matricular de asignaturas a alumno



    del universidad


   