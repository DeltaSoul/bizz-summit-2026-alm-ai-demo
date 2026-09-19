import os
import requests
import json

# 1. Variables de entorno (Inyectadas por GitHub Actions Secrets)
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip('/')
API_KEY = os.environ.get("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = "gpt-4o" # Nombre exacto del despliegue en Sweden Central

# 2. Leer la metadata de la solución
# Corrección de arquitectura: El comando unpack de Power Platform deposita el customizations.xml
# principal en la carpeta Other/, mientras que otros recursos tienen sus propias carpetas.
xml_path = "src/solution/Other/customizations.xml"
try:
    with open(xml_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
except FileNotFoundError:
    print(f"Error crítico: No se encontró el archivo en {xml_path}. Verifique la ejecución del paso Unpack.")
    exit(1)

# 3. El Prompt del Arquitecto
system_prompt = """
Eres un Arquitecto de Soluciones experto en Power Platform.
Tu objetivo es analizar el archivo customizations.xml de una solución y generar una especificación técnica en formato Markdown.

REGLAS ESTRICTAS:
1. Extrae todas las Entidades (Tablas) personalizadas.
2. Extrae las Relaciones entre ellas.
3. Genera un diagrama Entidad-Relación utilizando sintaxis Mermaid.js (bloque ```mermaid erDiagram ... ```).
4. El output debe ser SOLO el código Markdown válido, sin texto introductorio ni despedidas.
"""

user_prompt = f"Analiza el siguiente customizations.xml de la solución:\n\n{xml_content[:80000]}" 
# Truncado por límite de seguridad para la ventana de contexto del prompt.
# Nota técnica: gpt-4o soporta 128k tokens, pero truncamos para asegurar consistencia y coste.

# 4. Llamada REST a Azure OpenAI Foundry
url = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2025-01-01-preview"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY
}
payload = {
    "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    "temperature": 0.2
}

print("Enviando metadata de Dataverse a Azure AI Foundry...")
response = requests.post(url, headers=headers, json=payload)
response.raise_for_status()

# 5. Guardar el resultado Markdown
os.makedirs("out", exist_ok=True)
result_text = response.json()['choices'][0]['message']['content']

with open("out/TECHNICAL_SPEC.md", "w", encoding="utf-8") as out_file:
    out_file.write(result_text)

print("Especificación técnica autogenerada exitosamente en out/TECHNICAL_SPEC.md")
