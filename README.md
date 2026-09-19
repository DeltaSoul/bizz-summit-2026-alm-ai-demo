# 🚀 Bizz Summit 2026: ALM & AI Masterclass Demo

Bienvenido al repositorio oficial de la demostración para el **Bizz Summit 2026**. 
Esta arquitectura demuestra el ciclo de vida de aplicaciones (ALM) automatizado en **Power Platform** y **Azure**, integrado con capacidades de Inteligencia Artificial.

## 🏗️ Estructura del Repositorio

| Directorio | Propósito |
|------------|-----------|
| `/.github/workflows/` | Pipelines YAML de CI/CD (GitHub Actions) para automatizar el despliegue a los entornos TEST y PROD. |
| `/solutions/` | Código fuente desempaquetado de las soluciones de Dynamics 365 / Power Platform (XML, JSON, Plugins). |
| `/scripts/` | Scripts de PowerShell auxiliares para el despliegue de infraestructura y configuración de Azure AI. |
| `/docs/` | Diagramas de arquitectura (Mermaid) y material de apoyo para la ponencia. |

## 🌐 Entornos de Ejecución (Zero State Labs)
La demostración fluye a través de 3 entornos aislados en Dataverse:
1. **[DEV]** Development Environment (Construcción)
2. **[TEST]** Sandbox Environment (Pruebas Automatizadas)
3. **[PROD]** Production Environment (Versión Final)

---
*Desarrollado en Zero State Labs.*