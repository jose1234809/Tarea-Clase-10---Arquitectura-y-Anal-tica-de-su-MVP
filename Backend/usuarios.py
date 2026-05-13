import sqlite3
from .conexion import BaseDeDatos


class Usuario:
    """CRUD de usuarios que registran tasas de cambio."""

    def __init__(self, db: BaseDeDatos):
        self.db = db

    def crear(self, nombre: str, email: str, rol: str) -> int:
        if not nombre.strip() or not email.strip() or not rol.strip():
            raise ValueError("Todos los campos del usuario son obligatorios.")
        if "@" not in email:
            raise ValueError("El email debe contener @.")
        return self.db.ejecutar(
            "INSERT INTO usuarios(nombre, email, rol) VALUES (?, ?, ?)",
            (nombre.strip(), email.strip().lower(), rol.strip()),
        )

    def listar(self) -> list[sqlite3.Row]:
        return self.db.consultar("SELECT * FROM usuarios ORDER BY id_usuario")

    def obtener(self, id_usuario: int) -> sqlite3.Row | None:
        return self.db.consultar_uno(
            "SELECT * FROM usuarios WHERE id_usuario = ?", (id_usuario,)
        )

    def actualizar(self, id_usuario: int, nombre: str, email: str, rol: str) -> None:
        if not self.obtener(id_usuario):
            raise ValueError("No existe un usuario con ese ID.")
        if not nombre.strip() or not email.strip() or not rol.strip():
            raise ValueError("Todos los campos son obligatorios.")
        if "@" not in email:
            raise ValueError("El email debe contener @.")
        self.db.ejecutar(
            """
            UPDATE usuarios
            SET nombre = ?, email = ?, rol = ?
            WHERE id_usuario = ?
            """,
            (nombre.strip(), email.strip().lower(), rol.strip(), id_usuario),
        )

    def eliminar(self, id_usuario: int) -> None:
        if not self.obtener(id_usuario):
            raise ValueError("No existe un usuario con ese ID.")
        self.db.ejecutar("DELETE FROM usuarios WHERE id_usuario = ?", (id_usuario,))
