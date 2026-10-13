import re


# ---------------------------------------------------------
# Patrones básicos
# ---------------------------------------------------------

SENSITIVE_PATTERNS = {
    "email": re.compile(
        r"\b[A-Za-z0-9._%+-]+@"
        r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "us_phone": re.compile(
        r"\b(?:\+1[-.\s]?)?"
        r"\(?\d{3}\)?[-.\s]?"
        r"\d{3}[-.\s]?"
        r"\d{4}\b"
    ),

    "us_ssn": re.compile(
        r"\b\d{3}-\d{2}-\d{4}\b"
    ),

    "gemini_api_key": re.compile(
        r"\bAIza[A-Za-z0-9_-]{20,}\b"
    ),
}


REPLACEMENTS = {
    "email": "[EMAIL_REDACTED]",
    "us_phone": "[PHONE_REDACTED]",
    "us_ssn": "[SSN_REDACTED]",
    "gemini_api_key": "[API_KEY_REDACTED]",
}


def detect_sensitive_data(text: str) -> dict:
    """
    Detecta categorías básicas de PII y secretos.
    """

    findings = {}

    for category, pattern in SENSITIVE_PATTERNS.items():
        matches = pattern.findall(text)

        if matches:
            findings[category] = len(matches)

    return {
        "contains_sensitive_data": bool(findings),
        "findings": findings,
    }


def redact_sensitive_data(text: str) -> str:
    """
    Reemplaza PII y secretos conocidos por etiquetas
    de redacción antes de utilizar o registrar el texto.
    """

    redacted = text

    for category, pattern in SENSITIVE_PATTERNS.items():
        redacted = pattern.sub(
            REPLACEMENTS[category],
            redacted,
        )

    return redacted


if __name__ == "__main__":
    example = (
        "Mi correo es demo@example.com, "
        "mi teléfono es 336-555-1234 "
        "y mi SSN es 123-45-6789."
    )

    print("Original:")
    print(example)

    print("\nDetección:")
    print(detect_sensitive_data(example))

    print("\nTexto protegido:")
    print(redact_sensitive_data(example))