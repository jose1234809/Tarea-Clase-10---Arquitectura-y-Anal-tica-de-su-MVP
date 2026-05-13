"""Frontend profesional de Dólar Track Pro.

Interfaz gráfica construida con Tkinter + Pillow, conectada al backend
SQLite del proyecto. Permite registrar tasas/TRM, validar los campos,
mostrar alertas con messagebox y visualizar los registros en una tabla.
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

# Permite ejecutar la app desde main.py o directamente desde este archivo.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Backend.conexion import BaseDeDatos
from Backend.monedas import Moneda
from Backend.registros_trm import RegistroTRM
from Backend.usuarios import Usuario

DB_PATH = PROJECT_ROOT / "Backend" / "dolar_track.db"
LOGO_PATH = Path(__file__).resolve().parent / "img" / "logo.png"


class DolarTrackApp:
    """Ventana principal del MVP con estilo tipo dashboard."""

    COLOR_BG = "#EEF3F8"
    COLOR_CARD = "#FFFFFF"
    COLOR_PRIMARY = "#0F3D5E"
    COLOR_PRIMARY_DARK = "#082A40"
    COLOR_ACCENT = "#21A67A"
    COLOR_ACCENT_DARK = "#168462"
    COLOR_WARNING = "#F59E0B"
    COLOR_DANGER = "#D64545"
    COLOR_TEXT = "#1F2937"
    COLOR_MUTED = "#6B7280"
    COLOR_BORDER = "#D8E0EA"
    COLOR_TABLE_ALT = "#F7FAFC"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Dólar Track Pro | Frontend MVP")
        self.root.geometry("1240x820")
        self.root.minsize(1100, 740)
        self.root.configure(bg=self.COLOR_BG)

        self.db = BaseDeDatos(str(DB_PATH))
        self.db.inicializar()
        self.servicio_usuarios = Usuario(self.db)
        self.servicio_monedas = Moneda(self.db)
        self.servicio_registros = RegistroTRM(self.db)

        self.logo_tk: ImageTk.PhotoImage | None = None
        self.metric_labels: dict[str, tk.Label] = {}
        self.selected_table_item: str | None = None

        self._crear_estilos()
        self._crear_interfaz()
        self._cargar_opciones()
        self._cargar_tabla()
        self.entry_valor.focus_set()

    # ------------------------------------------------------------------
    # Estilos generales
    # ------------------------------------------------------------------
    def _crear_estilos(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Modern.Treeview",
            background=self.COLOR_CARD,
            fieldbackground=self.COLOR_CARD,
            foreground=self.COLOR_TEXT,
            borderwidth=0,
            rowheight=34,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Modern.Treeview.Heading",
            background=self.COLOR_PRIMARY,
            foreground="white",
            borderwidth=0,
            font=("Segoe UI", 10, "bold"),
            padding=(8, 8),
        )
        style.map("Modern.Treeview.Heading", background=[("active", self.COLOR_PRIMARY_DARK)])
        style.map(
            "Modern.Treeview",
            background=[("selected", "#CDE7F6")],
            foreground=[("selected", self.COLOR_PRIMARY_DARK)],
        )

        style.configure(
            "Modern.TCombobox",
            fieldbackground="white",
            background="white",
            foreground=self.COLOR_TEXT,
            arrowcolor=self.COLOR_PRIMARY,
            padding=6,
            font=("Segoe UI", 10),
        )

    # ------------------------------------------------------------------
    # Construcción visual
    # ------------------------------------------------------------------
    def _crear_interfaz(self) -> None:
        self._crear_header()
        self._crear_contenido()

    def _crear_header(self) -> None:
        # Header más alto y centrado para evitar que el logo o los textos se recorten.
        header = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=205)
        header.pack(fill="x")
        header.pack_propagate(False)

        contenido_header = tk.Frame(header, bg=self.COLOR_PRIMARY)
        contenido_header.pack(fill="both", expand=True, padx=28, pady=(18, 14))

        try:
            imagen = Image.open(LOGO_PATH).convert("RGBA")
            bbox = imagen.getbbox()
            if bbox:
                imagen = imagen.crop(bbox)

            resample = getattr(Image, "Resampling", Image).LANCZOS
            imagen.thumbnail((760, 128), resample)
            self.logo_tk = ImageTk.PhotoImage(imagen)
            logo_label = tk.Label(contenido_header, image=self.logo_tk, bg=self.COLOR_PRIMARY)
            logo_label.pack(pady=(0, 8))
        except Exception:
            fallback = tk.Label(
                contenido_header,
                text="DÓLAR TRACK PRO",
                bg=self.COLOR_PRIMARY,
                fg="white",
                font=("Segoe UI", 34, "bold"),
            )
            fallback.pack(pady=(4, 8))

        subtitle = tk.Label(
            contenido_header,
            text="MVP financiero para registrar, validar y consultar tasas de cambio en SQLite",
            bg=self.COLOR_PRIMARY,
            fg="#EAF6FC",
            font=("Segoe UI", 13, "bold"),
            justify="center",
            wraplength=1000,
        )
        subtitle.pack(anchor="center")

    def _crear_contenido(self) -> None:
        contenedor = tk.Frame(self.root, bg=self.COLOR_BG)
        contenedor.pack(fill="both", expand=True, padx=24, pady=16)
        contenedor.grid_columnconfigure(0, weight=0)
        contenedor.grid_columnconfigure(1, weight=1)
        contenedor.grid_rowconfigure(0, weight=1)

        self._crear_panel_formulario(contenedor)
        self._crear_panel_datos(contenedor)

    def _crear_panel_formulario(self, parent: tk.Frame) -> None:
        card = tk.Frame(parent, bg=self.COLOR_CARD, highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        card.grid(row=0, column=0, sticky="ns", padx=(0, 20))
        card.configure(width=360)
        card.grid_propagate(False)

        tk.Label(
            card,
            text="Nuevo registro",
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            font=("Segoe UI", 19, "bold"),
        ).pack(anchor="w", padx=24, pady=(24, 2))

        tk.Label(
            card,
            text="Ingresa la tasa y guárdala directamente en la base de datos.",
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
            justify="left",
            wraplength=300,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=24, pady=(0, 18))

        form = tk.Frame(card, bg=self.COLOR_CARD)
        form.pack(fill="x", padx=24)

        self.entry_fecha = self._crear_input(form, "Fecha", "AAAA-MM-DD")
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))

        self.combo_moneda = self._crear_combo(form, "Moneda")
        self.entry_valor = self._crear_input(form, "Valor TRM / tasa", "Ejemplo: 4210.50")
        self.combo_usuario = self._crear_combo(form, "Usuario responsable")

        botones = tk.Frame(card, bg=self.COLOR_CARD)
        botones.pack(fill="x", padx=24, pady=(24, 12))

        self.boton_registrar = tk.Button(
            botones,
            text="Registrar tasa",
            command=self.registrar,
            bg=self.COLOR_ACCENT,
            fg="white",
            activebackground=self.COLOR_ACCENT_DARK,
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            cursor="hand2",
            padx=16,
            pady=12,
        )
        self.boton_registrar.pack(fill="x", pady=(0, 10))

        self.boton_limpiar = tk.Button(
            botones,
            text="Limpiar campos",
            command=self.limpiar,
            bg=self.COLOR_PRIMARY,
            fg="white",
            activebackground=self.COLOR_PRIMARY_DARK,
            activeforeground="white",
            font=("Segoe UI", 11, "bold"),
            bd=0,
            cursor="hand2",
            padx=16,
            pady=12,
        )
        self.boton_limpiar.pack(fill="x")

        nota = tk.Frame(card, bg="#F6F9FC", highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        nota.pack(fill="x", padx=24, pady=(18, 0))
        tk.Label(
            nota,
            text="Validaciones activas",
            bg="#F6F9FC",
            fg=self.COLOR_PRIMARY,
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=14, pady=(12, 2))
        tk.Label(
            nota,
            text="• Campos obligatorios\n• Fecha con formato correcto\n• Valor numérico mayor que cero\n• Sin duplicar fecha y moneda",
            bg="#F6F9FC",
            fg=self.COLOR_MUTED,
            justify="left",
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=14, pady=(0, 12))

    def _crear_panel_datos(self, parent: tk.Frame) -> None:
        panel = tk.Frame(parent, bg=self.COLOR_BG)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        metricas = tk.Frame(panel, bg=self.COLOR_BG)
        metricas.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        for columna in range(3):
            metricas.grid_columnconfigure(columna, weight=1)

        self._crear_tarjeta_metrica(metricas, 0, "Registros", "0", "Total en SQLite")
        self._crear_tarjeta_metrica(metricas, 1, "Promedio general", "$ 0.00", "Todas las monedas")
        self._crear_tarjeta_metrica(metricas, 2, "Última tasa", "$ 0.00", "Registro más reciente")

        tabla_card = tk.Frame(panel, bg=self.COLOR_CARD, highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        tabla_card.grid(row=1, column=0, sticky="nsew")
        tabla_card.grid_columnconfigure(0, weight=1)
        tabla_card.grid_rowconfigure(1, weight=1)

        encabezado = tk.Frame(tabla_card, bg=self.COLOR_CARD)
        encabezado.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 12))
        encabezado.grid_columnconfigure(0, weight=1)

        tk.Label(
            encabezado,
            text="Historial de registros",
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            font=("Segoe UI", 18, "bold"),
        ).grid(row=0, column=0, sticky="w")

        tk.Button(
            encabezado,
            text="Actualizar tabla",
            command=self._cargar_tabla,
            bg="#E8F1F8",
            fg=self.COLOR_PRIMARY,
            activebackground="#D7E9F5",
            activeforeground=self.COLOR_PRIMARY,
            font=("Segoe UI", 10, "bold"),
            bd=0,
            cursor="hand2",
            padx=14,
            pady=8,
        ).grid(row=0, column=1, sticky="e")

        tabla_wrapper = tk.Frame(tabla_card, bg=self.COLOR_CARD)
        tabla_wrapper.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        tabla_wrapper.grid_columnconfigure(0, weight=1)
        tabla_wrapper.grid_rowconfigure(0, weight=1)

        columnas = ("id", "fecha", "moneda", "valor", "usuario", "decision")
        self.tabla = ttk.Treeview(
            tabla_wrapper,
            columns=columnas,
            show="headings",
            height=16,
            style="Modern.Treeview",
        )

        encabezados = {
            "id": "ID",
            "fecha": "Fecha",
            "moneda": "Moneda",
            "valor": "Valor",
            "usuario": "Usuario",
            "decision": "Alerta",
        }
        anchos = {
            "id": 60,
            "fecha": 120,
            "moneda": 90,
            "valor": 130,
            "usuario": 230,
            "decision": 120,
        }
        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=anchos[col], anchor="center" if col != "usuario" else "w")

        self.tabla.tag_configure("par", background=self.COLOR_CARD)
        self.tabla.tag_configure("impar", background=self.COLOR_TABLE_ALT)
        self.tabla.tag_configure("compra", foreground=self.COLOR_ACCENT_DARK)
        self.tabla.tag_configure("venta", foreground=self.COLOR_DANGER)
        self.tabla.tag_configure("mantener", foreground=self.COLOR_WARNING)

        scroll_y = ttk.Scrollbar(tabla_wrapper, orient="vertical", command=self.tabla.yview)
        scroll_x = ttk.Scrollbar(tabla_wrapper, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

    def _crear_tarjeta_metrica(self, parent: tk.Frame, columna: int, titulo: str, valor: str, descripcion: str) -> None:
        card = tk.Frame(parent, bg=self.COLOR_CARD, highlightbackground=self.COLOR_BORDER, highlightthickness=1)
        card.grid(row=0, column=columna, sticky="ew", padx=0 if columna == 0 else 10)

        tk.Label(
            card,
            text=titulo,
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", padx=18, pady=(14, 0))

        label_valor = tk.Label(
            card,
            text=valor,
            bg=self.COLOR_CARD,
            fg=self.COLOR_PRIMARY,
            font=("Segoe UI", 22, "bold"),
        )
        label_valor.pack(anchor="w", padx=18, pady=(2, 0))

        tk.Label(
            card,
            text=descripcion,
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w", padx=18, pady=(0, 14))

        self.metric_labels[titulo] = label_valor

    def _crear_input(self, parent: tk.Frame, etiqueta: str, ayuda: str) -> tk.Entry:
        tk.Label(
            parent,
            text=etiqueta,
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(10, 4))
        entry = tk.Entry(
            parent,
            font=("Segoe UI", 11),
            bg="#F9FBFD",
            fg=self.COLOR_TEXT,
            relief="solid",
            bd=1,
            highlightthickness=1,
            highlightbackground=self.COLOR_BORDER,
            highlightcolor=self.COLOR_PRIMARY,
            insertbackground=self.COLOR_PRIMARY,
        )
        entry.pack(fill="x", ipady=9)
        tk.Label(
            parent,
            text=ayuda,
            bg=self.COLOR_CARD,
            fg=self.COLOR_MUTED,
            font=("Segoe UI", 8),
        ).pack(anchor="w", pady=(2, 0))
        return entry

    def _crear_combo(self, parent: tk.Frame, etiqueta: str) -> ttk.Combobox:
        tk.Label(
            parent,
            text=etiqueta,
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(10, 4))
        combo = ttk.Combobox(parent, state="readonly", style="Modern.TCombobox", font=("Segoe UI", 10))
        combo.pack(fill="x", ipady=5)
        return combo

    # ------------------------------------------------------------------
    # Datos y lógica
    # ------------------------------------------------------------------
    def _cargar_opciones(self) -> None:
        monedas = self.servicio_monedas.listar()
        usuarios = self.servicio_usuarios.listar()

        self.combo_moneda["values"] = [
            f"{m['id_moneda']} - {m['simbolo']} · {m['nombre']}" for m in monedas
        ]
        self.combo_usuario["values"] = [
            f"{u['id_usuario']} - {u['nombre']} · {u['rol']}" for u in usuarios
        ]

        if monedas:
            self.combo_moneda.current(0)
        if usuarios:
            self.combo_usuario.current(0)

    def _cargar_tabla(self) -> None:
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        registros = list(self.servicio_registros.listar())
        promedios = self._calcular_promedios_por_moneda(registros)

        for indice, fila in enumerate(registros[::-1]):
            moneda = fila["moneda"]
            valor = float(fila["valor"])
            decision = self._calcular_decision(valor, promedios.get(moneda, valor))
            tags = ["par" if indice % 2 == 0 else "impar", decision.lower()]

            self.tabla.insert(
                "",
                "end",
                values=(
                    fila["id_registro"],
                    fila["fecha"],
                    moneda,
                    self._formatear_moneda(valor),
                    fila["usuario"],
                    decision,
                ),
                tags=tuple(tags),
            )

        self._actualizar_metricas(registros)

    def _calcular_promedios_por_moneda(self, registros: list[sqlite3.Row]) -> dict[str, float]:
        acumulados: dict[str, list[float]] = {}
        for fila in registros:
            acumulados.setdefault(fila["moneda"], []).append(float(fila["valor"]))
        return {moneda: sum(valores) / len(valores) for moneda, valores in acumulados.items() if valores}

    def _calcular_decision(self, valor: float, promedio: float) -> str:
        diferencia = valor - promedio
        if abs(diferencia) < 0.01:
            return "Mantener"
        return "Compra" if valor < promedio else "Venta"

    def _actualizar_metricas(self, registros: list[sqlite3.Row]) -> None:
        total = len(registros)
        valores = [float(fila["valor"]) for fila in registros]
        promedio = sum(valores) / total if total else 0
        ultimo = registros[-1] if registros else None
        ultima_tasa = float(ultimo["valor"]) if ultimo else 0

        self.metric_labels["Registros"].configure(text=str(total))
        self.metric_labels["Promedio general"].configure(text=self._formatear_moneda(promedio))
        self.metric_labels["Última tasa"].configure(text=self._formatear_moneda(ultima_tasa))

    def _obtener_id(self, texto_combo: str, nombre_campo: str) -> int:
        if not texto_combo:
            raise ValueError(f"Debes seleccionar {nombre_campo}.")
        return int(texto_combo.split(" - ")[0])

    def registrar(self) -> None:
        """Valida los datos del formulario y los envía a SQLite."""
        try:
            fecha = self.entry_fecha.get().strip()
            valor_texto = self.entry_valor.get().strip().replace(",", ".")
            id_moneda = self._obtener_id(self.combo_moneda.get(), "una moneda")
            id_usuario = self._obtener_id(self.combo_usuario.get(), "un usuario")

            if not fecha or not valor_texto:
                raise ValueError("Todos los campos son obligatorios.")

            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError as exc:
                raise ValueError("La fecha debe tener el formato AAAA-MM-DD. Ejemplo: 2026-04-29") from exc

            try:
                valor = float(valor_texto)
            except ValueError as exc:
                raise ValueError("La cantidad debe ser un número. Ejemplo: 4210.50") from exc

            if valor <= 0:
                raise ValueError("La tasa/TRM debe ser mayor que cero.")

            id_registro = self.servicio_registros.crear(fecha, id_moneda, valor, id_usuario)
            messagebox.showinfo(
                "Registro exitoso",
                f"La tasa fue guardada correctamente en SQLite.\nID generado: {id_registro}",
            )
            self.limpiar(mantener_fecha=True)
            self._cargar_tabla()

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Registro duplicado",
                "Ya existe una tasa para esa fecha y esa moneda. Cambia la fecha o selecciona otra moneda.",
            )
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
        except Exception as error:
            messagebox.showerror("Error inesperado", f"Ocurrió un problema: {error}")

    def limpiar(self, mantener_fecha: bool = False) -> None:
        fecha_actual = self.entry_fecha.get().strip() if mantener_fecha else datetime.now().strftime("%Y-%m-%d")
        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, fecha_actual)
        self.entry_valor.delete(0, tk.END)
        if self.combo_moneda["values"]:
            self.combo_moneda.current(0)
        if self.combo_usuario["values"]:
            self.combo_usuario.current(0)
        self.entry_valor.focus_set()

    def _formatear_moneda(self, valor: float) -> str:
        return f"$ {valor:,.2f}"


def iniciar_app() -> None:
    root = tk.Tk()
    DolarTrackApp(root)
    root.mainloop()


if __name__ == "__main__":
    iniciar_app()
