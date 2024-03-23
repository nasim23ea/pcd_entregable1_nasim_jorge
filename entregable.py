from enum import Enum
#prueba
class Departamento(Enum):
    DIIC = 1
    DITEC = 2
    DIS = 3

class Sexo(Enum):
    HOMBRE = 1
    MUJER = 2


class Persona:
    def __init__(self, nombre, dni, direccion, sexo):
        self.nombre = nombre
        self.dni = dni
        self.direccion = direccion
        self.sexo = sexo


class MiembroDepartamento(Persona, Departamento):
    def __init__(self, nombre, dni, direccion, sexo, departamento : Departamento):
        Persona().__init__(self, nombre, dni, direccion, sexo)
        self.departamento = departamento


class Investigador(Persona):
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion):
        Persona().__init__(self, nombre, dni, direccion, sexo)
        self.area_investigacion = area_investigacion 

class ProfesorAsociado(Persona):
    def __init__(self, nombre, dni, direccion, sexo, departamento):
        Persona().__init__(nombre, dni, direccion, sexo)
        self.asignaturas = []
        self.departamento = departamento #Todo profesor está asociado a un departamento, por lo que es obligatorio pasarlo al constructor

class ProfesorTitular(Investigador):
    def __init__(self, nombre, dni, direccion, sexo, area_investigacion, departamento):
        Investigador().__init__(nombre, dni, direccion, sexo, area_investigacion)
        self.asignaturas = []
        self.departamento = departamento #Todo profesor está asociado a un departamento, por lo que es obligatorio pasarlo al constructor

class Estudiante(Persona):
    def __init__(self, nombre, dni, direccion, sexo):
        super().__init__(nombre, dni, direccion, sexo)
        self.asignaturas_matriculadas = []


# Ejemplo de uso:
if __name__ == "__main__":
    investigador = MiembroDepartamento("Juan", "12345678X", "Calle A", "V", Departamento.DIIC)
    print(f"{investigador.nombre} está en el departamento {investigador.departamento}")

    investigador.cambiar_departamento(Departamento.DITEC)
    print(f"{investigador.nombre} ahora está en el departamento {investigador.departamento}")


# Ejemplo de uso:
if __name__ == "__main__":
    