import os
import sqlite3
from datetime import datetime

from .analisis import AnalisisSemanal
from .conexion import BaseDeDatos
from .monedas import Moneda
from .registros_trm import RegistroTRM
from .usuarios import Usuario

# La ruta se genera dinámicamente con os para que funcione en cualquier computador.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "dolar_track.db")


def leer_texto(mensaje: str, obligatorio: bool = True) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor or not obligatorio:
            return valor
        print("❌ Este campo no puede quedar vacío.")


def leer_entero(mensaje: str, minimo: int | None = None) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"❌ El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("❌ Digita un número entero válido.")


def leer_float(mensaje: str, minimo: float | None = None) -> float:
    while True:
        try:
            valor = float(input(mensaje).replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"❌ El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("❌ Digita un número válido. Ejemplo: 4210.50")


def leer_fecha(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        try:
            datetime.strptime(valor, "%Y-%m-%d")
            return valor
        except ValueError:
            print("❌ Fecha inválida. Usa el formato AAAA-MM-DD. Ejemplo: 2026-04-29")


def imprimir_tabla(filas) -> None:
    if not filas:
        print("⚠️ No hay datos para mostrar.")
        return
    columnas = filas[0].keys()
    print(" | ".join(columnas))
    print("-" * 100)
    for fila in filas:
        print(" | ".join(str(fila[col]) for col in columnas))


def ejecutar_seguro(accion) -> None:
    try:
        accion()
    except sqlite3.IntegrityError as error:
        print(f"❌ Error de integridad en la BD: {error}")
        print("Revisa que no estés duplicando fechas/monedas o eliminando datos relacionados.")
    except ValueError as error:
        print(f"❌ {error}")
    except Exception as error:
        print(f"❌ Ocurrió un error inesperado: {error}")


def menu_usuarios(servicio: Usuario) -> None:
    while True:
        print("\n--- CRUD USUARIOS ---")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Actualizar usuario")
        print("4. Eliminar usuario")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            nombre = leer_texto("Nombre: ")
            email = leer_texto("Email: ")
            rol = leer_texto("Rol: ")
            ejecutar_seguro(lambda: print(f"✅ Usuario creado con ID {servicio.crear(nombre, email, rol)}"))
        elif opcion == "2":
            imprimir_tabla(servicio.listar())
        elif opcion == "3":
            id_usuario = leer_entero("ID usuario a actualizar: ", 1)
            nombre = leer_texto("Nuevo nombre: ")
            email = leer_texto("Nuevo email: ")
            rol = leer_texto("Nuevo rol: ")
            ejecutar_seguro(lambda: (servicio.actualizar(id_usuario, nombre, email, rol), print("✅ Usuario actualizado.")))
        elif opcion == "4":
            id_usuario = leer_entero("ID usuario a eliminar: ", 1)
            ejecutar_seguro(lambda: (servicio.eliminar(id_usuario), print("✅ Usuario eliminado.")))
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida.")


def menu_monedas(servicio: Moneda) -> None:
    while True:
        print("\n--- CRUD MONEDAS ---")
        print("1. Crear moneda")
        print("2. Listar monedas")
        print("3. Actualizar moneda")
        print("4. Eliminar moneda")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            nombre = leer_texto("Nombre moneda: ")
            simbolo = leer_texto("Símbolo. Ejemplo USD: ")
            descripcion = leer_texto("Descripción: ", obligatorio=False)
            ejecutar_seguro(lambda: print(f"✅ Moneda creada con ID {servicio.crear(nombre, simbolo, descripcion)}"))
        elif opcion == "2":
            imprimir_tabla(servicio.listar())
        elif opcion == "3":
            id_moneda = leer_entero("ID moneda a actualizar: ", 1)
            nombre = leer_texto("Nuevo nombre: ")
            simbolo = leer_texto("Nuevo símbolo: ")
            descripcion = leer_texto("Nueva descripción: ", obligatorio=False)
            ejecutar_seguro(lambda: (servicio.actualizar(id_moneda, nombre, simbolo, descripcion), print("✅ Moneda actualizada.")))
        elif opcion == "4":
            id_moneda = leer_entero("ID moneda a eliminar: ", 1)
            ejecutar_seguro(lambda: (servicio.eliminar(id_moneda), print("✅ Moneda eliminada.")))
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida.")


def menu_registros(servicio: RegistroTRM, usuarios: Usuario, monedas: Moneda) -> None:
    while True:
        print("\n--- CRUD REGISTROS TRM ---")
        print("1. Crear registro diario")
        print("2. Listar registros")
        print("3. Actualizar registro")
        print("4. Eliminar registro")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            imprimir_tabla(monedas.listar())
            id_moneda = leer_entero("ID moneda: ", 1)
            imprimir_tabla(usuarios.listar())
            id_usuario = leer_entero("ID usuario: ", 1)
            fecha = leer_fecha("Fecha del registro AAAA-MM-DD: ")
            valor = leer_float("Valor TRM/tasa: ", 0.01)
            ejecutar_seguro(lambda: print(f"✅ Registro creado con ID {servicio.crear(fecha, id_moneda, valor, id_usuario)}"))
        elif opcion == "2":
            imprimir_tabla(servicio.listar())
        elif opcion == "3":
            imprimir_tabla(servicio.listar())
            id_registro = leer_entero("ID registro a actualizar: ", 1)
            imprimir_tabla(monedas.listar())
            id_moneda = leer_entero("Nuevo ID moneda: ", 1)
            imprimir_tabla(usuarios.listar())
            id_usuario = leer_entero("Nuevo ID usuario: ", 1)
            fecha = leer_fecha("Nueva fecha AAAA-MM-DD: ")
            valor = leer_float("Nuevo valor: ", 0.01)
            ejecutar_seguro(lambda: (servicio.actualizar(id_registro, fecha, id_moneda, valor, id_usuario), print("✅ Registro actualizado.")))
        elif opcion == "4":
            imprimir_tabla(servicio.listar())
            id_registro = leer_entero("ID registro a eliminar: ", 1)
            ejecutar_seguro(lambda: (servicio.eliminar(id_registro), print("✅ Registro eliminado.")))
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida.")


def menu_analisis(servicio: AnalisisSemanal, usuarios: Usuario, monedas: Moneda) -> None:
    while True:
        print("\n--- ANALÍTICA Y ALERTAS ---")
        print("1. Calcular promedio, volatilidad y alertas")
        print("2. Listar análisis guardados")
        print("0. Volver")
        opcion = input("Opción: ").strip()

        if opcion == "1":
            imprimir_tabla(usuarios.listar())
            id_usuario = leer_entero("ID usuario responsable del análisis: ", 1)
            imprimir_tabla(monedas.listar())
            id_moneda = leer_entero("ID moneda a analizar: ", 1)
            fecha_inicio = leer_fecha("Fecha inicio AAAA-MM-DD: ")
            fecha_fin = leer_fecha("Fecha fin AAAA-MM-DD: ")

            def accion():
                resultado = servicio.calcular(id_usuario, id_moneda, fecha_inicio, fecha_fin)
                print("\n✅ RESULTADO DEL ANÁLISIS")
                print(f"Promedio: {resultado['promedio']}")
                print(f"Volatilidad: {resultado['volatilidad']}")
                print(f"Días de compra: {resultado['dias_compra']}")
                print(f"Días de venta: {resultado['dias_venta']}")
                print("\nAlertas por día:")
                for alerta in resultado["alertas"]:
                    print(
                        f"{alerta['fecha']} | valor: {alerta['valor']} | "
                        f"decisión: {alerta['decision']} | "
                        f"dif. promedio: {alerta['diferencia_promedio']:.2f}"
                    )
                guardar = input("¿Guardar análisis en la BD? (s/n): ").strip().lower()
                if guardar == "s":
                    id_analisis = servicio.guardar(resultado)
                    print(f"✅ Análisis guardado con ID {id_analisis}.")

            ejecutar_seguro(accion)
        elif opcion == "2":
            imprimir_tabla(servicio.listar())
        elif opcion == "0":
            break
        else:
            print("❌ Opción inválida.")


def main() -> None:
    db = BaseDeDatos(DB_PATH)
    db.inicializar()

    usuarios = Usuario(db)
    monedas = Moneda(db)
    registros = RegistroTRM(db)
    analisis = AnalisisSemanal(db)

    while True:
        print("\n==============================")
        print("📊 DÓLAR TRACK PRO")
        print("Base de datos:", DB_PATH)
        print("==============================")
        print("1. CRUD usuarios")
        print("2. CRUD monedas")
        print("3. CRUD registros TRM")
        print("4. Analítica y alertas")
        print("0. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            menu_usuarios(usuarios)
        elif opcion == "2":
            menu_monedas(monedas)
        elif opcion == "3":
            menu_registros(registros, usuarios, monedas)
        elif opcion == "4":
            menu_analisis(analisis, usuarios, monedas)
        elif opcion == "0":
            print("👋 Sistema cerrado correctamente.")
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    main()
