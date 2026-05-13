import sqlite3
from typing import Iterable, Optional

from .datos import MONEDAS_INICIALES, REGISTROS_TRM_INICIALES, USUARIOS_INICIALES


class BaseDeDatos:
    """Administra la conexión, creación y carga inicial de la base de datos."""

    def __init__(self, ruta_db: str):
        self.ruta_db = ruta_db

    def conectar(self) -> sqlite3.Connection:
        conexion = sqlite3.connect(self.ruta_db)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def ejecutar(self, sql: str, parametros: Iterable = ()) -> int:
        with self.conectar() as conexion:
            cursor = conexion.execute(sql, tuple(parametros))
            conexion.commit()
            return cursor.lastrowid

    def consultar(self, sql: str, parametros: Iterable = ()) -> list[sqlite3.Row]:
        with self.conectar() as conexion:
            cursor = conexion.execute(sql, tuple(parametros))
            return cursor.fetchall()

    def consultar_uno(self, sql: str, parametros: Iterable = ()) -> Optional[sqlite3.Row]:
        resultados = self.consultar(sql, parametros)
        return resultados[0] if resultados else None

    def inicializar(self) -> None:
        self.crear_tablas()
        self.sembrar_datos_si_vacio()

    def crear_tablas(self) -> None:
        with self.conectar() as conexion:
            conexion.executescript(
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    rol TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS monedas (
                    id_moneda INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    simbolo TEXT NOT NULL UNIQUE,
                    descripcion TEXT
                );

                CREATE TABLE IF NOT EXISTS registros_trm (
                    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT NOT NULL,
                    id_moneda INTEGER NOT NULL,
                    valor REAL NOT NULL CHECK(valor > 0),
                    id_usuario INTEGER NOT NULL,
                    FOREIGN KEY (id_moneda) REFERENCES monedas(id_moneda),
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
                    UNIQUE(fecha, id_moneda)
                );

                CREATE TABLE IF NOT EXISTS analisis_semanal (
                    id_analisis INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_usuario INTEGER NOT NULL,
                    id_moneda INTEGER NOT NULL,
                    fecha_inicio TEXT NOT NULL,
                    fecha_fin TEXT NOT NULL,
                    dias_compra INTEGER NOT NULL,
                    dias_venta INTEGER NOT NULL,
                    promedio REAL NOT NULL,
                    volatilidad REAL NOT NULL,
                    cantidad_registros INTEGER NOT NULL,
                    fecha_calculo TEXT NOT NULL,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
                    FOREIGN KEY (id_moneda) REFERENCES monedas(id_moneda)
                );
                """
            )
            conexion.commit()

    def sembrar_datos_si_vacio(self) -> None:
        total = self.consultar_uno("SELECT COUNT(*) AS total FROM usuarios")["total"]
        if total > 0:
            return

        with self.conectar() as conexion:
            for usuario in USUARIOS_INICIALES:
                conexion.execute(
                    "INSERT INTO usuarios(nombre, email, rol) VALUES (?, ?, ?)",
                    (usuario["nombre"], usuario["email"], usuario["rol"]),
                )

            for moneda in MONEDAS_INICIALES:
                conexion.execute(
                    "INSERT INTO monedas(nombre, simbolo, descripcion) VALUES (?, ?, ?)",
                    (moneda["nombre"], moneda["simbolo"], moneda["descripcion"]),
                )

            for fecha, id_moneda, valor, id_usuario in REGISTROS_TRM_INICIALES:
                conexion.execute(
                    """
                    INSERT INTO registros_trm(fecha, id_moneda, valor, id_usuario)
                    VALUES (?, ?, ?, ?)
                    """,
                    (fecha, id_moneda, valor, id_usuario),
                )
            conexion.commit()
