import os
import sys
import requests
import json

# 1. Variables de entorno (Inyectadas por GitHub Actions Secrets)
ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip('/')
API_KEY = os.environ.get("AZURE_OPENAI_KEY")
DEPLOYMENT_NAME = "gpt-4o" # Nombre exacto del despliegue en Sweden Central

# 2. Leer la metadata de la solución de forma agnóstica
# Corrección arquitectónica: Recorremos src/solutions/[NOMBRE_SOLUCION] para soportar un Monorepo
solution_name_env = os.environ.get("SOLUTION_NAME", "BizzSummitDemoALM")
solution_dir = f"src/solutions/{solution_name_env}"
xml_content = ""

if not os.path.exists(solution_dir):
    print(f"Error crítico: No se encontró el directorio base {solution_dir}. Verifique el paso Unpack.")
    sys.exit(1)

for root, dirs, files in os.walk(solution_dir):
    for file_name in files:
        # QA: Añadimos .yaml para atrapar el código fuente de las Canvas Apps desempaquetadas
        if file_name.endswith(('.xml', '.json', '.yaml', '.yml')):
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    xml_content += f"\n--- ARCHIVO: {file_name} ---\n"
                    # Aumentamos a 30k por archivo para Canvas Apps complejas
                    xml_content += f.read()[:30000] 
            except Exception as e:
                print(f"Advertencia: No se pudo leer {file_path}: {e}")

if not xml_content.strip():
    print("Advertencia: No se encontraron archivos fuente en la solución. ¿Está vacía?")
    xml_content = "Solución vacía o sin componentes soportados."

# QA: GPT-4o soporta 128k tokens (~500k caracteres). Aumentamos el límite de 80k a 300k para soluciones Enterprise reales.
xml_content = xml_content[:300000]

# 3. El Prompt del Arquitecto
system_prompt = """
Eres un Arquitecto de Soluciones Enterprise experto en Microsoft Power Platform.
Tu objetivo es analizar el código fuente de una solución (XML de Dataverse, JSON de Power Automate, YAML de Canvas Apps) y generar una Especificación Técnica en formato Markdown estricto.

DEBES SEGUIR EXACTAMENTE ESTA ESTRUCTURA DE DOCUMENTO:

# Especificación Técnica de Arquitectura

## 1. Resumen Ejecutivo
(Redacta un resumen de 2 o 3 párrafos explicando la función de negocio global que cumple toda la solución en su conjunto, deduciéndolo de la suma de sus componentes).

## 2. Inventario de Componentes
(Crea una tabla Markdown con todos los componentes detectados).
CRÍTICO: NO incluyas archivos de metadatos internos del framework (como Solution.xml, Customizations.xml o archivos .json/.xml de configuración) en esta tabla. Lista ÚNICAMENTE componentes reales de negocio (Flows, Canvas Apps, Tablas, Connection References, Variables).
| Display Name | Logical Name / Archivo | Tipo (Flow, Table, App, EnvVar) | Descripción / Propósito |
|---|---|---|---|

## 3. Modelo de Datos (Dataverse)
(Si encuentras tablas/entidades en XML, genera un diagrama Entidad-Relación usando ```mermaid erDiagram```. 
CRÍTICO SINTAXIS MERMAID: En `erDiagram`, cada atributo DEBE llevar un tipo de dato, nombre y clave, separados por espacios. 
EJEMPLO ESTRICTO: 
```mermaid
erDiagram
  NombreTabla {
    string id PK
    string nombre
  }
```
Detalla los campos clave. Si no hay tablas, escribe "No aplica").

## 4. Lógica de Procesos (Power Automate)
(Por cada flujo JSON encontrado, redacta una breve explicación de sus triggers y acciones. Luego, dibuja la lógica usando ```mermaid flowchart TD```. Si no hay flujos, escribe "No aplica". 
CRÍTICO SINTAXIS MERMAID: En Mermaid, si el texto de un nodo tiene paréntesis u otros caracteres especiales, DEBES envolverlo obligatoriamente en comillas dobles, ejemplo: `B["Enviar correo (V2)"]`).

## 5. Interfaz de Usuario (Canvas / Model-Driven)
(Si encuentras definiciones de Apps, resume sus pantallas principales y su propósito. Si no hay, escribe "No aplica").
"""

user_prompt = f"Analiza los siguientes archivos fuente de la solución:\n\n{xml_content}"

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
try:
    # QA: Timeout estricto de 120s para no colgar el runner de GitHub Actions si Azure cae
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error crítico: Falló la comunicación con Azure OpenAI Foundry: {e}")
    sys.exit(1)

# 5. Guardar el resultado Markdown
os.makedirs("out", exist_ok=True)
result_text = response.json()['choices'][0]['message']['content']

with open("out/TECHNICAL_SPEC.md", "w", encoding="utf-8") as out_file:
    out_file.write(result_text)

print("Especificación técnica autogenerada exitosamente en out/TECHNICAL_SPEC.md")
