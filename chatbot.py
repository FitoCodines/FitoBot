import streamlit as st
from groq import Groq
st.set_page_config(page_title="ChatBot", page_icon="😎")

st.title("FitoBot")

nombre = st.text_input("Cual es tu nombre?")

if st.button("Saludar"):
    st.write(f"Hola, {nombre}. Habla conmigo escribiendome un mensaje en la barra de abajo!")
    

modelos = ['llama3-8b-8192', 'llama3-70b-8192', 'gemma2-9b-it']

def configurarPagina():
    st.title("Habla con FitoBot")
    st.sidebar.title("Configurá la IA")
    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=modelos, index = 0)
    st.sidebar.text("El mensaje de la IA varía según el modelo que le pongas.")
    return elegirModelo

def ConectarGroq():
    claveSecreta = st.secrets["claveApi"]
    return Groq(api_key=claveSecreta)
def ConfigurarModelo(cliente, modelo, mensajeDeEntrada):
    instrucciones = {
        "role": "system",
        "content": (
            "Sos FitoBot, un asistente empático, confiable y claro. "
            "Siempre respondés con calidez, siendo útil, humano y honesto. "
            "No inventás información, y si no sabés algo, lo decís con amabilidad. "
            "Tu objetivo es ayudar a las personas de forma amable, sin hacer suposiciones peligrosas. "
            "Usá un lenguaje natural, cercano y sin sonar como un robot."
        )
    }

    mensaje_usuario = {"role": "user", "content": mensajeDeEntrada}

    return cliente.chat.completions.create(
        model=modelo,
        messages=[instrucciones, mensaje_usuario],
        stream=True
    )
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido,avatar):
    st.session_state.mensajes.append({"role":rol, "content":contenido, "avatar":avatar})


def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])


def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat: 
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

def main(): 


    modelo = configurarPagina()
    clienteUsuario = ConectarGroq()
    inicializar_estado()
    mensaje = st.chat_input("Escribi tu mensaje")
    area_chat()
    if mensaje:
        actualizar_historial("user", mensaje,"😁")

        chat_completo = ConfigurarModelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")

            st.rerun()
if __name__ == "__main__":
    main()


