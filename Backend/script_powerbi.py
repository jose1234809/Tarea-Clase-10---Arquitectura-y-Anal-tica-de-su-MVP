"""
Script para conectar Power BI con la base de datos SQLite.
En Power BI: Obtener datos > Script de Python > pegar este código.
IMPORTANTE: cambia db_path por la ruta real donde tengas dolar_track.db.
"""

import sqlite3
import pandas as pd

# Cambia esta ruta por la de tu computador.
db_path = r"C:\Users\TU_USUARIO\Documents\dolar_track_pro\dolar_track.db"

conexion = sqlite3.connect(db_path)

usuarios = pd.read_sql_query("SELECT * FROM usuarios", conexion)
monedas = pd.read_sql_query("SELECT * FROM monedas", conexion)
registros_trm = pd.read_sql_query("SELECT * FROM registros_trm", conexion)
analisis_semanal = pd.read_sql_query("SELECT * FROM analisis_semanal", conexion)

# Tabla adicional opcional para crear visuales rápidos sin hacer relaciones manuales.
registros_detalle = pd.read_sql_query(
    """
    SELECT
        r.id_registro,
        r.fecha,
        r.valor,
        r.id_moneda,
        m.nombre AS nombre_moneda,
        m.simbolo AS simbolo_moneda,
        r.id_usuario,
        u.nombre AS nombre_usuario,
        u.rol AS rol_usuario
    FROM registros_trm r
    JOIN monedas m ON m.id_moneda = r.id_moneda
    JOIN usuarios u ON u.id_usuario = r.id_usuario
    ORDER BY r.fecha
    """,
    conexion,
)

conexion.close()
