# Dólar Track Pro

Dólar Track Pro es un MVP financiero desarrollado en Python para registrar tasas de cambio, consultar información histórica y apoyar decisiones básicas de compra, venta o mantenimiento según el comportamiento de los registros.

## Estructura del proyecto

```text
dolar_track_pro_gui/
├── Backend/
│   ├── conexion.py
│   ├── datos.py
│   ├── usuarios.py
│   ├── monedas.py
│   ├── registros_trm.py
│   ├── analisis.py
│   └── dolar_track.db
│
├── Frontend/
│   ├── interfaz.py
│   └── img/
│       └── logo.png
│
├── main.py
├── requirements.txt
└── informe_powerbi_dolar_track_grupo_7.pbix
```

## ¿Para qué sirve?

El sistema permite registrar tasas diarias de monedas, guardar los datos en SQLite y consultar los registros desde una interfaz gráfica más intuitiva. El frontend fue construido con Tkinter y utiliza Pillow para cargar el logo de la aplicación.

## Frontend profesional

La interfaz incluye:

- Encabezado visual con logo centrado y texto grande.
- Panel lateral para registrar nuevas tasas.
- Validación de campos con `try-except`.
- Alertas de error y éxito con `messagebox`.
- Conexión directa con SQLite.
- Tabla grande con historial de registros.
- Tarjetas con métricas generales: total de registros, promedio general y última tasa.
- Alerta visual de decisión: compra, venta o mantener.

## Ejecución

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Ejecuta el proyecto desde la raíz:

```bash
python main.py
```

## Requisitos cumplidos de la entrega

- Carpeta `Backend` con módulos y base de datos.
- Carpeta `Frontend` con interfaz e imágenes.
- Archivo `main.py` como orquestador.
- Uso de `Label`, `Entry` y `Button`.
- Uso de Pillow para el logo.
- Uso de SQLite para persistencia.
- Uso de `try-except` para validaciones.
- Uso de `messagebox` para alertas al usuario.
