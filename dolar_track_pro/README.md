# Dólar Track Pro

Proyecto del Reto 3: Economía - **Dolar-Track**.

## Objetivo

Sistema modular End-to-End para registrar tasas diarias de moneda, calcular promedio, volatilidad y generar alertas de decisión:

- **Compra:** cuando la TRM/tasa está por debajo del promedio.
- **Venta:** cuando la TRM/tasa está por encima del promedio.
- **Mantener:** cuando la TRM/tasa es igual al promedio.

## Arquitectura del proyecto

```text
dolar_track_pro/
├── datos.py                 # Datos iniciales
├── conexion.py              # Creación dinámica de BD SQLite
├── usuarios.py              # Clase Usuario - CRUD
├── monedas.py               # Clase Moneda - CRUD
├── registros_trm.py         # Clase RegistroTRM - CRUD
├── analisis.py              # Clase AnalisisSemanal - métricas y alertas
├── main.py                  # Orquestador con menú interactivo
├── script_powerbi.py        # Script para conectar Power BI con SQLite
├── dolar_track.db           # Base de datos generada
├── informe_powerbi_dolar_track_grupo_7.pbix
└── requirements.txt
```

## Cómo ejecutar

1. Abre la carpeta en Visual Studio Code.
2. Abre una terminal dentro de la carpeta.
3. Ejecuta:

```bash
python main.py
```

El sistema crea automáticamente `dolar_track.db` si no existe.

## Validaciones incluidas

- Fechas en formato `AAAA-MM-DD`.
- Valores de TRM/tasa mayores que cero.
- Correos con `@`.
- Control de errores con `try-except`.
- Llaves foráneas activadas en SQLite.
- Restricción para no duplicar la misma fecha con la misma moneda.

## Conexión a Power BI

1. Abre Power BI Desktop.
2. Entra a **Obtener datos > Script de Python**.
3. Pega el contenido de `script_powerbi.py`.
4. Cambia la variable `db_path` por la ruta real del archivo `dolar_track.db`.
5. Carga las tablas:
   - `usuarios`
   - `monedas`
   - `registros_trm`
   - `analisis_semanal`
   - `registros_detalle` opcional

## Visuales sugeridos

1. Tarjeta: promedio de TRM/tasa.
2. Tarjeta: volatilidad.
3. Tarjeta: cantidad de registros.
4. Línea: evolución de la TRM/tasa por fecha.
5. Barras: cantidad de registros por usuario.
6. Segmentador: moneda o usuario.

## Entrega en GitHub

Subir todos estos archivos:

- Archivos `.py`
- `dolar_track.db`
- Archivo `.pbix`
- `README.md`
