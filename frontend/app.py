import requests
import streamlit as st


# ---------------------------------------------------------
# Configuración
# ---------------------------------------------------------

API_BASE_URL = "http://127.0.0.1:8000"
API_URL = f"{API_BASE_URL}/agent"
HEALTH_URL = f"{API_BASE_URL}/health"

st.set_page_config(
    page_title="Piedmont Metals | Asistente IA",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------
# Estilos visuales
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1400px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .pm-hero {
            padding: 1.4rem 1.6rem;
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 18px;
            margin-bottom: 1rem;
        }

        .pm-hero h1 {
            margin: 0;
            font-size: 2rem;
        }

        .pm-hero p {
            margin: 0.45rem 0 0 0;
            opacity: 0.78;
            font-size: 1rem;
        }

        .pm-section-title {
            font-size: 1.05rem;
            font-weight: 700;
            margin-top: 0.3rem;
            margin-bottom: 0.8rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 14px;
            padding: 0.85rem 1rem;
        }

        div[data-testid="stChatMessage"] {
            border-radius: 14px;
            padding: 0.2rem 0.4rem;
        }

        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.16);
        }

        .pm-footer {
            opacity: 0.65;
            font-size: 0.82rem;
            text-align: center;
            margin-top: 1.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Utilidades
# ---------------------------------------------------------

def api_is_available() -> bool:
    """Comprueba rápidamente si FastAPI está disponible."""

    try:
        response = requests.get(
            HEALTH_URL,
            timeout=2,
        )
        return response.status_code == 200
    except requests.RequestException:
        return False


def reset_conversation() -> None:
    """Restaura la conversación inicial."""

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "¡Hola! Soy el asistente de ventas e inventario. "
                "Puedo ayudarle con inventario, precios, productos, "
                "cotizaciones y procedimientos."
            ),
        }
    ]


# ---------------------------------------------------------
# Estado de sesión
# ---------------------------------------------------------

if "messages" not in st.session_state:
    reset_conversation()


# ---------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------

suggested_query = None
api_online = api_is_available()

with st.sidebar:
    st.title("Piedmont Metals")
    st.caption("Asistente IA de Ventas e Inventario")

    st.divider()

    st.subheader("Estado del sistema")

    if api_online:
        st.success("FastAPI conectado")
    else:
        st.error("FastAPI no disponible")

    st.caption(
        f"Backend: {API_BASE_URL}"
    )

    st.divider()

    st.subheader("Consultas sugeridas")

    if st.button(
        "📦 Consultar inventario",
        use_container_width=True,
    ):
        suggested_query = (
            "¿Cuántas unidades tenemos del SKU IJOIST-16-20?"
        )

    if st.button(
        "💲 Consultar precio",
        use_container_width=True,
    ):
        suggested_query = (
            "¿Cuál es el precio del SKU IJOIST-16-20?"
        )

    if st.button(
        "🧾 Crear cotización",
        use_container_width=True,
    ):
        suggested_query = (
            "Cotiza 20 unidades del SKU IJOIST-16-20."
        )

    if st.button(
        "📚 Consultar procedimiento",
        use_container_width=True,
    ):
        suggested_query = (
            "¿Qué procedimiento debemos seguir si "
            "no hay suficiente inventario?"
        )

    st.divider()

    if st.button(
        "🗑️ Limpiar conversación",
        use_container_width=True,
    ):
        reset_conversation()
        st.rerun()

    st.divider()

    st.caption(
        "Prototipo académico. Los datos, precios, "
        "cantidades y procedimientos utilizados son ficticios."
    )


# ---------------------------------------------------------
# Encabezado principal
# ---------------------------------------------------------

st.markdown(
    """
    <div class="pm-hero">
        <h1>Asistente IA de Ventas e Inventario</h1>
        <p>
            Consulta productos, precios, disponibilidad, cotizaciones
            y conocimiento operativo desde una sola interfaz.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Indicadores del prototipo
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "API",
        "Activa" if api_online else "Inactiva",
    )

with col2:
    st.metric(
        "Herramientas",
        "6",
    )

with col3:
    st.metric(
        "Pruebas",
        "13/13",
    )

with col4:
    st.metric(
        "Arquitectura",
        "RAG + MCP",
    )

st.divider()


# ---------------------------------------------------------
# Área de conversación
# ---------------------------------------------------------

st.markdown(
    '<div class="pm-section-title">Asistente conversacional</div>',
    unsafe_allow_html=True,
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        model = message.get("model")
        if model:
            st.caption(
                f"Modelo utilizado: {model}"
            )


# ---------------------------------------------------------
# Entrada del usuario
# ---------------------------------------------------------

typed_query = st.chat_input(
    "Escriba su consulta sobre ventas, inventario o procedimientos..."
)

user_query = suggested_query or typed_query


if user_query:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_query)

    answer = (
        "No se recibió una respuesta."
    )
    model = None

    with st.chat_message("assistant"):
        with st.spinner(
            "Analizando la consulta..."
        ):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "query": user_query,
                    },
                    timeout=60,
                )

                if response.status_code == 200:
                    data = response.json()

                    answer = data.get(
                        "answer",
                        "No se recibió una respuesta.",
                    )

                    model = data.get("model")

                    st.markdown(answer)

                    if model:
                        st.caption(
                            f"Modelo utilizado: {model}"
                        )

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

                else:
                    answer = (
                        "El backend respondió con un error "
                        f"HTTP {response.status_code}."
                    )

                    st.error(answer)

            except requests.exceptions.ConnectionError:
                answer = (
                    "No se pudo conectar con FastAPI. "
                    "Verifique que el backend esté ejecutándose "
                    f"en {API_BASE_URL}."
                )

                st.error(answer)

            except requests.exceptions.Timeout:
                answer = (
                    "La consulta tardó demasiado tiempo "
                    "en responder."
                )

                st.error(answer)

            except Exception as exc:
                answer = (
                    "Ocurrió un error inesperado "
                    "al procesar la consulta."
                )

                st.error(answer)

                print(
                    f"Error frontend: {exc}"
                )

    assistant_message = {
        "role": "assistant",
        "content": answer,
    }

    if model:
        assistant_message["model"] = model

    st.session_state.messages.append(
        assistant_message
    )


# ---------------------------------------------------------
# Pie de página
# ---------------------------------------------------------

st.markdown(
    """
    <div class="pm-footer">
        Piedmont Metals Sales & Inventory AI Agent ·
        Prototipo académico con FastAPI, RAG, Qdrant, Gemini y MCP
    </div>
    """,
    unsafe_allow_html=True,
)
