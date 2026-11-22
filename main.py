"""Software FJ - Simulación de 15 operaciones (válidas e inválidas).
Ejecutar:  python main.py   (se genera software_fj.log)
"""
from entidades import Cliente  # clase Cliente
from excepciones import ErrorSoftwareFJ  # raíz de las excepciones propias
from registro import log  # logger del sistema
from reserva import Reserva  # clase Reserva
from servicios import Asesoria, AlquilerEquipo, ReservaSala  # servicios concretos


class GestorFJ:
    """Gestiona clientes, servicios y reservas en listas internas (sin base de datos)."""

    def __init__(self):
        # Tres listas en memoria: la única "base de datos" del sistema
        self.clientes, self.servicios, self.reservas = [], [], []

    def _intentar(self, titulo, funcion, lista=None):
        """Ejecuta una operación; si falla registra el error y continúa."""
        print(f"\n▶ {titulo}")  # muestra la operación en consola
        log.info(f"OPERACIÓN: {titulo}")  # y la registra en el log
        try:
            obj = funcion()  # ejecuta la operación recibida
        except ErrorSoftwareFJ as e:  # error esperado y propio del sistema
            # Registra el error y, si fue encadenado, también su causa original
            log.error(f"{titulo} -> {type(e).__name__}: {e}"
                      + (f" | causa: {e.__cause__!r}" if e.__cause__ else ""))
            print(f"   ✖ {type(e).__name__}: {e}")
            return None  # el programa continúa con la siguiente operación
        except Exception as e:  # error inesperado: el sistema sigue vivo
            log.critical(f"{titulo} -> ERROR INESPERADO {type(e).__name__}: {e}")
            print(f"   ✖ Error inesperado controlado: {e}")
            return None
        else:
            # Solo si no hubo error: guarda el objeto en su lista (si corresponde)
            if lista is not None:
                lista.append(obj)
            print(f"   ✔ {obj}")
            return obj
        finally:
            log.debug(f"Fin de operación: {titulo}")  # siempre se registra el cierre


def main():
    g = GestorFJ()  # crea el gestor con sus listas vacías

    # 1-4 Clientes (válidos e inválidos)
    ana = g._intentar("1. Registrar cliente válido (Ana)",
                      lambda: Cliente("ana gómez", "1012345678", "ana@mail.com", "3001234567"),
                      g.clientes)
    g._intentar("2. Registrar cliente con email inválido",
                lambda: Cliente("Luis Pérez", "98765432", "luis@@mail"), g.clientes)
    g._intentar("3. Registrar cliente sin documento (parámetro faltante)",
                lambda: Cliente("Pedro Ruiz", None, "pedro@mail.com"), g.clientes)
    carlos = g._intentar("4. Registrar cliente válido (Carlos)",
                         lambda: Cliente("Carlos Díaz", "80123456", "carlos@mail.com"),
                         g.clientes)

    # 5-8 Servicios (válidos e inválidos)
    sala = g._intentar("5. Crear sala válida",
                       lambda: ReservaSala("Sala Innovación", 12), g.servicios)
    g._intentar("6. Crear equipo con unidades inválidas",
                lambda: AlquilerEquipo("Proyector", -3), g.servicios)
    equipo = g._intentar("7. Crear alquiler de equipo válido",
                         lambda: AlquilerEquipo("Portátil Gamer", 5), g.servicios)
    asesoria = g._intentar("8. Crear asesoría válida (senior)",
                           lambda: Asesoria("Arquitectura de software", "senior"),
                           g.servicios)

    # Polimorfismo: el mismo código opera sobre tres tipos distintos de servicio
    print("\n── Catálogo (polimorfismo) ──")
    for s in g.servicios:
        print("  •", s.describir(), "| 2h c/IVA:", f"${s.calcular_costo_con_iva(2):,.2f}")

    # 9-14 Reservas exitosas y fallidas
    r1 = g._intentar("9. Reserva exitosa: Ana + sala 3h",
                     lambda: Reserva(ana, sala, 3), g.reservas)
    if r1:  # solo continúa si la reserva se creó
        g._intentar("   9a. Confirmar", lambda: (r1.confirmar(), r1)[1])
        g._intentar("   9b. Procesar con 10% de descuento",
                    lambda: f"Total ${r1.procesar(descuento=0.10):,.2f}")
        g._intentar("   9c. Cancelar reserva ya procesada (no permitido)",
                    lambda: r1.cancelar())

    g._intentar("10. Reserva con duración inválida (sala 20h)",
                lambda: Reserva(ana, sala, 20), g.reservas)

    equipo.deshabilitar()  # simula un servicio fuera de servicio
    g._intentar("11. Reserva de servicio no disponible",
                lambda: Reserva(carlos, equipo, 5), g.reservas)
    equipo.habilitar()  # lo devuelve a su estado normal

    r4 = g._intentar("12. Reserva Carlos + asesoría 2h",
                     lambda: Reserva(carlos, asesoria, 2), g.reservas)
    if r4:
        g._intentar("   12a. Procesar sin confirmar (no permitido)",
                    lambda: r4.procesar())
        g._intentar("   12b. Cancelar", lambda: (r4.cancelar(), r4)[1])

    g._intentar("13. Reserva con cliente nulo (encadenamiento)",
                lambda: Reserva(None, sala, 2), g.reservas)
    g._intentar("14. Costo con descuento inconsistente (150%)",
                lambda: sala.calcular_costo(2, 0.19, 1.5))
    # 15: error NO previsto (ZeroDivisionError) para demostrar el "except Exception"
    g._intentar("15. Error inesperado (división por cero) controlado",
                lambda: 1 / 0)

    # Resumen final
    print("\n── Resumen ──")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | "
          f"Reservas: {len(g.reservas)}")
    for r in g.reservas:
        print("  •", r.describir())
    print("\nEl sistema terminó sin interrupciones. Revise software_fj.log")


if __name__ == "__main__":  # solo se ejecuta al correr este archivo directamente
    main()
