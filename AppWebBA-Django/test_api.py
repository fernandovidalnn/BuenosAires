import bcchapi
from datetime import datetime

siete = bcchapi.Siete(file="credenciales.txt")

# Buscar el código correcto de la serie del dólar observado diario
codigo_serie = siete.buscar("dólar observado").query("frequencyCode == 'DAILY'").iloc[0]["seriesId"]

# Obtener datos desde hace algunos días para asegurarnos de encontrar algo válido
hoy = datetime.now().strftime('%Y-%m-%d')
desde = "2025-05-15"  # por ejemplo, una semana atrás

# Consultar la serie
data = siete.cuadro(
    series=[codigo_serie],
    nombres=["dolar"],
    desde=desde,
    hasta=hoy
)

# Verifica que haya datos
if data.empty:
    print("⚠️ No se encontraron datos para el rango indicado.")
else:
    valor_dolar = data["dolar"].iloc[-1]  # Último valor disponible
    print("✅ Valor del dólar más reciente:", valor_dolar)
