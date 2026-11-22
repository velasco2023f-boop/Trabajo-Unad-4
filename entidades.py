"""Clase abstracta base y Cliente (con encapsulación y validaciones)."""
import re  # expresiones regulares para validar el email
from abc import ABC, abstractmethod  # herramientas para crear clases abstractas

# Importa las excepciones propias que se lanzarán al validar datos
from excepciones import ClienteInvalidoError, ParametroFaltanteError

# Patrón de email: texto@dominio.ext (compilado una sola vez para eficiencia)
_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class EntidadBase(ABC):
    """Abstracción de cualquier entidad general del sistema."""

    _contador = 0  # atributo de clase: cuenta cuántas entidades se han creado

    def __init__(self):
        EntidadBase._contador += 1  # incrementa el contador compartido
        self._id = EntidadBase._contador  # asigna un id único a la entidad

    @property
    def id(self) -> int:
        """Id de solo lectura (encapsulación: no tiene setter)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad concreta debe implementar su propia descripción."""
        ...

    def __str__(self):
        return self.describir()  # str(obj) usa la descripción polimórfica


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validados."""

    def __init__(self, nombre=None, documento=None, email=None, telefono=None):
        super().__init__()  # asigna el id mediante la clase base
        # Los tres primeros datos son obligatorios: si falta alguno, se lanza error
        if nombre is None or documento is None or email is None:
            raise ParametroFaltanteError("Nombre, documento y email son obligatorios.")
        self.nombre = nombre  # pasa por el setter (valida)
        self.documento = documento  # pasa por el setter (valida)
        self.email = email  # pasa por el setter (valida)
        self.telefono = telefono  # opcional; también se valida

    # --- propiedades con validación (encapsulación) ---
    @property
    def nombre(self):
        return self.__nombre  # atributo privado (name mangling)

    @nombre.setter
    def nombre(self, v):
        # Debe ser texto, tener al menos 3 caracteres y no contener números
        if not isinstance(v, str) or len(v.strip()) < 3 or any(c.isdigit() for c in v):
            raise ClienteInvalidoError(f"Nombre inválido: {v!r}")
        self.__nombre = v.strip().title()  # normaliza: sin espacios y en Título

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, v):
        # Solo dígitos y longitud entre 6 y 12
        if not str(v).isdigit() or not 6 <= len(str(v)) <= 12:
            raise ClienteInvalidoError(f"Documento inválido: {v!r}")
        self.__documento = str(v)  # se guarda siempre como texto

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, v):
        # Debe ser texto y cumplir el patrón de email
        if not isinstance(v, str) or not _EMAIL.match(v):
            raise ClienteInvalidoError(f"Email inválido: {v!r}")
        self.__email = v.lower()  # normaliza a minúsculas

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, v):
        # Es opcional (None), pero si se da debe tener exactamente 10 dígitos
        if v is not None and (not str(v).isdigit() or len(str(v)) != 10):
            raise ClienteInvalidoError(f"Teléfono inválido (10 dígitos): {v!r}")
        self.__telefono = None if v is None else str(v)

    def describir(self):
        """Implementación concreta del método abstracto (polimorfismo)."""
        return f"Cliente #{self.id}: {self.nombre} (CC {self.documento}, {self.email})"
