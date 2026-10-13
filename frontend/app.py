import requests
import streamlit as st


# ---------------------------------------------------------
# Configuración
# ---------------------------------------------------------

API_URL = "http://127.0.0.1:8000/agent"

st.set_page_config(
    page_title="Piedmont Metals AI Agent",
    page_icon="🤖",
    layout="centered",
)


# ---------------------------------------------------------
# Encabezado
# ---------------------------------------------------------

st.title(
    "🤖 Piedmont Metals Sales & Inventory AI Agent"
)

st.caption(
    "Prototipo académico de agente IA para consultas "
    "de ventas, inventario y conocimiento documental."
)

st.divider()


# ---------------------------------------------------------
# Estado de la conversación
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "¡Hola! Soy el agente de ventas e inventario. "
                "Puedo ayudarle a consultar inventario, precios, "
                "cotizaciones y procedimientos."
            ),
        }
    ]


# ---------------------------------------------------------
# Mostrar historial
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# Entrada del usuario
# ---------------------------------------------------------

user_query = st.chat_input(
    "Escriba su consulta..."
)


if user_query:

    # -----------------------------------------------------
    # Mostrar mensaje del usuario
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    # -----------------------------------------------------
    # Llamar FastAPI
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Consultando inventario y conocimiento..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "query": user_query,
                    },
                    timeout=60,
                )

                # -----------------------------------------
                # Respuesta exitosa
                # -----------------------------------------

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No se recibió una respuesta.",
                    )

                    st.markdown(answer)

                    model = data.get("model")

                    if model:
                        st.caption(
                            f"Modelo utilizado: {model}"
                        )

                # -----------------------------------------
                # Entrada bloqueada por seguridad
                # -----------------------------------------

                elif response.status_code == 400:

                    data = response.json()

                    detail = data.get(
                        "detail",
                        {},
                    )

                    answer = detail.get(
                        "message",
                        "La consulta fue bloqueada.",
                    )

                    st.warning(answer)

                # -----------------------------------------
                # Otros errores HTTP
                # -----------------------------------------

                else:

                    answer = (
                        "El backend respondió con un error "
                        f"HTTP {response.status_code}."
                    )

                    st.error(answer)

            # ---------------------------------------------
            # FastAPI no disponible
            # ---------------------------------------------

            except requests.exceptions.ConnectionError:

                answer = (
                    "No se pudo conectar con el backend. "
                    "Verifique que FastAPI esté ejecutándose "
                    "en http://127.0.0.1:8000."
                )

                st.error(answer)

            # ---------------------------------------------
            # Timeout
            # ---------------------------------------------

            except requests.exceptions.Timeout:

                answer = (
                    "La consulta tardó demasiado tiempo "
                    "en responder."
                )

                st.error(answer)

            # ---------------------------------------------
            # Error inesperado
            # ---------------------------------------------

            except Exception as exc:

                answer = (
                    "Ocurrió un error inesperado "
                    "al procesar la consulta."
                )

                st.error(answer)

                print(
                    f"Error frontend: {exc}"
                )

    # -----------------------------------------------------
    # Guardar respuesta en historial
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )


# ---------------------------------------------------------
# Información lateral
# ---------------------------------------------------------

with st.sidebar:

    st.header(
        "Acerca del prototipo"
    )

    st.write(
        "Este agente académico combina:"
    )

    st.markdown(
        """
        - **FastAPI**
        - **SQLite**
        - **Tools**
        - **RAG**
        - **Qdrant**
        - **Embeddings**
        - **Gemini**
        - **Security Guardrails**
        """
    )

    st.divider()

    st.caption(
        "Datos y procedimientos utilizados "
        "exclusivamente con fines académicos."
    )