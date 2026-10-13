import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types


# ---------------------------------------------------------
# Configuración
# ---------------------------------------------------------

load_dotenv()

MODELS = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
]


# ---------------------------------------------------------
# Cliente Gemini
# ---------------------------------------------------------

def get_gemini_client() -> genai.Client:
    """
    Crea un cliente Gemini utilizando la API key
    almacenada en el archivo .env.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "No se encontró GEMINI_API_KEY en el archivo .env."
        )

    return genai.Client(api_key=api_key)


# ---------------------------------------------------------
# Generación resiliente
# ---------------------------------------------------------

def generate_response(
    prompt: str,
    system_instruction: str | None = None,
) -> dict:
    """
    Intenta generar una respuesta utilizando los modelos
    Gemini configurados.

    Si todos fallan por indisponibilidad temporal,
    devuelve un resultado controlado en vez de detener
    toda la aplicación.
    """

    client = get_gemini_client()

    config = None

    if system_instruction:
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
        )

    errors_detected = []

    for model_name in MODELS:
        try:
            print(f"Intentando modelo: {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )

            return {
                "success": True,
                "model": model_name,
                "text": response.text or "",
                "error": None,
            }

        except errors.ServerError as exc:
            errors_detected.append(
                f"{model_name}: servicio temporalmente no disponible"
            )

            print(
                f"{model_name} no está disponible. "
                "Probando siguiente modelo..."
            )

    return {
        "success": False,
        "model": None,
        "text": "",
        "error": (
            "Los modelos Gemini están temporalmente "
            "no disponibles."
        ),
        "details": errors_detected,
    }


# ---------------------------------------------------------
# Prueba local
# ---------------------------------------------------------

if __name__ == "__main__":
    result = generate_response(
        prompt=(
            "Explica en una frase cuál es la función "
            "de un agente de ventas e inventario."
        ),
        system_instruction=(
            "Responde en español de forma profesional y concisa."
        ),
    )

    if result["success"]:
        print("\nRespuesta de Gemini:\n")
        print(result["text"])
        print(f"\nModelo utilizado: {result['model']}")

    else:
        print("\nLLM no disponible temporalmente.")
        print(result["error"])

        for detail in result.get("details", []):
            print(f"- {detail}")