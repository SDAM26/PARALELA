import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Proyecto Final Parachelas - Simulación de Escalabilidad",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .centered-header {
        text-align: center;  /* Centrar el texto */
        color: #4CAF50;     /* Cambiar color (verde) */
        font-size: 40px;    /* Tamaño de fuente */
        font-weight: bold;  /* Negrita */
    }
    .universe-symbol {
        text-align: center;
        font-size: 100px;    /* Tamaño grande para el emoji */
        margin-bottom: -20px; /* Ajustar espacio */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título centrado con emojis de estrellas y universo
st.markdown('<h2 class="centered-header">✨ Evolución galáctica 🌌</h2>', unsafe_allow_html=True)

st.sidebar.subheader("Carga de datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        data_df = pd.read_csv(uploaded_file)
        st.success("Archivo cargado exitosamente.")
        
        if "N" in data_df.columns and any("P" in col for col in data_df.columns):
            st.subheader("Datos cargados del CSV")
            st.dataframe(data_df, width=1400)

            N_values = data_df["N"].values
            execution_times = {
                int(col.split("P")[1]): data_df[col].values for col in data_df.columns if "P" in col
            }
            P_values = list(execution_times.keys())
            
            speedup = {P: [execution_times[min(P_values)][i] / execution_times[P][i] for i in range(len(N_values))] for P in P_values if P != min(P_values)}
            efficiency = {P: [speedup[P][i] / P for i in range(len(N_values))] for P in speedup.keys()}

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Tiempos de ejecución")
                fig1, ax1 = plt.subplots()
                for P in P_values:
                    ax1.plot(N_values, execution_times[P], label=f"{P} procesos")
                ax1.set_title("Tiempos de ejecución vs Tamaño del problema")
                ax1.set_xlabel("Tamaño del Problema (N)")
                ax1.set_ylabel("Tiempo de Ejecución (s)")
                ax1.legend()
                st.pyplot(fig1)

            with col2:
                st.subheader("Speedup")
                fig2, ax2 = plt.subplots()
                for P in speedup.keys():
                    ax2.plot(N_values, speedup[P], label=f"{P} procesos")
                ax2.set_title("Speedup vs Tamaño del problema")
                ax2.set_xlabel("Tamaño del Problema (N)")
                ax2.set_ylabel("Speedup")
                ax2.legend()
                st.pyplot(fig2)

            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Eficiencia")
                fig3, ax3 = plt.subplots()
                for P in efficiency.keys():
                    ax3.plot(N_values, efficiency[P], label=f"{P} procesos")
                ax3.set_title("Eficiencia vs Tamaño del problema")
                ax3.set_xlabel("Tamaño del Problema (N)")
                ax3.set_ylabel("Eficiencia")
                ax3.legend()
                st.pyplot(fig3)

            with col4:
                st.subheader("Eficiencia por número de procesos")
                fig4, ax4 = plt.subplots()
                for i, N in enumerate([N_values[2], N_values[5], N_values[-1]]):
                    efficiency_per_P = [efficiency[P][i] for P in efficiency.keys()]
                    ax4.plot(efficiency.keys(), efficiency_per_P, marker='o', label=f"N = {int(N)}")
                ax4.set_title("Eficiencia vs Número de procesos")
                ax4.set_xlabel("Número de procesos (P)")
                ax4.set_ylabel("Eficiencia")
                ax4.legend()
                st.pyplot(fig4)

        else:
            st.error("El archivo CSV debe contener una columna 'N' y columnas 'P1', 'P2', etc. con tiempos de ejecución.")
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
