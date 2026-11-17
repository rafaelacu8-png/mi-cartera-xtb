import streamlit as st
import yfinance as yf
import pandas as pd

# Configuración de la página para celular
st.set_page_config(page_title="Mi Portafolio XTB", page_icon="📈", layout="centered")

st.title("📈 Mi Portafolio XTB Chile")
st.write("Seguimiento diario en pesos chilenos (CLP)")

# --- PANEL DE INGRESO DE DATOS ---
with st.expander("⚙️ Configurar mi inversión (Toca aquí para editar)", expanded=True):
    inversion_clp = st.number_input("Capital total invertido (CLP)", min_value=1000, value=20000, step=5000)
    frac_voo = st.number_input("Fracciones ETF S&P 500 (VOO)", min_value=0.0, value=0.0258, format="%.4f")
    frac_nvda = st.number_input("Fracciones Nvidia (NVDA)", min_value=0.0, value=0.0325, format="%.4f")

# --- DESCARGA DE DATOS EN TIEMPO REAL ---
with st.spinner("Actualizando precios de mercado..."):
    tickers = ["NVDA", "VOO", "CLP=X"]
    datos = yf.download(tickers, period="1mo", progress=False)["Close"]

    precio_nvda = float(datos["NVDA"].iloc[-1])
    precio_voo = float(datos["VOO"].iloc[-1])
    dolar_clp = float(datos["CLP=X"].iloc[-1])

    valor_voo_clp = frac_voo * precio_voo * dolar_clp
    valor_nvda_clp = frac_nvda * precio_nvda * dolar_clp
    valor_total_clp = valor_voo_clp + valor_nvda_clp

    ganancia_clp = valor_total_clp - inversion_clp
    rentabilidad_pct = (ganancia_clp / inversion_clp) * 100

# --- TARJETAS DE RESULTADOS ---
st.divider()
col1, col2 = st.columns(2)
col1.metric("Valor Actual", f"${valor_total_clp:,.0f} CLP", f"{ganancia_clp:+,.0f} CLP ({rentabilidad_pct:+.2f}%)")
col2.metric("Dólar Hoy", f"${dolar_clp:,.1f} CLP")

st.write(f"**ETF S&P 500:** ${valor_voo_clp:,.0f} CLP (${precio_voo:.2f} USD)")
st.write(f"**Nvidia:** ${valor_nvda_clp:,.0f} CLP (${precio_nvda:.2f} USD)")

# --- GRÁFICO INTERACTIVO ---
st.subheader("Evolución últimos 30 días (CLP)")
historial_clp = (datos["VOO"] * frac_voo + datos["NVDA"] * frac_nvda) * datos["CLP=X"]
df_grafico = pd.DataFrame({"Valor Cartera (CLP)": historial_clp, "Inversión Inicial": inversion_clp})
st.line_chart(df_grafico)
