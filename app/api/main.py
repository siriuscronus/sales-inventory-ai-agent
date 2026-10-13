from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.agent.orchestrator import run_agent


# ---------------------------------------------------------
# Aplicación FastAPI
# ---------------------------------------------------------

app = FastAPI(
    title="Piedmont Metals Sales & Inventory AI Agent",
    description=(
        "API académica para consultas de ventas, "
        "inventario y conocimiento documental."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------
# Modelos de entrada
# ---------------------------------------------------------

class AgentRequest(BaseModel):
    """
    Solicitud enviada al agente.
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Consulta del usuario.",
    )


# ---------------------------------------------------------
# Endpoint raíz
# ---------------------------------------------------------

@app.get("/")
def root():
    """
    Información básica del servicio.
    """

    return {
        "service": (
            "Piedmont Metals Sales & Inventory AI Agent"
        ),
        "version": "1.0.0",
        "status": "running",
    }


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():
    """
    Permite comprobar si la API está funcionando.
    """

    return {
        "status": "healthy",
    }


# ---------------------------------------------------------
# Endpoint principal del agente
# ---------------------------------------------------------

@app.post("/agent")
def ask_agent(request: AgentRequest):
    """
    Envía una consulta al AI Agent.

    El flujo interno incluye:

    1. Security Gateway.
    2. Tools.
    3. RAG.
    4. Gemini.
    """

    result = run_agent(
        request.query
    )

    # -----------------------------------------------------
    # Entrada bloqueada por seguridad
    # -----------------------------------------------------

    security = result.get(
        "security",
        {},
    )

    if not security.get(
        "allowed",
        True,
    ):
        raise HTTPException(
            status_code=400,
            detail={
                "message": (
                    "La consulta fue bloqueada por "
                    "los controles de seguridad."
                ),
                "issues": security.get(
                    "issues",
                    [],
                ),
            },
        )

    # -----------------------------------------------------
    # Respuesta del agente
    # -----------------------------------------------------

    return result