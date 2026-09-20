import os
import requests
import json

# 1. Variables de entorno (Inyectadas por GitHub Actions Secrets)
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip('/')
API_KEY = os.environ.get("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = "gpt-4o" # Nombre exacto del despliegue en Sweden Central

# 2. Leer la metadata de la solución de forma agnóstica
# Corrección arquitectónica: En lugar de buscar solo Other/customizations.xml, 
# recorremos todo src/solution para capturar flujos (.json), tablas (.xml) y apps.
solution_dir = "src/solution"
xml_content = ""

if not os.path.exists(solution_dir):
    print(f"Error crítico: No se encontró el directorio base {solution_dir}. Verifique el paso Unpack.")
    exit(1)

for root, dirs, files in os.walk(solution_dir):
    for file_name in files:
        if file_name.endswith(('.xml', '.json')):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    xml_content += f"\n--- ARCHIVO: {file_name} ---\n"
                    xml_content += f.read()[:20000] # Evitar que un solo archivo inunde el buffer
            except Exception as e:
                print(f"Advertencia: No se pudo leer {file_path}: {e}")

if not xml_content.strip():
    print("Advertencia: No se encontraron archivos XML o JSON en la solución. ¿Está vacía?")
    xml_content = "Solución vacía o sin componentes soportados."

# Truncado general por seguridad de token (80k chars = ~20k tokens)
xml_content = xml_content[:80000]

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
