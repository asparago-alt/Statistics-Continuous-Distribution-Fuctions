# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 10:40:29 2026

@author: alexs
"""

# -*- coding: utf-8 -*-
import streamlit as st
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calcolatore Statistico Pro", layout="centered")

st.title("📊 Calcolatore Statistico Universale")

# --- SIDEBAR: CONFIGURAZIONE ---
st.sidebar.header("Impostazioni")
dist_choice = st.sidebar.selectbox("1. Scegli la Distribuzione:", 
                                   ["Normale", "Esponenziale", "T di Student", "Chi-Quadro"])

calc_mode = st.sidebar.radio("2. Tipo di Calcolo:", 
                             ["Minore di (X < x)", "Intervallo (x1 < X < x2)"])

# --- LOGICA DISTRIBUZIONI ---
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
    x_plot = np.linspace(0, dist.ppf(0.99), 500)

st.divider()

# --- INPUT E CALCOLO ---
if calc_mode == "Minore di (X < x)":
    x_val = st.number_input("Inserisci il valore x:", value=float(np.median(x_plot)))
    prob = dist.cdf(x_val)
    label_res = f"P(X < {x_val:.2f})"
    x_fill_min, x_fill_max = x_plot[0], x_val
else:
    col1, col2 = st.columns(2)
    with col1:
        x1 = st.number_input("Limite Inferiore (x1)", value=float(x_plot[250]))
    with col2:
        x2 = st.number_input("Limite Superiore (x2)", value=float(x_plot[350]))
    prob = dist.cdf(x2) - dist.cdf(x1)
    label_res = f"P({x1:.2f} < X < {x2:.2f})"
    x_fill_min, x_fill_max = x1, x2

# --- RISULTATO E GRAFICO ---
st.metric(label=f"Probabilità {label_res}", value=f"{prob:.4f}")

fig, ax = plt.subplots()
ax.plot(x_plot, dist.pdf(x_plot), 'b-', lw=2)

# Colora l'area corretta
px = np.linspace(max(x_fill_min, x_plot[0]), min(x_fill_max, x_plot[-1]), 100)
ax.fill_between(px, dist.pdf(px), color='skyblue', alpha=0.5)

ax.set_ylim(bottom=0)
st.pyplot(fig)
