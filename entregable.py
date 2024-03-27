from enum import Enum
from abc import ABCMeta, abstractmethod

class Departamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

class Sexo(Enum):
    HOMBRE = 1
    MUJER = 2

class Persona(metaclass= ABCMeta):
    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        self.sexo = sexo

    @abstractmethod
    def devuelve_datos(self):
        pass


class MiembroDepartamento():
    def __init__(self, miembros = {}): #diccionario que contiene como clave el departamento, y como valor, una lista de personas
        self.miembros = miembros
                                            #cada profesor/investigador está asociado a un único departamento
        
    def _añadir_miembro(self, persona):        #solo la universidad tiene acceso a estos métodos
        if persona.departamento.value is not None:
            print(f"Esta persona ya es miembro del departamento {persona.departamento.value}")
            return
        self.miembros[persona.departamento.value].append(persona)
        print(f"{persona.nombre} ha sido añadido como miembro del departamento {persona.departamento.value}")

    def _eliminar_miembro(self, persona):
        lista = self.miembros[persona.departamento.value]
        for p in lista:
            if p.dni == persona.dni:
                lista.remove(p)
                self.miembros[persona.departamento.value] = lista
                print(f"{persona.nombre} ha sido eliminado del departamento {persona.departamento.value}")
                return
        #No se da el caso de algún trabajador se quede sin departamento. Esta función solo se utiliza cuando eliminamos (despedimos) a un trabajador
    
    def _cambiar_miembro(self, persona, nuevo_departamento):
        departamento_actual = persona.departamento
        if departamento_actual is not None:
            if departamento_actual.value != nuevo_departamento.value:
                for p in self.miembros[departamento_actual.value]:
                    if p.dni == persona.dni:
                        self.miembros[departamento_actual.value] = self.miembros[departamento_actual.value].remove(p)
                        self._añadir_miembro(persona)
                print(f"{persona.nombre} ha sido trasladado del departamento {departamento_actual} al departamento {nuevo_departamento.value}")
            else:
                print(f"{persona.nombre} ya pertenece al departamento {nuevo_departamento.value}")
        else:
            print(f"{persona.nombre} no es miembro de ningún departamento")


class Estudiante(Persona): #Todo estudiante está matriculado de alguna asignatura, por lo que es obligatorio pasar un listado de asignaturas matriculadas
    def __init__(self, nombre, dni, direccion, sexo : Sexo, asignaturas_matriculadas):
        Persona().__init__(nombre, dni, direccion, sexo)
        self.asignaturas_matriculadas = asignaturas_matriculadas

    def devuelve_datos(self):
        return "Estudiante \t"+"Nombre: "+self.nombre+" DNI: "+self.dni+" Direccion: "+self.direccion+" Sexo: "+self.sexo.value

    def devuelve_asignaturas(self):
        print(f"El estudiante está matriculado de las siguientes asignaturas")
        for i in self.asignaturas_matriculadas:
            i.devuelve_datos()

class Investigador(Persona):
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion, departamento):
        Persona().__init__(self, nombre, dni, direccion, sexo)
        self.area_investigacion = area_investigacion
        self.departamento = departamento

    def devuelve_datos(self):
        return "Investigador \t"+"Nombre: "+self.nombre+" DNI: "+self.dni+" Direccion: "+self.direccion+" Sexo: "+self.sexo.value+" Area de investigación: "+self.area_investigacion+" Departamento :"+self.departamento.value

class ProfesorAsociado(Persona): #Todo profesor asociado imparte alguna asignatura, por lo que es obligatorio pasar un listado de asignaturas impartidas
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        Persona().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = asignaturas
        self.departamento = departamento #Todo profesor está asociado a un departamento, por lo que es obligatorio pasarlo al constructor

    def devuelve_datos(self):
        return "Profesor asociadio \t"+"Nombre: "+self.nombre+" DNI: "+self.dni+" Direccion: "+self.direccion+" Sexo: "+self.sexo.value+" Departamento :"+self.departamento.value

    def devuelve_asignaturas(self):
        print(f"El profesor imparte las siguientes asignaturas")
        for i in self.asignaturas:
            print(i.devuelve_datos())

class ProfesorTitular(Investigador): #Todo profesor titular imparte alguna asignatura, por lo que es obligatorio pasar un listado de asignaturas impartidas
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion, departamento, asignaturas): #Todo profesor titular pertenece a un area de investigacion
        Investigador().__init__(nombre, dni, direccion, sexo, area_investigacion)
        self.asignaturas = asignaturas
        self.departamento = departamento #Todo profesor está asociado a un departamento, por lo que es obligatorio pasarlo al constructor

    def _añadir_asignatura(self, asignatura):
        self.asignaturas.append(asignatura)

    def _eliminar_asignatura(self, asignatura):
        if asignatura in self.asignaturas:
            self.asignaturas.remove(asignatura)
    
    def devuelve_asignaturas(self):
        print(f"El profesor imparte las siguientes asignaturas")
        for i in self.asignaturas:
            print(i.devuelve_datos())

class Asignatura:
    def __init__(self, id, nombre, creditos, modalidad : Departamento):
        self.id = id
        self.nombre = nombre
        self.creditos = creditos
        self.modalidad = modalidad
        self.docentes = []

    def devuelve_datos(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Créditos: {self.creditos}, Modalidad: {self.modalidad.value}"
    
    def _añadir_docente(self, profesor):
        self.docentes.append(profesor)

    def _eliminar_docente(self, profesor):
        if profesor in self.docentes:
            self.docentes.remove(profesor)

class Universidad:
    def __init__(self, nombre, id, asignaturas, departamentos, areas_investigacion):
        self.nombre = nombre
        self.id = id
        self.asignaturas = asignaturas
        self.estudiantes = []
        self.profesores = {"asociados" : [], "titulares" : []} #diccionario de profesores con asociados y titulares
        self.investigadores = []
        self.areas_investigacion = areas_investigacion
        self.departamentos = departamentos
        self.miembros_departamento = MiembroDepartamento()
        for dep in self.departamentos:
            self.miembros_departamento.miembros[dep.value] = []


    def matricular_estudiante(self, nombre, dni, direccion, sexo, asignaturas_matriculadas):
        self.estudiantes.append(Estudiante(nombre, dni, direccion, sexo, asignaturas_matriculadas))

    def eliminar_estudiante(self, dni):
        for p in self.estudiantes:
            if p.dni == dni:
                self.estudiantes.remove(p)
                return
        return "Estudiante no encontrado"

    def contratar_profesor_asociado(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        profesor_asociado = ProfesorAsociado(nombre, dni, direccion, sexo, departamento, asignaturas)
        self.profesores["asociados"].append(profesor_asociado)
        self.miembros_departamento._añadir_miembro(profesor_asociado)

    def contratar_profesor_titular(self, nombre, dni, direccion, sexo, area_investigacion, departamento, asignaturas):
        profesor_titular = ProfesorTitular(nombre, dni, direccion, sexo, area_investigacion, departamento, asignaturas)
        self.profesores["titulares"].append(profesor_titular)
        self.miembros_departamento._añadir_miembro(profesor_titular)

    def contratar_investigador(self, nombre, dni, direccion, sexo, area_investigacion, departamento):
        investigador = Investigador(nombre, dni, direccion, sexo, area_investigacion, departamento)
        self.investigadores.append(investigador)
        self.miembros_departamento._añadir_miembro(investigador)

    def despedir_profesor(self, dni):
        for lista in self.profesores.values():
            for p in lista:
                if p.dni == dni:
                    lista.remove(p)
                    self.miembros_departamento._eliminar_miembro(p) #al eliminar un profesor, se elimina como miembro de su departamento
                    return
        return "Profesor no encontrado"
    
    def despedir_investigador(self, dni):
        for p in self.investigadores:
            if p.dni == dni:
                self.investigadores.remove(p)
        return "Profesor no encontrado"

    def asignar_profesor_asignatura(self, profesor, *asignaturas):
        for asignatura in asignaturas:
            if asignatura in self.asignaturas:
                asignatura._añadir_docente(profesor)
                profesor._añadir_asignatura(asignatura)
            else:
                print(f"Asignatura {asignatura.nombre} no está disponible")

    def eliminar_profesor_asignatura(self, profesor, *asignaturas):
        for asignatura in asignaturas:
            if asignatura in self.asignaturas:
                asignatura._eliminar_docente(profesor)
                profesor._eliminar_asignatura(asignatura)
            else:
                print(f"Asignatura {asignatura.nombre} no está disponible")

    def get_datos_universidad(self):
        cont = 0
        for i in self.profesores.values():
            cont += len(i)
        return {
            'nombre': self.nombre,
            'id': self.id,
            'n_estudiantes': len(self.estudiantes),
            'n_profesores': cont,
            'n_investigadores':len(self.investigadores)
        }

    def eliminar_estudiante_asignatura(self, estudiante, *asignaturas):
        for asignatura in asignaturas:
            if asignatura in estudiante.asignaturas_matriculadas:
                estudiante.asignaturas_matriculadas.remove(asignatura)
            else:
                print(f"El estudiante no se encuentra matriculado de la asignatura {asignatura.nombre}")

    def agregar_miembro_departamento(self, persona, departamento): #agregar una persona a un departamento no tendria sentido
        self.miembros_departamento.añadir_miembro(persona, departamento)         #ya que los miembros (profesores, investigadores...) se añaden automaticamente
                                                      #al crearlos. Lo que si tiene sentido es su modificacion (enunciado)
    
    def eliminar_miembro_departamento(self, persona, departamento):
        self.miembros_departamento.eliminar_miembro(persona, departamento)

    def cambio_departamento(self, persona, nuevo_departamento):
        self.miembros_departamento.cambiar_miembro(persona, nuevo_departamento)

    def get_profesores(self):
        print("Profesores:")
        for profesor in self.profesores["asociados"] + self.profesores["titulares"]:
            print(profesor.devuelve_datos())

    def get_investigadores(self):
        print("Investigadores:")
        for investigador in self.investigadores:
            print(investigador.devuelve_datos())

    def imprimir_alumnos(self):
        print("Alumnos:")
        for alumno in self.estudiantes:
            print(alumno.devuelve_datos())

# Ejemplo de uso:
if __name__ == "__main__":