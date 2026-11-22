"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Cliente, EntidadBase  # tipos usados en validación y herencia
# Excepciones propias que usa la reserva
from excepciones import (ErrorSoftwareFJ, OperacionNoPermitidaError,
                         ReservaInvalidaError)
from registro import log  # logger para registrar eventos y errores
from servicios import IVA, Servicio  # IVA para el cálculo y Servicio para validar tipo


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente, con máquina de estados."""

    # Estados posibles de una reserva (constantes de clase)
    PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = (
        "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA")

    def __init__(self, cliente, servicio, duracion):
        super().__init__()  # id único
        try:
            # Verifica que los objetos recibidos sean del tipo correcto
            if not isinstance(cliente, Cliente):
                raise TypeError("cliente debe ser instancia de Cliente")
            if not isinstance(servicio, Servicio):
                raise TypeError("servicio debe ser instancia de Servicio")
            servicio.verificar_disponibilidad()  # falla si está deshabilitado
            servicio.validar_parametros(duracion)  # falla si la duración no es válida
        except (TypeError, ErrorSoftwareFJ) as e:
            # Encadenamiento de excepciones: "from e" conserva el error original
            raise ReservaInvalidaError(f"No se pudo crear la reserva: {e}") from e
        # Si todo es válido, se guardan los datos de la reserva
        self._cliente, self._servicio, self._duracion = cliente, servicio, duracion
        self._estado = self.PENDIENTE  # toda reserva nace pendiente
        self._costo = None  # el costo se calcula al procesar

    @property
    def estado(self):
        return self._estado  # solo lectura

    @property
    def costo(self):
        return self._costo  # solo lectura

    def confirmar(self):
        """PENDIENTE -> CONFIRMADA."""
        if self._estado != self.PENDIENTE:  # solo se confirma lo pendiente
            raise OperacionNoPermitidaError(
                f"Solo se confirma una reserva PENDIENTE (actual: {self._estado}).")
        self._servicio.verificar_disponibilidad()  # el servicio sigue disponible?
        self._estado = self.CONFIRMADA  # cambia el estado
        log.info(f"Reserva #{self.id} CONFIRMADA")  # deja registro del evento

    def cancelar(self):
        """Cancela la reserva si aún no está cancelada ni procesada."""
        if self._estado in (self.CANCELADA, self.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}.")
        self._estado = self.CANCELADA  # cambia el estado
        log.info(f"Reserva #{self.id} CANCELADA")  # deja registro del evento

    def procesar(self, descuento: float = 0.0):
        """Calcula el costo final; demuestra try/except/else/finally."""
        try:
            # Solo una reserva confirmada puede procesarse
            if self._estado != self.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Debe estar CONFIRMADA para procesar (actual: {self._estado}).")
            # Cálculo polimórfico: depende del tipo de servicio (con IVA y descuento)
            costo = self._servicio.calcular_costo(self._duracion, IVA, descuento)
        except ErrorSoftwareFJ as e:
            log.error(f"Reserva #{self.id} no procesada: {e}")  # registra el fallo
            raise  # relanza el mismo error para que lo gestione quien llamó
        else:
            # Solo se ejecuta si NO hubo excepción
            self._costo = costo  # guarda el costo calculado
            self._estado = self.PROCESADA  # cierra el ciclo de la reserva
            log.info(f"Reserva #{self.id} PROCESADA. Total: ${costo:,.2f}")
            return costo
        finally:
            # Se ejecuta SIEMPRE, haya o no error
            log.debug(f"Fin de procesamiento de reserva #{self.id} "
                      f"(estado: {self._estado})")

    def describir(self):
        """Implementación concreta del método abstracto de EntidadBase."""
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} x {self._duracion}h")
