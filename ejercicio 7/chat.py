import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# Estilos (omitted for brevity, assume it's still there)
st.markdown("""
<style>
body {
    background-color: white;
    color: #064635;
}
h1, h2, h3 {
    color: #046a38;
}
div.stButton > button {
    border-radius: 5px;
    background-color: #046a38;
    color: white;
    padding: 8px 16px;
    border: none;
}
div.stButton > button:hover {
    background-color: #064635;
}
input, textarea {
    border: 2px solid #046a38 !important;
    color: #064635 !important;
}
</style>
""", unsafe_allow_html=True)

# Initialize Gemini client with key from secrets.toml
# Ensure your secrets.toml has 'GEMINI_API_KEY'
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# --- CRITICAL NEW MODEL SELECTION LOGIC WITH MORE DEBUGGING ---
MODEL_NAME = ''
model = None # Initialize model to None

try:
    # First, try to initialize with the most recommended model directly
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        MODEL_NAME = 'gemini-1.5-flash'
        st.success(f"DEBUG: Successfully initialized with model: {MODEL_NAME}")
    except Exception as e_flash:
        st.warning(f"DEBUG: Failed to initialize 'gemini-1.5-flash': {e_flash}")
        st.info("DEBUG: Listing all available models to find an alternative...")

        available_models_info = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models_info.append(m.name)
        
        st.write(f"DEBUG: Models found supporting 'generateContent': {available_models_info}")

        if 'gemini-pro' in available_models_info:
            model = genai.GenerativeModel('gemini-pro')
            MODEL_NAME = 'gemini-pro'
            st.success(f"DEBUG: Successfully initialized with fallback model: {MODEL_NAME}")
        elif 'gemini-1.5-pro' in available_models_info: # Try 1.5 Pro if gemini-pro isn't there but 1.5 Pro is
            model = genai.GenerativeModel('gemini-1.5-pro')
            MODEL_NAME = 'gemini-1.5-pro'
            st.success(f"DEBUG: Successfully initialized with fallback model: {MODEL_NAME}")
        else:
            st.error("ERROR: Neither 'gemini-1.5-flash', 'gemini-pro', nor 'gemini-1.5-pro' are available for your API key. Cannot proceed.")
            st.stop()

    if not model: # Should not happen if previous logic is correct, but as a safeguard
        st.error("ERROR: No valid Gemini model could be initialized. Please check your API key and access rights.")
        st.stop()

except Exception as e_main:
    st.error(f"FATAL ERROR during Gemini model setup: {e_main}. Please ensure your API key is correct in .streamlit/secrets.toml and try again.")
    st.stop()


# Cargar base de datos (rest of your code, omitted for brevity)
CSV_FILE = "fase5.csv"
if os.path.exists(CSV_FILE):
    dt = pd.read_csv(CSV_FILE, encoding="latin1")
    dt.columns = dt.columns.str.strip().str.lower()
    if 'contrase\u00f1a' in dt.columns:
        dt = dt.rename(columns={'contrase\u00f1a': 'contrasena'})
    if 'g\u00e9nero' in dt.columns:
        dt = dt.rename(columns={'g\u00e9nero': 'genero'})
else:
    dt = pd.DataFrame(columns=["correo", "nombre", "contrasena", "genero"])

# Estado de sesión (omitted for brevity)
if "sesionIniciada" not in st.session_state:
    st.session_state.sesionIniciada = False
if "correo" not in st.session_state:
    st.session_state.correo = ""
if "nombre" not in st.session_state:
    st.session_state.nombre = ""
if "genero" not in st.session_state:
    st.session_state.genero = ""
if "intentos_login" not in st.session_state:
    st.session_state.intentos_login = 0

MAX_INTENTOS = 5

# Funciones de autenticación (omitted for brevity)
def iniciarSesion(correoInput, clave):
    correo = correoInput + "@uvg"
    encontrado = False
    for i in range(len(dt)):
        if dt["correo"][i] == correo and dt["contrasena"][i] == clave:
            st.session_state.nombre = dt["nombre"][i]
            st.session_state.genero = dt["genero"][i]
            st.session_state.correo = correo
            st.session_state.sesionIniciada = True
            st.session_state.intentos_login = 0
            encontrado = True
            break
    if not encontrado:
        st.session_state.intentos_login += 1
        if st.session_state.intentos_login >= MAX_INTENTOS:
            st.error(f"Has superado el número máximo de intentos ({MAX_INTENTOS}). Intenta más tarde.")
        else:
            intentos_restantes = MAX_INTENTOS - st.session_state.intentos_login
            st.error(f"Correo o contraseña incorrectos. Te quedan {intentos_restantes} intentos.")
    return encontrado

def registrarse(correoInput, clave, nombre, genero):
    global dt
    correo = correoInput + "@uvg"
    if correo in dt["correo"].values:
        return False
    nuevaFila = {
        "correo": correo,
        "nombre": nombre,
        "contrasena": clave,
        "genero": genero
    }
    dt = pd.concat([dt, pd.DataFrame([nuevaFila])], ignore_index=True)
    dt.to_csv(CSV_FILE, index=False, encoding="latin1")
    st.session_state.correo = correo
    st.session_state.nombre = nombre
    st.session_state.genero = genero
    st.session_state.sesionIniciada = True
    st.session_state.intentos_login = 0
    return True

def protocolo():
    st.write("\n=== Protocolo de Relajación ===")
    st.write("1. Inhala por la nariz durante 3 segundos")
    st.write("2. Mantén el aire durante 5 segundos")
    st.write("3. Exhala lentamente por la boca")
    st.write("4. Repite este proceso 3 veces o hasta sentirte mejor\n")

def botonEmergencia():
    st.write("\n=== BOTÓN DE EMERGENCIA ===")
    st.write("Este botón es para casos de crisis emocional grave.")
    opcion = st.radio("Elige una opción:", ["1. Sí, necesito ayuda urgente.", "2. No, volver al menú principal."])
    if opcion.startswith("1"):
        st.write("\nBOTÓN DE EMERGENCIA ACTIVADO")
        st.write("Conectándote con apoyo emocional de la UVG...")
        st.write("✉️ bienestar@uvg.edu.gt")
        st.write("📞 Teléfono de atención emocional (24/7)")
        st.write("🏡 Oficina de Apoyo Emocional, Campus Central")
        st.success("Estamos contigo ❤️")
    else:
        st.write("Regresando al menú...")

def chatConExpertos():
    st.title(f"Chat con Expertos (Impulsado por {MODEL_NAME})") # Display the actual model name

    if "chat_messages" not in st.session_state:
        # Initialize chat_messages with a user message to set the persona for Gemini
        st.session_state.chat_messages = [
            {"role": "user", "content": "Eres un terapeuta amable y empático que ofrece apoyo emocional."}
        ]

    # Display chat messages from history
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        elif msg["role"] == "model":
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    if prompt := st.chat_input("¿Cómo te sientes hoy?"):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            # Prepare messages for Gemini
            gemini_messages = []
            for msg in st.session_state.chat_messages:
                gemini_messages.append({'role': 'user' if msg['role'] == 'user' else 'model', 'parts': [msg['content']]})

            # Call the model
            response = model.generate_content(gemini_messages)

            reply = response.text
            st.session_state.chat_messages.append({"role": "model", "content": reply})

            with st.chat_message("assistant"):
                st.markdown(reply)

        except Exception as e:
            st.error(f"Error al contactar con Gemini: {e}")
            # st.exception(e) # Uncomment to see the full traceback for debugging

# Interfaz principal (rest of your code, omitted for brevity)
st.title("Programa de Ayuda Psicológica")

if not st.session_state.sesionIniciada:
    st.subheader("=== Menú de Inicio ===")
    menuInicio = st.radio("Elige una opción:", ["1. Iniciar sesión", "2. Registrarse"])
    correoInput = st.text_input("Correo (sin @uvg):")
    clave = st.text_input("Contraseña:", type="password")
    if menuInicio == "2. Registrarse":
        nombre = st.text_input("Nombre:")
        genero = st.radio("Género:", ["masculino", "femenino"])
        if st.button("Registrarse"):
            if registrarse(correoInput, clave, nombre, genero):
                saludo = "Bienvenida" if genero == "femenino" else "Bienvenido"
                st.success(f"Registro exitoso. ¡{saludo}, {nombre}!")
            else:
                st.error("Ese correo ya está registrado.")
    else:
        if st.session_state.intentos_login < MAX_INTENTOS:
            if st.button("Iniciar sesión"):
                if iniciarSesion(correoInput, clave):
                    saludo = "Bienvenido" if st.session_state.genero == "masculino" else "Bienvenida"
                    st.success(f"\n{saludo} {st.session_state.nombre}!! Has ingresado con el correo ({st.session_state.correo})")
        else:
            st.error(f"Has superado el número máximo de intentos ({MAX_INTENTOS}). Intenta más tarde.")
else:
    st.sidebar.write(f"{st.session_state.nombre}, selecciona una opción:")
    opcion = st.sidebar.radio("=== Menú Principal ===", ["1. Chat con Expertos", "2. Botón de Emergencia", "3. Protocolo", "4. Cerrar sesión", "5. Salir del programa"])
    if opcion.startswith("1"):
        chatConExpertos()
    elif opcion.startswith("2"):
        botonEmergencia()
    elif opcion.startswith("3"):
        protocolo()
    elif opcion.startswith("4"):
        if st.button("¿Deseas cerrar sesión?"):
            st.session_state.sesionIniciada = False
            st.session_state.intentos_login = 0
            st.success("Sesión cerrada.")
    elif opcion.startswith("5"):
        st.write(f"Gracias por usar el programa, {st.session_state.nombre}. ¡Que tengas un buen día!")
        st.session_state.sesionIniciada = False
        st.session_state.intentos_login = 0