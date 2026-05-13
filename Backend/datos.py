"""Datos iniciales para Dólar Track Pro.
Este archivo se usa para sembrar la base de datos cuando se crea por primera vez.
"""

USUARIOS_INICIALES = [
    {
        "nombre": "Carlos Administrador",
        "email": "carlos.admin@dolartrack.com",
        "rol": "Administrador",
    },
    {
        "nombre": "Laura Analista",
        "email": "laura.analista@dolartrack.com",
        "rol": "Analista",
    },
]

MONEDAS_INICIALES = [
    {
        "nombre": "Dólar estadounidense",
        "simbolo": "USD",
        "descripcion": "Moneda base para seguimiento de TRM en Colombia",
    },
    {
        "nombre": "Euro",
        "simbolo": "EUR",
        "descripcion": "Moneda secundaria para comparación de decisiones de inversión",
    },
]

# Valores de ejemplo cercanos al dashboard de Power BI.
# Formato: fecha, id_moneda, valor, id_usuario
REGISTROS_TRM_INICIALES = [
    ("2026-04-23", 1, 4199.00, 1),
    ("2026-04-24", 1, 4211.00, 1),
    ("2026-04-25", 1, 4185.00, 1),
    ("2026-04-26", 1, 4225.00, 1),
    ("2026-04-27", 1, 4240.00, 1),
    ("2026-04-28", 1, 4196.00, 1),
    ("2026-04-29", 1, 4230.00, 1),
    ("2026-04-23", 2, 4540.00, 2),
    ("2026-04-24", 2, 4558.00, 2),
    ("2026-04-25", 2, 4532.00, 2),
    ("2026-04-26", 2, 4565.00, 2),
]
