from enum import Enum
from abc import ABCMeta, abstractmethod
#prueba

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


class MiembroDepartamento(): #pueden haber personas miembro de departamentos que no sean profesores ni investigadores...
    def __init__(self, departamento : Departamento, miembros = []):
        self.departamento = departamento
        self.miembros = miembros


class Estudiante(Persona): #Todo estudiante está matriculado de alguna asignatura, por lo que es obligatorio pasar un listado de asignaturas matriculadas
    def __init__(self, nombre, dni, direccion, sexo, asignaturas_matriculadas):
        Persona().__init__(nombre, dni, direccion, sexo)
        self.asignaturas_matriculadas = asignaturas_matriculadas

class Investigador(Persona):
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion, departamento):
        Persona().__init__(self, nombre, dni, direccion, sexo)
        self.area_investigacion = area_investigacion
        self.departamento = departamento
        departamento.miembros.append(self) #al crear un investigador lo asociamos directamente en la lista de miembros de su departamento


class ProfesorAsociado(Persona): #Todo profesor asociado imparte alguna asignatura, por lo que es obligatorio pasar un listado de asignaturas impartidas
    def __init__(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        Persona().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = asignaturas
        self.departamento = departamento #Todo profesor está asociado a un departamento, por lo que es obligatorio pasarlo al constructor
        departamento.miembros.append(self)


class ProfesorTitular(Investigador): #Todo profesor titular imparte alguna asignatura, por lo que es obligatorio pasar un listado de asignaturas impartidas
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion, departamento, asignaturas): #Todo profesor titular pertenece a un area de investigacion
        Investigador().__init__(nombre, dni, direccion, sexo, area_investigacion)
        self.asignaturas = asignaturas
        self.departamento = departamento #Todo profesor está asociado a un departamento, por lo que es obligatorio pasarlo al constructor
        departamento.miembros.append(self)

class Asignatura:
    def __init__(self, id, nombre, creditos, modalidad : Departamento):
        self.id = id
        self.nombre = nombre
        self.creditos = creditos
        self.modalidad = modalidad
        self.docentes = []

    def asignar_docente(self, profesor):
        self.docentes.append(profesor)

    def quitar_docente(self, profesor):
        if profesor in self.docentes:
            self.docentes.remove(profesor)




class Universidad:
    def __init__(self, nombre, ciudad, direccion, telefono, asignaturas):
        self.nombre = nombre
        self.ciudad = ciudad
        self.direccion = direccion
        self.telefono = telefono
        self.asignaturas = asignaturas
        self.profesores_asociados = []
        self.profesores_titulares = []
        self.investigadores = []
        self.areas_investigacion = []
        self.departamentos = []

    def matricular_estudiante(self, nombre, dni, direccion, sexo, asignaturas_matriculadas):
        Estudiante(nombre, dni, direccion, sexo, asignaturas_matriculadas)

    def eliminar_estudiante(self):
        pass 

    def contratar_profesor_asociado(self, nombre, dni, direccion, sexo, departamento, asignaturas):
        self.profesores_asociados.append(ProfesorAsociado(nombre, dni, direccion, sexo, departamento, asignaturas))

    def contratar_profesor_titular(self, nombre, dni, direccion, sexo, area_investigacion, departamento, asignaturas):
        self.profesores_titulares.append(ProfesorTitular(nombre, dni, direccion, sexo, area_investigacion, departamento, asignaturas))

    def despedir_profesor(self, profesor):
        pass

    def get_datos_universidad(self):
        return {
            'nombre': self.nombre,
            'ciudad': self.ciudad,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'n_estudiantes': self.n_estudiantes,
            'n_profesores': self.n_profesores
        }

    def set_datos_universidad(self, nombre, ciudad, direccion, telefono):
        self.nombre = nombre
        self.ciudad = ciudad
        self.direccion = direccion
        self.telefono = telefono

    def matricular_estudiante_asignatura(self, estudiante, *asignaturas):
        for asignatura in asignaturas:
            estudiante.asignaturas_matriculadas.append(asignatura)

    def eliminar_estudiante(self, estudiante, asignatura):
        pass

    def agregar_miembro(self, persona, departamento): #agregar una persona a un departamento no tendria sentido
        departamento.agregar_miembro(persona)         #ya que los miembros (profesores, investigadores...) se añaden automaticamente
                                                      #al crearlos. Lo que si tiene sentido es su modificacion (enunciado)
    
    def eliminar_miembro(self, persona, departamento):
        departamento.eliminar_miembro(persona)

    def cambio_dpto(self, persona, nuevo_departamento):
        persona.departamento.miembros.remove(persona)
        persona.departamento = nuevo_departamento
        nuevo_departamento.miembros.append(persona)


# Ejemplo de uso:
if __name__ == "__main__":