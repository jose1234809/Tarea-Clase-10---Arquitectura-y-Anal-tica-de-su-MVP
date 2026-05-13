from datetime import datetime
from statistics import mean, pstdev

from .conexion import BaseDeDatos
from .registros_trm import RegistroTRM


class AnalisisSemanal:
    """Calcula promedio, volatilidad y alertas de compra/venta."""

    def __init__(self, db: BaseDeDatos):
        self.db = db
        self.registros = RegistroTRM(db)

    def calcular(self, id_usuario: int, id_moneda: int, fecha_inicio: str, fecha_fin: str) -> dict:
        registros = self.registros.listar_por_rango(id_moneda, fecha_inicio, fecha_fin)
        if len(registros) < 2:
            raise ValueError("Se necesitan mínimo 2 registros para calcular volatilidad.")

        valores = [float(r["valor"]) for r in registros]
        promedio = mean(valores)
        volatilidad = pstdev(valores)

        alertas = []
        dias_compra = 0
        dias_venta = 0
        for registro in registros:
            valor = float(registro["valor"])
            if valor < promedio:
                decision = "COMPRA"
                dias_compra += 1
            elif valor > promedio:
                decision = "VENTA"
                dias_venta += 1
            else:
                decision = "MANTENER"
            alertas.append(
                {
                    "fecha": registro["fecha"],
                    "valor": valor,
                    "decision": decision,
                    "diferencia_promedio": valor - promedio,
                }
            )

        return {
            "id_usuario": id_usuario,
            "id_moneda": id_moneda,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "promedio": round(promedio, 2),
            "volatilidad": round(volatilidad, 2),
            "dias_compra": dias_compra,
            "dias_venta": dias_venta,
            "cantidad_registros": len(registros),
            "fecha_calculo": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alertas": alertas,
        }

    def guardar(self, resultado: dict) -> int:
        return self.db.ejecutar(
            """
            INSERT INTO analisis_semanal(
                id_usuario, id_moneda, fecha_inicio, fecha_fin,
                dias_compra, dias_venta, promedio, volatilidad,
                cantidad_registros, fecha_calculo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                resultado["id_usuario"],
                resultado["id_moneda"],
                resultado["fecha_inicio"],
                resultado["fecha_fin"],
                resultado["dias_compra"],
                resultado["dias_venta"],
                resultado["promedio"],
                resultado["volatilidad"],
                resultado["cantidad_registros"],
                resultado["fecha_calculo"],
            ),
        )

    def listar(self):
        return self.db.consultar(
            """
            SELECT
                a.id_analisis,
                u.nombre AS usuario,
                m.simbolo AS moneda,
                a.fecha_inicio,
                a.fecha_fin,
                a.promedio,
                a.volatilidad,
                a.dias_compra,
                a.dias_venta,
                a.cantidad_registros,
                a.fecha_calculo
            FROM analisis_semanal a
            JOIN usuarios u ON u.id_usuario = a.id_usuario
            JOIN monedas m ON m.id_moneda = a.id_moneda
            ORDER BY a.id_analisis DESC
            """
        )
