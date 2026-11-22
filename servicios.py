"""Servicio abstracto y tres servicios especializados."""
from abc import abstractmethod  # para declarar métodos abstractos

from entidades import EntidadBase  # clase base de la que hereda Servicio
# Excepciones propias usadas en validaciones y cálculos
from excepciones import (CalculoInconsistenteError, ServicioInvalidoError,
                         ServicioNoDisponibleError)

IVA = 0.19  # impuesto al valor agregado usado en los cálculos (19 %)


class Servicio(EntidadBase):
    """Clase abstracta: define lo común a todos los servicios de Software FJ."""

    def __init__(self, nombre: str, tarifa_hora: float):
        super().__init__()  # id único desde EntidadBase
        # El nombre debe ser texto no vacío
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio requiere un nombre.")
        # La tarifa debe ser un número positivo
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}")
        self._nombre = nombre  # nombre del servicio
        self._tarifa_hora = float(tarifa_hora)  # tarifa por hora
        self._disponible = True  # todo servicio nace disponible

    @property
    def nombre(self):
        return self._nombre  # solo lectura

    @property
    def disponible(self):
        return self._disponible  # solo lectura

    def deshabilitar(self):
        self._disponible = False  # el servicio deja de poder reservarse

    def habilitar(self):
        self._disponible = True  # el servicio vuelve a estar disponible

    # --- métodos abstractos (polimorfismo): cada hijo los sobrescribe ---
    @abstractmethod
    def validar_parametros(self, duracion: float) -> None:
        """Valida la duración según las reglas de cada servicio."""
        ...

    @abstractmethod
    def calcular_costo_base(self, duracion: float) -> float:
        """Costo sin impuestos ni descuentos; varía según el servicio."""
        ...

    @abstractmethod
    def describir(self) -> str:
        """Texto descriptivo del servicio."""
        ...

    # --- "sobrecarga" de calcular_costo mediante parámetros opcionales ---
    def calcular_costo(self, duracion: float, impuesto: float = 0.0,
                       descuento: float = 0.0) -> float:
        """Variantes:
        calcular_costo(h)                     -> costo base
        calcular_costo(h, impuesto=0.19)      -> con impuesto
        calcular_costo(h, descuento=0.1)      -> con descuento
        calcular_costo(h, 0.19, 0.1)          -> con ambos
        """
        self.validar_parametros(duracion)  # polimorfismo: valida según el tipo
        # Impuesto entre 0 y 1; descuento entre 0 y menos de 1 (nunca 100 %)
        if not 0 <= impuesto <= 1 or not 0 <= descuento < 1:
            raise CalculoInconsistenteError(
                f"Impuesto/descuento fuera de rango: {impuesto}, {descuento}")
        # Aplica descuento primero y luego impuesto sobre el costo base
        total = self.calcular_costo_base(duracion) * (1 - descuento) * (1 + impuesto)
        if total <= 0:  # un costo no positivo indica un cálculo inconsistente
            raise CalculoInconsistenteError("El costo calculado no es positivo.")
        return round(total, 2)  # redondea a 2 decimales

    def calcular_costo_con_iva(self, duracion: float) -> float:
        """Variante de conveniencia: costo con IVA y sin descuento."""
        return self.calcular_costo(duracion, impuesto=IVA)

    def verificar_disponibilidad(self):
        """Lanza error si el servicio está deshabilitado."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"'{self._nombre}' no está disponible.")


class ReservaSala(Servicio):
    """Servicio especializado: reserva de salas."""

    def __init__(self, nombre, capacidad, tarifa_hora=50000):
        super().__init__(nombre, tarifa_hora)  # valida nombre y tarifa
        # La capacidad debe ser un entero positivo
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad  # personas que caben en la sala

    def validar_parametros(self, duracion):
        # Una sala se reserva entre 1 y 12 horas
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 12:
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 12 horas.")

    def calcular_costo_base(self, duracion):
        return self._tarifa_hora * duracion  # tarifa lineal por hora

    def describir(self):
        return f"Sala '{self._nombre}' (cap. {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Servicio especializado: alquiler de equipos."""

    def __init__(self, nombre, unidades, tarifa_hora=20000):
        super().__init__(nombre, tarifa_hora)  # valida nombre y tarifa
        # Las unidades deben ser un entero positivo
        if not isinstance(unidades, int) or unidades <= 0:
            raise ServicioInvalidoError(f"Unidades inválidas: {unidades!r}")
        self._unidades = unidades  # unidades disponibles del equipo

    def validar_parametros(self, duracion):
        # El alquiler es de 1 a 72 horas
        if not isinstance(duracion, (int, float)) or not 1 <= duracion <= 72:
            raise ServicioInvalidoError("El alquiler es de 1 a 72 horas.")

    def calcular_costo_base(self, duracion):
        recargo = 1.10 if duracion > 24 else 1.0  # recargo por larga duración
        return self._tarifa_hora * duracion * recargo

    def describir(self):
        return f"Equipo '{self._nombre}' ({self._unidades} u.) - ${self._tarifa_hora:,.0f}/h"


class Asesoria(Servicio):
    """Servicio especializado: asesorías con nivel de experiencia."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # multiplicador por nivel

    def __init__(self, nombre, nivel="junior", tarifa_hora=80000):
        super().__init__(nombre, tarifa_hora)  # valida nombre y tarifa
        if nivel not in self.NIVELES:  # el nivel debe existir en el diccionario
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r}")
        self._nivel = nivel  # nivel del asesor

    def validar_parametros(self, duracion):
        # La asesoría dura entre media hora y 8 horas
        if not isinstance(duracion, (int, float)) or not 0.5 <= duracion <= 8:
            raise ServicioInvalidoError("La asesoría dura entre 0.5 y 8 horas.")

    def calcular_costo_base(self, duracion):
        # La tarifa se multiplica según el nivel del asesor
        return self._tarifa_hora * self.NIVELES[self._nivel] * duracion

    def describir(self):
        return f"Asesoría '{self._nombre}' nivel {self._nivel} - ${self._tarifa_hora:,.0f}/h"
