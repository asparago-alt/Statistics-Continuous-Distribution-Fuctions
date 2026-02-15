# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 11:40:05 2026

@author: alexs
"""

# -*- coding: utf-8 -*-
import streamlit as st
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calcolatore Statistico", layout="centered")

st.title("📊 Calcolatore di Probabilità (P < x)")

# Sidebar per la scelta della distribuzione - AGGIUNTA CHI QUADRO
dist_choice = st.sidebar.selectbox("Distribuzione:", ["Normale", "Esponenziale", "T di Student", "Chi-Quadro"])

# Parametri delle distribuzioni
if dist_choice == "Normale":
    mu = st.number_input("Media (μ)", value=64.5)
    sigma = st.number_input("Deviazione Standard (σ)", value=2.4, min_value=0.01)
    dist = stats.norm(loc=mu, scale=sigma)
    x_plot = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)

elif dist_choice == "Esponenziale":
    lam = st.number_input("Lambda (λ)", value=1.0, min_value=0.01)
    dist = stats.expon(scale=1/lam)
    x_plot = np.linspace(0, dist.ppf(0.99), 500)

elif dist_choice == "T di Student":
    df_t = st.number_input("Gradi di Libertà (v)", value=10, min_value=1)
    dist = stats.t(df=df_t)
    x_plot = np.linspace(-4, 4, 500)

elif dist_choice == "Chi-Quadro":
    df_chi = st.number_input("Gradi di Libertà (k)", value=5, min_value=1)
    dist = stats.chi2(df=df_chi)
    # La Chi-Quadro parte da 0, definiamo un range sensato fino al 99° percentile
    x_plot = np.linspace(0, dist.ppf(0.99), 500)

st.divider()

# Input per il valore singolo (Minore di X)
default_x = 63.0 if dist_choice == "Normale" else 2.0
x_val = st.number_input(f"Calcola P(X < x) inserendo x:", value=float(default_x))

# Calcolo Probabilità Cumulata
prob = dist.cdf(x_val)

# Risultato
st.metric(label=f"Probabilità P(X < {x_val})", value=f"{prob:.4f}")

# Grafico
fig, ax = plt.subplots()
y_plot = dist.pdf(x_plot)
ax.plot(x_plot, y_plot, 'b-', lw=2)

# Colora l'area a sinistra del valore scelto
# Per distribuzioni che partono da 0 (Esponenziale, Chi-Quadro), limitiamo il riempimento
lower_bound = x_plot[0]
x_fill = np.linspace(lower_bound, x_val, 100)
# Evitiamo di colorare fuori dal grafico se x_val è fuori dal range visibile
x_fill = x_fill[x_fill >= lower_bound] 

ax.fill_between(x_fill, dist.pdf(x_fill), color='skyblue', alpha=0.5, label='Area P(X < x)')

ax.axvline(x_val, color='red', linestyle='--', label=f'x = {x_val}')
ax.set_ylim(bottom=0) # La densità non è mai negativa
ax.legend()
st.pyplot(fig)

#$env:PYTHONUTF8=1; py -m streamlit run "C:\Users\alexs\Desktop\PYTHON\static_cont.py"$env:PYTHONUTF8=1; py -m streamlit run "C:\Users\alexs\Desktop\PYTHON\statistic_cont.py"