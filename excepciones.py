"""Excepciones personalizadas de Software FJ.

Se define una jerarquía: todas heredan de ErrorSoftwareFJ, de modo que
con un solo `except ErrorSoftwareFJ` se capturan todos los errores propios
del sistema, sin confundirlos con errores inesperados de Python.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de todo el sistema (raíz de la jerarquía)."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Falta un parámetro obligatorio (por ejemplo, un cliente sin documento)."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Los datos de un cliente (nombre, documento, email, teléfono) son inválidos."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Los parámetros de un servicio (tarifa, capacidad, duración...) son inválidos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado está deshabilitado y no puede reservarse."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Intento de reserva incorrecto (cliente/servicio/duración inválidos)."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """La operación no es válida para el estado actual de la reserva."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Un cálculo de costos produjo un resultado o parámetros inconsistentes."""
