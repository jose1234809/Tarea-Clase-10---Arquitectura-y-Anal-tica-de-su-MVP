# Dólar Track Pro

Dólar Track Pro es un sistema End-to-End desarrollado en Python, SQLite y Power BI, enfocado en el análisis de la TRM para apoyar decisiones financieras relacionadas con la compra y venta de divisas.

El proyecto corresponde al Reto 3: Economía - Dólar Track, y busca simular una solución tecnológica para un inversionista que necesita registrar, analizar y visualizar el comportamiento diario de la tasa representativa del mercado.

## Descripción del sistema

El sistema permite registrar usuarios, monedas y valores diarios de la TRM mediante una arquitectura modular basada en programación orientada a objetos. A partir de los registros ingresados, se calculan indicadores como el promedio de la TRM, la volatilidad y las alertas de decisión.

Las alertas se generan comparando el valor de la TRM con el promedio registrado:

- Compra: cuando la TRM está por debajo del promedio.
- Venta: cuando la TRM está por encima del promedio.
- Mantener: cuando la TRM es igual al promedio.

De esta manera, el sistema puede apoyar el análisis de tendencias y facilitar una interpretación básica del comportamiento del dólar.

## Arquitectura del proyecto

El proyecto está organizado en módulos independientes para separar responsabilidades y facilitar el mantenimiento del código.

- `datos.py`: contiene los datos iniciales del sistema.
- `conexion.py`: crea y administra la base de datos SQLite.
- `usuarios.py`: gestiona la información de los usuarios.
- `monedas.py`: administra las monedas registradas.
- `registros_trm.py`: permite registrar y consultar valores diarios de TRM.
- `analisis.py`: calcula métricas como promedio, volatilidad y alertas.
- `main.py`: funciona como archivo orquestador del sistema.
- `script_powerbi.py`: conecta la base de datos con Power BI.
- `dolar_track.db`: base de datos generada por el sistema.
- `informe_powerbi_dolar_track_grupo_7.pbix`: dashboard analítico del proyecto.

## Base de datos

La base de datos está construida en SQLite y contiene las siguientes tablas principales:

### usuarios

Almacena la información de los usuarios que interactúan con el sistema.

Campos principales:

- `id_usuario`
- `nombre`
- `email`
- `rol`

### monedas

Contiene la información de las monedas registradas para el análisis.

Campos principales:

- `id_moneda`
- `nombre`
- `simbolo`
- `descripcion`

### registros_trm

Registra los valores diarios de la TRM asociados a una moneda y a un usuario.

Campos principales:

- `id_registro`
- `fecha`
- `valor`
- `id_moneda`
- `id_usuario`

### analisis_semanal

Guarda los resultados del análisis realizado sobre los registros de TRM.

Campos principales:

- `id_analisis`
- `fecha_inicio`
- `fecha_fin`
- `fecha_calculo`
- `promedio`
- `volatilidad`
- `dias_compra`
- `dias_venta`
- `id_usuario`

## Dashboard en Power BI

El proyecto incluye un dashboard en Power BI conectado a la base de datos `dolar_track.db`. Este tablero permite visualizar de forma clara los principales indicadores del sistema.

El dashboard presenta:

- Promedio de la TRM.
- Volatilidad de la TRM.
- Cantidad total de registros.
- Evolución de la TRM por fecha.
- Cantidad de registros por usuario.
- Tabla de detalle con fecha, moneda, usuario y valor de la TRM.
- Filtros para facilitar el análisis de la información.

## Utilidad del proyecto

Dólar Track Pro puede ser útil para personas interesadas en hacer seguimiento al comportamiento del dólar y analizar sus variaciones en el tiempo. Aunque el sistema es una simulación académica, representa una solución aplicable a escenarios financieros básicos, donde se requiere registrar datos, calcular indicadores y visualizar información para apoyar la toma de decisiones.

El proyecto integra backend, base de datos y analítica visual, cumpliendo con una arquitectura End-to-End orientada al análisis financiero.
