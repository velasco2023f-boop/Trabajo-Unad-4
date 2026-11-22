# Software FJ – Sistema de Gestión de Clientes, Servicios y Reservas

Proyecto de la Fase 4 del curso **Programación (213023)** – UNAD.
Sistema orientado a objetos en Python, **sin base de datos**: los datos viven en listas en memoria
y solo se escribe un archivo de logs (`software_fj.log`).

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`ErrorSoftwareFJ` y derivadas) |
| `registro.py` | Configuración del logger (archivo `software_fj.log`) |
| `entidades.py` | `EntidadBase` (abstracta) y `Cliente` (encapsulación + validaciones) |
| `servicios.py` | `Servicio` (abstracta) y `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | `Reserva`: confirmar, cancelar y procesar (`try/except/else/finally`) |
| `main.py` | Simulación de 15 operaciones válidas e inválidas |

## Ejecución
```bash
python main.py
```
Requiere Python 3.8+ y no usa librerías externas.

## Conceptos aplicados
Abstracción, herencia, polimorfismo, encapsulación, "sobrecarga" mediante parámetros opcionales,
excepciones personalizadas, `try/except/else/finally`, encadenamiento (`raise ... from ...`) y logging.
