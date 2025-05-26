'''
Algoritmos y programación básica
Ejercicio 7 - Streamlit
Milena Rodríguez 251027
18 de mayo del 2025
'''

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


with st.sidebar:
    st.title("¡Gladiadores!")
    st.divider()
    
    menu = ["Cargar Archivo", "Análisis exploratorio", "Indicadores", "Gráficas"]
    opcion = st.radio("Opciones", menu)
    
    
    
if opcion == "Cargar Archivo":
    st.header("📜️Archivo")
    
    st.divider()
    archivo = st.file_uploader("Escoja el archivo que desee subir", "csv")
    st.session_state
    
    if archivo is not None:
        datos = pd.read_csv(archivo)
        st.session_state["datos"] = datos
        st.dataframe(st.session_state["datos"])
        
        
        
elif opcion == "Análisis exploratorio":
    st.header("🏛️Análisis exploratorio")
    st.divider()
    
    if "datos" in st.session_state:
        datos = st.session_state["datos"]
        st.write("Filas y columnas:", datos.shape)
    else:
        st.warning("Primero sube un archivo en la opción 'Cargar Archivo'.")
        
    analisis = datos.columns.tolist()
    with st.expander("Datos disponibles"):
        for columna in analisis:
            st.write("-", columna)
            
    with st.expander("Primeras filas"):
        st.write(datos.head(10))
        
    with st.expander("Estadísticas generales"):  
        st.dataframe(datos.describe())
        
        
        
        
elif opcion == "Indicadores":
    st.header("Indicadores importantes")
    st.divider()
    
    if "datos" in st.session_state:
        datos = st.session_state["datos"]

        total = len(datos)
        sobrevivientes = datos["Survived"].sum()
        porcentaje = (sobrevivientes / total) * 100
        
        st.subheader("🛡️ Gladiadores que sobrevivieron")
        st.write("**Descripción:** porcentaje de gladiadores que han sobrevivido a las batallas.")
        st.write("**Justificación:** esta información es relevante pues indica el nivel de las batallas a las que se enfrentan los gladiadores. Ayuda a preparar estrategias y equipos, y compararlos con batallas anteriores para ver las mejores y aspectos a mejorar.")
        st.write("**Método:** se suma la cantidad de gladiadores que tienen el valor 'True' en la casilla de sobrevivencia y se divide entre la cantidad total de gladiadores. Luego, se multiplica por 100 para obtener el porcentaje final.")
        st.metric("Porcentaje de supervivencia", f"{porcentaje:.2f}%")        
        
        
        st.divider()
        

        total = len(datos)
        
        st.subheader("❤️‍🩹️ Salud del equipo")
        st.write("**Descripción:** indica el estado que tiene el equipo de salud para saber su condición para luchar.")
        st.write("**Justificación:** el estado de salud del equipo ayuda a predecir el desempeño que podrían tener los gladidadores si se enfentraran a una batalla en el momento.")
        st.write("**Método:** se suma la cantidad de 'Excelente', 'Bueno' y 'Regular' en la columna 'Health Status'. Luego, se divide la cantidad de cada uno por el total de gladiadores y se multiplican por 100 para obtener el porcentaje final.")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            cantidad = (datos["Health Status"] == "Excellent").sum()
            porcentaje = (cantidad / total) * 100
            st.metric("Excelente", f"{porcentaje:.2f}%")

        with col2:
            cantidad = (datos["Health Status"] == "Good").sum()
            porcentaje = (cantidad / total) * 100
            st.metric("Bueno", f"{porcentaje:.2f}%")

        with col3:
            cantidad = (datos["Health Status"] == "Fair").sum()
            porcentaje = (cantidad / total) * 100
            st.metric("Regular", f"{porcentaje:.2f}%")
        
        
        st.divider()
        
        
        st.subheader("⚔️️ Luchadores más experimentados")
        st.write("**Descripción:** luchadores con mayor cantidad de experiencia en combate.")
        st.write("**Justificación:** la experiencia es clave para determinar estrategias y asignar posiciones y cargos en el campo de batalla.")
        st.write("**Método:** se ordena la columna de 'Battle Experience' de forma descendente y se toman los primeros 5 datos.")
        
        top5 = datos.sort_values("Battle Experience", ascending=False).head(5)

        for i in range(5):
            nombre = top5.iloc[i]["Name"]
            experiencia = top5.iloc[i]["Battle Experience"]
            st.metric(f"Top {i+1}", f"{nombre} ({experiencia} puntos)")
            
            
        st.divider()
        
            
        st.subheader("🩸️Luchadores con más victorias")
        st.write("**Descripción:** luchadores que más batallas hayan ganado.")
        st.write("**Justificación:** además de la experiencia en batalla, es importante saber qué gladiadores tienen mayor posibilidad de ganar la batalla basado en cuántas batallas hayan ganado en el pasado.")
        st.write("**Método:** se ordena la columna de 'Wins' de forma descendente y se toman los primeros 5 datos.")
        
        top5_victorias = datos.sort_values("Wins", ascending=False).head(5)

        for i in range(5):
            nombre = top5_victorias.iloc[i]["Name"]
            victorias = top5_victorias.iloc[i]["Wins"]
            st.metric(f"Top {i+1}", f"{nombre} ({victorias} victorias)")
            
            
        st.divider()
        
        
        total = len(datos)
        
        st.subheader("🧠️ Estrategias de batalla")
        st.write("**Descripción:** indica los porcentajes de las estrategias de batalla|.")
        st.write("**Justificación:** esta información es relevante para organizar estrategias y posiciones en el campo de batalla. Por ejemplo, se puede poner a los gladiadores defensivos en frente, o los balanceados en el medio.")
        st.write("**Método:** se suma la cantidad de 'Balanceado', 'Agresivo' y 'Defensivo' en la columna 'Battle Strategy'. Luego, se divide la cantidad de cada uno por el total de gladiadores y se multiplican por 100 para obtener el porcentaje final.")
        
        col1, col2, col3 = st.columns(3)

        with col1:
            cantidad = (datos["Battle Strategy"] == "Balanced").sum()
            porcentaje = (cantidad / total) * 100
            st.metric("Balanceado", f"{porcentaje:.2f}%")

        with col2:
            cantidad = (datos["Battle Strategy"] == "Aggressive").sum()
            porcentaje = (cantidad / total) * 100
            st.metric("Agresivo", f"{porcentaje:.2f}%")

        with col3:
            cantidad = (datos["Battle Strategy"] == "Defensive").sum()
            porcentaje = (cantidad / total) * 100
            st.metric("Defensivo", f"{porcentaje:.2f}%")
        
    else:
        st.warning("Primero sube un archivo en la opción 'Cargar Archivo'.")
        
        
elif opcion == "Gráficas":
    st.header("Gráficas importantes")
    st.divider()
    
    if "datos" in st.session_state:
        datos = st.session_state["datos"]
        
        habilidades = datos["Special Skills"].value_counts()
        
        habilidades.plot(kind = "bar",
                         title = "★️Habilidades especiales de los gladiadores",
                         xlabel = "Habilidad",
                         ylabel = "Magnitud",
                         color = "#672e7c")
        
        st.pyplot(plt.gcf())
        
        
        st.divider()
        
        plt.clf()
        armas = datos["Weapon of Choice"].value_counts()
    
        armas.plot(kind="bar",
                   title="⚔︎ Armas preferidas de los gladiadores",
                   xlabel="Arma",
                   ylabel="Cantidad",
                   color="#7c2e3a")
    
        st.pyplot(plt.gcf())
            
            
        st.divider()
        
        
        plt.clf()
        sobrevivientes = datos["Survived"].value_counts()
    
        sobrevivientes.plot.pie(autopct = '%1.1f%%',
                                startangle = 90,
                                labels = ["Sobrevivió", "No sobrevivió"] if True in sobrevivientes.index else ["No sobrevivió", "Sobrevivió"],
                                title = "♡ Gladiadores que sobrevivieron",
                                ylabel = "")
    
        st.pyplot(plt.gcf())
        
        
    else:
        st.warning("Primero sube un archivo en la opción 'Cargar Archivo'.")
    
    
    
    