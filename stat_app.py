# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 10:40:29 2026

@author: alexs
"""

import streamlit as st
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# Forza l'uso di UTF-8 per evitare errori di codifica
st.set_page_config(page_title="Calcolatore Statistico", layout="centered")

st.title("📊 Calcolatore di Probabilità")
st.write("Calcola l'area sotto la curva: $P(x_1 < X < x_2)$")

# 1. Scelta della distribuzione (Aggiunta Chi-Quadro)
dist_choice = st.sidebar.selectbox("Scegli la Distribuzione:", 
                                   ["Normale", "Esponenziale", "T di Student", "Chi-Quadro"])

# Inizializziamo le variabili per il calcolo
prob = 0.0

if dist_choice == "Normale":
    mu = st.number_input("Media (μ)", value=64.5)
    sigma = st.number_input("Deviazione Standard (σ)", value=2.4, min_value=0.01)
    dist = stats.norm(loc=mu, scale=sigma)
    x_range = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)

elif dist_choice == "Esponenziale":
    lam = st.number_input("Lambda (λ)", value=1.0, min_value=0.01)
    dist = stats.expon(scale=1/lam)
    x_range = np.linspace(0, dist.ppf(0.99), 500)

elif dist_choice == "T di Student":
    df_t = st.number_input("Gradi di Libertà (v)", value=10, min_value=1)
    dist = stats.t(df=df_t)
    x_range = np.linspace(-4, 4, 500)

elif dist_choice == "Chi-Quadro":
    df_chi = st.number_input("Gradi di Libertà (k)", value=5, min_value=1)
    dist = stats.chi2(df=df_chi)
    # La Chi-Quadro parte da 0, definiamo un range fino al 99° percentile per visibilità
    x_range = np.linspace(0, dist.ppf(0.99), 500)

# 2. Input Intervallo
st.divider()
col1, col2 = st.columns(2)
with col1:
    # Impostiamo il valore di default basandoci sul range calcolato
    x1 = st.number_input("Limite Inferiore (x1)", value=float(x_range[0]))
with col2:
    x2 = st.number_input("Limite Superiore (x2)", value=float(x_range[-1]))

# 3. Calcolo della Probabilità (Differenza tra CDF)
prob = dist.cdf(x2) - dist.cdf(x1)

# Visualizzazione Risultato
st.metric(label=f"Probabilità P({x1} < X < {x2})", value=f"{prob:.4f}")

# 4. Grafico
fig, ax = plt.subplots()
y = dist.pdf(x_range)
ax.plot(x_range, y, 'r-', lw=2, label='PDF')

# Area colorata (con clip per evitare valori fuori range nelle distribuzioni limitate)
px = np.linspace(max(x1, x_range[0]), min(x2, x_range[-1]), 100)
ax.fill_between(px, dist.pdf(px), color='red', alpha=0.3, label='Area probabilità')

ax.set_title(f"Distribuzione {dist_choice}")
ax.set_ylim(bottom=0)
ax.legend()
st.pyplot(fig)

#$env:PYTHONUTF8=1; py -m streamlit run "C:\Users\alexs\Desktop\PYTHON\stat_app.py"$env:PYTHONUTF8=1; py -m streamlit run "C:\Users\alexs\Desktop\PYTHON\stat_app.py"