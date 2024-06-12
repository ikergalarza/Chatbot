import streamlit as st
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import json


# Con cargar el entorno y que esté la clave de API ahí ya parece que vale para lanzar el modelo de OpenAi
load_dotenv(".env")

print(os.getenv("OPENAI_API_KEY"))

llm = ChatOpenAI(model = "gpt-4o", temperature = 0)

st.title("ChatBot Neety")

messages = []

# Inicializar el historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Cargar el historial de conversación desde un archivo
history_file = "conversation_history.json"
try:
    with open(history_file, "r") as file:
        messages = json.load(file)
except FileNotFoundError:
    print("El archivo no se encontró.")
except json.decoder.JSONDecodeError:
    print("El archivo no contiene un JSON válido.")

# Mostrar mensajes de chat del historial al recargar la app
for message in messages: # se recorre todos los mensajes de la session state
    if message != messages[0]:
        with st.chat_message(message[0]): #para cada rol le metemos el contenido del mensaje
            st.markdown(message[1])


# Reaccionar a la entrada del usuario // si el usuario pone algo se rellena el prompt y empiezas a reaccionar con el chat
if prompt := st.chat_input("Escribe tu mensaje..."): 
    # Mostrar mensaje del usuario en el contenedor de mensajes del chat
    st.chat_message("user").markdown(prompt) # se muestra en en el chat el mensaje que se ha introducido por el usuario
    # Agregar mensaje del usuario al historial del chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    messages.append(["human", prompt])

    response = llm.invoke(messages).content
    # Mostrar respuesta del asistente en el contenedor de mensajes de chat
    with st.chat_message("assistant"):
        st.markdown(response) # con esto se muestra la respuesta del assistant
    # Agregar respuesta del asistente al historial del chat
    st.session_state.messages.append({"role": "assistant", "content": response})
    messages.append(["assistant", response])
    
    # Guardar el historial de conversación en el archivo
    with open(history_file, "w") as file:
        json.dump(messages, file)

print(st.session_state.messages)
print(messages)