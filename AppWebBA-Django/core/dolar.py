# core/dolar.py
import bcchapi
import pandas as pd

try:
    siete = bcchapi.Siete(file="credenciales.txt")  # Tu archivo debe estar en la raíz del proyecto
    data = siete.cuadro(
        series=["F073.TCO.PRE.Z.D"],  # Dólar observado diario
        nombres=["dolar"]
    )
    dolar_actual = float(data["dolar"].iloc[-1])  # Último valor del dólar
except:
    dolar_actual = 900.0  # Fallback si falla la API
