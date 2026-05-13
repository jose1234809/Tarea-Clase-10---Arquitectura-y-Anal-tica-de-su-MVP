import sqlite3
from .conexion import BaseDeDatos


class RegistroTRM:
    """CRUD de registros diarios de tasa de cambio."""

    def __init__(self, db: BaseDeDatos):
        self.db = db

    def crear(self, fecha: str, id_moneda: int, valor: float, id_usuario: int) -> int:
        if valor <= 0:
            raise ValueError("La tasa/TRM debe ser mayor que cero.")
        return self.db.ejecutar(
            """
            INSERT INTO registros_trm(fecha, id_moneda, valor, id_usuario)
            VALUES (?, ?, ?, ?)
            """,
            (fecha, id_moneda, valor, id_usuario),
        )

    def listar(self) -> list[sqlite3.Row]:
        return self.db.consultar(
            """
            SELECT
                r.id_registro,
                r.fecha,
                m.simbolo AS moneda,
                r.valor,
                u.nombre AS usuario
            FROM registros_trm r
            JOIN monedas m ON m.id_moneda = r.id_moneda
            JOIN usuarios u ON u.id_usuario = r.id_usuario
            ORDER BY r.fecha, r.id_registro
            """
        )

    def listar_por_rango(self, id_moneda: int, fecha_inicio: str, fecha_fin: str) -> list[sqlite3.Row]:
        return self.db.consultar(
            """
            SELECT *
            FROM registros_trm
            WHERE id_moneda = ? AND fecha BETWEEN ? AND ?
            ORDER BY fecha
            """,
            (id_moneda, fecha_inicio, fecha_fin),
        )

    def obtener(self, id_registro: int) -> sqlite3.Row | None:
        return self.db.consultar_uno(
            "SELECT * FROM registros_trm WHERE id_registro = ?", (id_registro,)
        )

    def actualizar(self, id_registro: int, fecha: str, id_moneda: int, valor: float, id_usuario: int) -> None:
        if not self.obtener(id_registro):
            raise ValueError("No existe un registro con ese ID.")
        if valor <= 0:
            raise ValueError("La tasa/TRM debe ser mayor que cero.")
        self.db.ejecutar(
            """
            UPDATE registros_trm
            SET fecha = ?, id_moneda = ?, valor = ?, id_usuario = ?
            WHERE id_registro = ?
            """,
            (fecha, id_moneda, valor, id_usuario, id_registro),
        )

    def eliminar(self, id_registro: int) -> None:
        if not self.obtener(id_registro):
            raise ValueError("No existe un registro con ese ID.")
        self.db.ejecutar("DELETE FROM registros_trm WHERE id_registro = ?", (id_registro,))
