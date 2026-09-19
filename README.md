# 🚀 Autogenerando la especificación técnica de tu solución de Power Platform con Azure AI Foundry

**Bizz Summit 2026**

La creación y mantenimiento de la documentación técnica es, a menudo, el gran cuello de botella en los despliegues de Power Platform. Redactar diccionarios de datos, mapear dependencias y detallar los componentes de una solución consume un tiempo vital. Pero, ¿y si tu pipeline de despliegue lo hiciera todo por ti?

En esta sesión técnica, desglosaremos la arquitectura de un flujo de Application Lifecycle Management (ALM) verdaderamente autónomo. Analizaremos el caso de uso y los componentes técnicos necesarios para interceptar los pipelines de despliegue mediante GitHub Actions, extrayendo la metadata de la solución en pleno vuelo.

A través de una demostración en vivo de un flujo ya implementado, veremos en acción cómo la automatización invoca a Azure AI Foundry nativamente desde el runner para analizar los archivos XML/JSON y el código fuente de los componentes (Canvas Apps, Cloud Flows). En la demo se mostrará la generación instantánea de una especificación técnica viva en el repositorio, un artefacto que documenta la lógica funcional de la solución, explica el código de cada app o flujo, expone las dependencias y renderiza automáticamente el modelo Entidad-Relación con Mermaid.js, sin intervención humana.

## 📊 Detalles de la Sesión
- **Session Format:** Sesión
- **Track:** Técnico
- **Applies to:** Power Apps, Power Automate, Dataverse, ALM, Azure AI
- **Level:** 300 (Advanced)
- **Language:** Español

## 🏗️ Estructura del Repositorio

| Directorio | Propósito |
|------------|-----------|
| `/.github/workflows/` | Pipelines YAML de GitHub Actions que orquestan el despliegue e invocan a Azure AI Foundry. |
| `/solutions/` | Código fuente desempaquetado de las soluciones (XML, JSON, Plugins) listo para ser analizado por la IA. |
| `/scripts/` | Scripts de PowerShell para la interacción con las APIs de Azure y extracción de metadata. |
| `/docs/` | Artefactos generados automáticamente (Especificaciones Técnicas, Diagramas Mermaid). |

---
*Demostración diseñada por Zero State Labs.*