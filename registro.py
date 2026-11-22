"""Configuración del archivo de logs (única persistencia permitida)."""
import logging  # módulo estándar de Python para registrar eventos
import os  # permite construir rutas de archivo independientes del sistema operativo

# Ruta absoluta del log: queda junto a este archivo, sin importar desde dónde se ejecute
RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Crea (una sola vez) y devuelve el logger del sistema."""
    logger = logging.getLogger("SoftwareFJ")  # obtiene el logger por nombre
    if not logger.handlers:  # evita duplicar manejadores si se llama varias veces
        logger.setLevel(logging.DEBUG)  # registra desde DEBUG hasta CRITICAL
        # Escribe en archivo; mode="w" lo reinicia en cada ejecución
        h = logging.FileHandler(RUTA_LOG, mode="w", encoding="utf-8")
        # Formato de cada línea: fecha | nivel | mensaje
        h.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s"))
        logger.addHandler(h)  # asocia el manejador al logger
    return logger  # devuelve el logger listo para usar


log = obtener_logger()  # instancia global que importan los demás módulos
