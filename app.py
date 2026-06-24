"""
=====================================================================
 Descuentos por Volumen
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_calculadora_descuentos_por_volumen_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Descuentos por Volumen."""

    def __init__(self, unidades, precio, descuento):
        self.unidades = float(unidades)
        self.precio = float(precio)
        self.descuento = float(descuento)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        subtotal = self.unidades * self.precio
        monto_desc = subtotal * (self.descuento / 100)
        total = subtotal - monto_desc
        precio_final = total / self.unidades if self.unidades > 0 else 0
        return {"subtotal": subtotal, "total": total, "precio_final": precio_final}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""
        return "✅ Descuento aplicado."


# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("unidades"), input_float("precio"), input_float("descuento"))
    r = c.calcular()
    html = f"""
      <div class="result-value">🏷️ Total: {fmt_moneda(r["total"])}</div>
      <p class="result-detail">Subtotal: {fmt_moneda(r["subtotal"])} · Precio final/u: {fmt_moneda(r["precio_final"])}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "unidades": input_float("unidades"),
            "precio": input_float("precio"),
            "descuento": input_float("descuento"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "unidades" in datos:
            document.querySelector("#unidades").value = datos["unidades"]
        if "precio" in datos:
            document.querySelector("#precio").value = datos["precio"]
        if "descuento" in datos:
            document.querySelector("#descuento").value = datos["descuento"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
